import json
import requests
import docker
import redis
from celery import shared_task
from hurry.filesize import size, si


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
    endpoints = ['/status', '/images', '/containers', '/networks', '/volumes', '/services', '/nodes', '/swarm']

    for endpoint in range(len(endpoints)): # sort by endpoints
        current_info_list = []
        for i in range(len(items)):

            if endpoint >= 5 and items[i]['endpoints']['/status']['Swarm']['ControlAvailable'] is False: # if not manager skip  ['/services', '/nodes', '/swarm']
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
        # redis_instance.set(f"{endpoints[endpoint]}", json.dumps(current_info_list))

    return None


@shared_task
def pull_image(data):
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    nodes = json.loads(redis_instance.get('/nodes'))['result']
    ip = [x for x in nodes if x['host'] == data['node']][0]['ip']
    data = json.dumps({'params': {'image': data['image']}, 'task': 'image_pull'})
    r = requests.post(f"http://{ip}:8001", headers=headers, data=data)  # response code for sending data
    print(r)
    print(ip)