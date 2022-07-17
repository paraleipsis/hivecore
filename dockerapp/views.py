from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


import redis
import json

redis_instance = redis.StrictRedis(decode_responses=True)


class ImagesViewSet(ViewSet):

    def list(self, request, format=None):
        items = json.loads(redis_instance.get('/images'))
        return Response(items)
        


@api_view()
def container_list(request):
    items = json.loads(redis_instance.get('/containers'))
    return Response(items)

@api_view()
def network_list(request):
    items = json.loads(redis_instance.get('/networks'))
    return Response(items)

@api_view()
def volume_list(request):
    items = json.loads(redis_instance.get('/volumes'))
    return Response(items)

@api_view()
def service_list(request):
    items = json.loads(redis_instance.get('/services'))
    return Response(items)

@api_view()
def node_list(request):
    items = json.loads(redis_instance.get('/nodes'))
    return Response(items)

@api_view()
def swarm_list(request):
    items = json.loads(redis_instance.get('/swarm'))
    return Response(items)

@api_view()
def node_system_info(request):
    items = json.loads(redis_instance.get('/status'))
    return Response(items)

# @api_view()
# def image_detail(request, id):
#     return Response('ok')

# @api_view()
# def container_detail(request, id):
#     return Response('ok')

# @api_view()
# def network_detail(request, id):
#     return Response('ok')
