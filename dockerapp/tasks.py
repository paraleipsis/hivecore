import dataclasses
import json
import requests
import docker
import redis
from celery import shared_task


# claim ip's
client = docker.APIClient()
redis_instance = redis.StrictRedis()

@shared_task
def collect_docker_stuff():
    nodes = client.nodes()
    res = []
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    for ip in nodes:
        res.append(
            {
                'ip': str(ip['Status']['Addr']),
                'endpoints': json.loads(requests.get(f"http://{ip['Status']['Addr']}:8001", headers=headers).text)
                }
        )

        redis_instance.set("docker_stuff", json.dumps(res))
        
    return None


@shared_task
def sort_docker_stuff():
    items = json.loads(redis_instance.get('docker_stuff')) # json with info from hosts to list
    endpoints = ['/status', '/images', '/containers', '/networks', '/volumes', '/services', '/nodes', '/swarm', '/configs', '/secrets']

    for endpoint in range(len(endpoints)): # sort by endpoints
        current_info_list = []
        for i in range(len(items)):

            # if not manager skip  ['/services', '/nodes', '/swarm', 'configs', 'secrets']
            if endpoint >= 5 and items[i]['endpoints']['/status']['Swarm']['ControlAvailable'] is False:
                continue

            ip = items[i]['ip']
            host = items[i]['endpoints']['/status']['Name']
            collections = items[i]['endpoints'][endpoints[endpoint]]

            if endpoints[endpoint] in ('/swarm', '/status'):
                current_info_list.append({'ip': ip, 'host': host, 'type': endpoints[endpoint], 'items': collections})
            else:
                for collection in collections:
                    if endpoints[endpoint] == '/nodes':
                        host = collection['Description']['Hostname']
                        ip = collection['Status']['Addr']
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

    subnet, gateway  = '', ''
    if 'subnet' in data.keys():
        subnet = data.pop('subnet')

    if 'gateway' in data.keys():
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
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    nodes = json.loads(redis_instance.get('/nodes'))['result']
    ip = [x for x in nodes if x['host'] == data['node']][0]['ip']
    data = json.dumps({'params': {x: data[x] for x in data if x not in "node"}, 'task': 'create_service'})
    print(data)
    # requests.post(f"http://{ip}:8001", headers=headers, data=data)  # response code for sending data