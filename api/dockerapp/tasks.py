import json
import requests
import docker
from docker.types import (TaskTemplate, ContainerSpec, ServiceMode, 
                          RestartPolicy, Mount, UpdateConfig, 
                          ConfigReference, SecretReference, 
                          EndpointSpec, NetworkAttachmentConfig)
from celery import shared_task
from requests.exceptions import ConnectionError
from hurry.filesize import size, si
from django.conf import settings


client = docker.APIClient()
redis_instance = settings.REDIS_INSTANCE

@shared_task
def collect_docker_stuff():
    nodes = client.nodes()
    res = []
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    for ip in nodes:
        try:
            res.append(
                {
                    'ip': str(ip['Status']['Addr']),
                    'endpoints': json.loads(requests.get(f"http://{ip['Status']['Addr']}:8001", headers=headers).text)
                    }
            )
        except ConnectionError:
            continue

        redis_instance.set("docker_stuff", json.dumps(res))
        
    return None


@shared_task
def sort_docker_stuff():
    items = json.loads(redis_instance.get('docker_stuff')) # json with info from hosts to list
    endpoints = ['/status', '/containers', '/images', '/networks', '/volumes', '/services', '/nodes', '/swarm', '/configs', '/secrets']

    for endpoint in range(len(endpoints)): # sort by endpoints
        current_info_list = []
        for i in range(len(items)):

            # if not manager skip  ['/services', '/nodes', '/swarm', 'configs', 'secrets']
            if endpoint >= 5 and items[i]['endpoints']['/status']['Swarm']['ControlAvailable'] is False:
                continue

            ip = items[i]['ip']
            host = items[i]['endpoints']['/status']['Name']
            collections = items[i]['endpoints'][endpoints[endpoint]]

            # '/swarm', '/status' enpoints return one dict instead of list of dicts so we dont need to iterate over it
            if endpoints[endpoint] in ('/swarm', '/status'):
                current_info_list.append({'ip': ip, 'host': host, 'type': endpoints[endpoint], 'items': collections})
            else:
                for collection in collections:
                    if endpoints[endpoint] == '/nodes':
                        host = collection['Description']['Hostname']
                        ip = collection['Status']['Addr']
                    # if there is no tag take tags from digest
                    
                    if endpoints[endpoint] == '/images':

                        containers = json.loads(redis_instance.get('/containers'))['result']
                        for container in containers:
                            image = collection['Id']
                            if image in container['items'].values():
                                collection['Used_by'] = container['items']['Id']
                                break
                            else:
                                collection['Used_by'] = 'unused'
                        
                        try:
                            if len(collection['RepoDigests']) != 0:
                                collection['Repository'] = collection['RepoDigests'][0][:collection['RepoDigests'][0].index('@')]
                            else:
                                collection['Repository'] = collection['RepoTags'][0][:collection['RepoTags'][0].index(':')]
                        except IndexError:
                            collection['Repository'] = '<none>'

                        collection['Created'] = collection['Created'][:collection['Created'].index('.')].replace('T', ' ')

                        # convert image size in bytes to mb
                        collection['Size'] = size(collection['Size'], system=si)

                        if 'ExposedPorts' in collection['Config']:
                            collection['Config']['ExposedPorts'] = list(collection['Config']['ExposedPorts'].keys())
                        else:
                            collection['Config']['ExposedPorts'] = 'No Exposed Ports'

                        if collection['Config']['Volumes']:
                            collection['Config']['Volumes'] = list(collection['Config']['Volumes'].keys())
                        else:
                            collection['Config']['Volumes'] = 'No Volumes'

                        if not collection['DockerVersion']:
                            collection['DockerVersion'] = 'Docker'

                        if not collection['Config']['Cmd']:
                            collection['Config']['Cmd'] = 'No CMD'

                        if not collection['Config']['Entrypoint']:
                            collection['Config']['Entrypoint'] = 'No Entrypoint'

                        if not collection['RepoTags']:
                            for digest in collection['RepoDigests']:
                                collection['RepoTags'].append(f"{digest[:digest.index('@')]}:<none>")

                    current_info_list.append({'ip': ip, 'host': host, 'type': endpoints[endpoint], 'items': collection})

        redis_instance.set(f"{endpoints[endpoint]}", json.dumps({'count': len(current_info_list), 'result': current_info_list}))

    return None


