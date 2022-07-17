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


class ContainersViewSet(ViewSet):

    def list(self, request, format=None):
        items = json.loads(redis_instance.get('/containers'))
        return Response(items)


class NetworksViewSet(ViewSet):

    def list(self, request, format=None):
        items = json.loads(redis_instance.get('/networks'))
        return Response(items)


class VolumesViewSet(ViewSet):

    def list(self, request, format=None):
        items = json.loads(redis_instance.get('/volumes'))
        return Response(items)


class ServicesViewSet(ViewSet):

    def list(self, request, format=None):
        items = json.loads(redis_instance.get('/services'))
        return Response(items)


class NodesViewSet(ViewSet):

    def list(self, request, format=None):
        items = json.loads(redis_instance.get('/nodes'))
        return Response(items)


class SwarmViewSet(ViewSet):

    def list(self, request, format=None):
        items = json.loads(redis_instance.get('/swarm'))
        return Response(items)


class StatusViewSet(ViewSet):

    def list(self, request, format=None):
        items = json.loads(redis_instance.get('/status'))
        return Response(items)