@shared_task
def pull_image(data):
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    nodes = json.loads(redis_instance.get('/nodes'))['result']
    ip = [x for x in nodes if x['host'] == data['node']][0]['ip']
    data = json.dumps({'params': {'image': data['image']}, 'task': 'image_pull'})
    requests.post(f"http://{ip}:8001", headers=headers, data=data)  # response code for sending data
    

@shared_task
def build_image(data):
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    nodes = json.loads(redis_instance.get('/nodes'))['result']
    ip = [x for x in nodes if x['host'] == data['node']][0]['ip']

    if 'dockerfile_path' in data.keys():
        data['fileobj'] = data.pop('dockerfile_path')
    else:
        data['fileobj'] = data.pop('dockerfile_field')

    data = json.dumps({'params': {x: data[x] for x in data if x not in "node"}, 'task': 'image_build'})
    requests.post(f"http://{ip}:8001", headers=headers, data=data)  # response code for sending data


@shared_task
def container_action(data):
    print(data)
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    ip = data.pop('container_ip')
    task = data.pop('container_signal')
    data = json.dumps({'params': data, 'task': task})
    requests.post(f"http://{ip}:8001", headers=headers, data=data)


@shared_task
def create_container(data):
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    nodes = json.loads(redis_instance.get('/nodes'))['result']
    ip = [x for x in nodes if x['host'] == data['node']][0]['ip']

    if data['network'] != 'None':
        data['network'] = data['network'].split(":")[2] # id from string 'name:host:id'
    else:
        del data['network']


    data['host_config'] = client.create_host_config()
    if 'ports' in data.keys():
        # example: 6000:6000, 6002 (there host port will be random)
        # 'xxxx:xxxx, xxxx:xxxx' to ['xxxx:xxxx', 'xxxx:xxxx']
        lst_of_ports = [i.split(':') for i in data['ports'].split(',')]
        # ['xxxx:xxxx', 'xxxx:xxxx'] to [{xxxx:xxxx}, {xxxx:xxxx}]
        lst_of_dicts_of_ports = [{int(i[0]): int(i[1])} if len(i) > 1 else {int(i[0]): None} for i in lst_of_ports]
        # [{xxxx:xxxx}, {xxxx:xxxx}] to [xxxx, xxxx] of keys - ports to open inside container
        ports = [[int(k) for k in i][0] for i in lst_of_dicts_of_ports]
        # list of dicts to one dict
        port_bindings = {k: v for d in lst_of_dicts_of_ports for k, v in d.items()}
        data['ports'] = ports
        data['host_config']['port_bindings'] = port_bindings

    # ls, /usr/bin/nginx -t
    if 'command' in data.keys():
        data['command'] = [i.strip() for i in data['command'].split(',')]

    # /home/user1/:/mnt/vol2:rw, /var/www:/mnt/vol1:ro
    if 'volumes' in data.keys():
        lst_of_volumes = [i.split(':') for i in data['volumes'].split(',')]
        lst_of_list_of_volumes = [[f'{i[0]}:{i[1]}:{i[2]}'] for i in lst_of_volumes]
        binds = [x.strip() for xs in lst_of_list_of_volumes for x in xs]
        volumes = [i[1] for i in lst_of_volumes]
        data['volumes'] = volumes
        data['host_config']['binds'] = binds

    # env from "a=a\r\nb=b" to ['a=a', 'b=b']
    if 'environment' in data.keys():
        data['environment'] = [i for i in data['environment'].split('\r\n')] # env from "a=a\r\nb=b" to ['a=a', 'b=b']

    # label: value
    if 'labels' in data.keys():
        data['labels'] = {k: v for d in [{j[0]: j[1]} for j in [i.split(':') for i in data['labels'].split('\r\n')]] for k, v in d.items()}

    if data['restart_policy'] != 'no':
        data['host_config']['RestartPolicy'] = {"Name": data['restart_policy'], "MaximumRetryCount": 5}

    del data['restart_policy']

    data = json.dumps({'params': {x: data[x] for x in data if x not in "node"}, 'task': 'create_container'})

    requests.post(f"http://{ip}:8001", headers=headers, data=data)  # response code for sending data


@shared_task
def create_network(data):
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    nodes = json.loads(redis_instance.get('/nodes'))['result']
    ip = [x for x in nodes if x['host'] == data['node']][0]['ip']

    if 'subnet' in data.keys() and 'gateway' in data.keys():
        subnet = data.pop('subnet')
        gateway = data.pop('gateway')

        ipam_pool = docker.types.IPAMPool(
            subnet=subnet,
            gateway=gateway
        )

        ipam_config = docker.types.IPAMConfig(
            pool_configs=[ipam_pool]
        )

        data['ipam'] = ipam_config

    # com.docker.network.bridge.enable_icc=true | options from "a=a\r\nb=b" to ['a=a', 'b=b']
    if 'options' in data.keys():
        data['options'] = {k: v for d in [{j[0]: j[1]} for j in [i.split('=') for i in data['options'].split('\r\n')]] for k, v in d.items()}

    if 'labels' in data.keys():
        data['labels'] = {k: v for d in [{j[0]: j[1]} for j in [i.split(':') for i in data['labels'].split('\r\n')]] for k, v in d.items()}
    print(data)

    data = json.dumps({'params': {x: data[x] for x in data if x not in "node"}, 'task': 'create_network'})
    requests.post(f"http://{ip}:8001", headers=headers, data=data)  # response code for sending data


@shared_task
def create_volume(data):
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    nodes = json.loads(redis_instance.get('/nodes'))['result']
    ip = [x for x in nodes if x['host'] == data['node']][0]['ip']

    if 'driver_opts' in data.keys():
        data['driver_opts'] = {k: v for d in [{j[0]: j[1]} for j in [i.split('=') for i in data['driver_opts'].split('\r\n')]] for k, v in d.items()}

    if 'labels' in data.keys():
        data['labels'] = {k: v.strip() for d in [{j[0]: j[1]} for j in [i.split(':') for i in data['labels'].split('\r\n')]] for k, v in d.items()}

    data = json.dumps({'params': {x: data[x] for x in data if x not in "node"}, 'task': 'create_volume'})
    requests.post(f"http://{ip}:8001", headers=headers, data=data)  # response code for sending data


@shared_task
def create_config(data):
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    nodes = json.loads(redis_instance.get('/nodes'))['result']
    ip = [x for x in nodes if x['host'] == data['node']][0]['ip']

    if 'data_path' in data.keys():
        data['data'] = data.pop('data_path')
    else:
        data['data'] = data.pop('data_field')

    if 'labels' in data.keys():
        data['labels'] = {k: v.strip() for d in [{j[0]: j[1]} for j in [i.split(':') for i in data['labels'].split('\r\n')]] for k, v in d.items()}

    data = json.dumps({'params': {x: data[x] for x in data if x not in "node"}, 'task': 'create_config'})
    requests.post(f"http://{ip}:8001", headers=headers, data=data)  # response code for sending data


@shared_task
def create_secret(data):
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    nodes = json.loads(redis_instance.get('/nodes'))['result']
    ip = [x for x in nodes if x['host'] == data['node']][0]['ip']

    if 'data_path' in data.keys():
        data['data'] = data.pop('data_path')
    else:
        data['data'] = data.pop('data_field')

    if 'labels' in data.keys():
        data['labels'] = {k: v.strip() for d in [{j[0]: j[1]} for j in [i.split(':') for i in data['labels'].split('\r\n')]] for k, v in d.items()}

    data = json.dumps({'params': {x: data[x] for x in data if x not in "node"}, 'task': 'create_secret'})
    print(data)
    requests.post(f"http://{ip}:8001", headers=headers, data=data)  # response code for sending data


@shared_task
def create_service(data):

    def dict_from_dict(source_dict={}, keys=[]):
        # form new dict from source dict with provided keys
        return {x:source_dict[x] if x in source_dict else None for x in keys}

    def field_mapping(data_dict, data_dict_key, sep=None, ports=False):
        try:
            # ports (no sht...)
            if ports:
                return {k: v for d in [{int(j[0]): int(j[1])} for j in [i.split(':') for i in data_dict[data_dict_key].split(',')]] for k, v in d.items()}
            # labels or environment variables (a=a/a: a to {a: a})
            return {k.strip(): v.strip() for d in [{j[0]: j[1]} for j in [i.split(sep) for i in data_dict[data_dict_key].split('\r\n')]] for k, v in d.items()}
        except AttributeError:
            return None

    def none_check(reference):
        i = field_mapping(data_dict=data, data_dict_key=reference, sep=':')
        if i is not None:
            if reference == 'secrets':
                return [SecretReference(secret_id=v, secret_name=k) for k, v in i.items()]
            return [ConfigReference(config_id=v, config_name=k) for k, v in i.items()]
        return None

    service = dict_from_dict(source_dict=data, keys=['service_name', 'labels'])
    container_spec = dict_from_dict(source_dict=data, keys=['image', 'hostname', 'environment', 'working_dir', 'open_stdin', 'tty'])
    mounts = dict_from_dict(source_dict=data, keys=['container_path', 'volume', 'read_only'])
    restart_policy = dict_from_dict(source_dict=data, keys=['restart_condition', 'restart_delay', 'max_attempts', 'restart_window'])
    endpoint_spec = dict_from_dict(source_dict=data, keys=['ports'])
    update_config = dict_from_dict(source_dict=data, keys=['update_parallelism', 'update_delay', 'failure_action', 'update_order'])
    service_mode = dict_from_dict(source_dict=data, keys=['scheduling_mode', 'replicas'])

    secret = none_check('secrets')
    config = none_check('configs')

    container_spec['environment'] = field_mapping(data_dict=container_spec, data_dict_key='environment', sep='=')
    endpoint_spec['ports'] = field_mapping(data_dict=endpoint_spec, data_dict_key='ports', ports=True)
    service['labels'] = field_mapping(data_dict=service, data_dict_key='labels', sep=':')

    if None in mounts.values():
        mounts = None
    else:
        mounts = [Mount(target=mounts['container_path'], source=mounts['volume'], read_only=mounts['read_only'])]
        

    client.create_service(
        task_template=TaskTemplate(
            container_spec=ContainerSpec(
                image=container_spec['image'],
                hostname=container_spec['hostname'],
                env=container_spec['environment'],
                workdir=container_spec['working_dir'],
                open_stdin=container_spec['open_stdin'],
                tty=container_spec['tty'],
                mounts=mounts,
                secrets=secret,
                configs=config
            ),
            restart_policy=RestartPolicy(
                condition=restart_policy['restart_condition'],
                delay=restart_policy['restart_delay'],
                max_attempts=restart_policy['max_attempts'],
                window=restart_policy['restart_window']
            ),
        ),
        endpoint_spec=EndpointSpec(ports=endpoint_spec['ports']),
        update_config=UpdateConfig(
            parallelism=update_config['update_parallelism'], 
            delay=update_config['update_delay'], 
            failure_action=update_config['failure_action'], 
            order=update_config['update_order']
        ),
        name=service['service_name'],
        labels=service['labels'],
        mode=ServiceMode(
            mode=service_mode['scheduling_mode'], 
            replicas=service_mode['replicas']
        ),
        networks=[NetworkAttachmentConfig(target=i.split(":")[2]) for i in data['networks']]
    )

    return None



