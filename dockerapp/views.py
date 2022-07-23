from traceback import print_tb
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from .serializers import ContainerSerializer, ImageSerializer, BuildImageSerializer, CreateContainerSerializer, CreateNetworkSerializer, NetworkSerializer
from .tasks import *
import redis
import json

redis_instance = redis.StrictRedis(decode_responses=True)


# image list, image pull
class ImagesViewSet(ViewSet):
    serializer_class = ImageSerializer

    # pull images
    def create(self, request):
        serializer = ImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pull_image.delay(serializer.data)
        return Response(serializer.data)

    def list(self, request, format=None):
        items = json.loads(redis_instance.get('/images'))
        return Response(items)


# build image from Dockerfile
class BuildImagesViewSet(ViewSet):
    serializer_class = BuildImageSerializer

    def list(self, request, format=None):
        return Response('ok')
    
    def create(self, request):
        serializer = BuildImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        '''serializer.data contains keys: tag, dockerfile_path | dockerfile_field, node
        dockerfile_path - from FileUpload field after serializer contains null because 
        path where file must be saved should be determined in model (that this app dont have), so file
        after serializing processing converts to null

        before converting to null we make copy of serializer.data and in that copy for dockerfile_path key
        we past data from uploaded file 

        after that we just continue to work with that copy (serialized_data) and forget about serializer.data
        '''

        serialized_data = serializer.data  # copy of serializer.data (property returns OrderedDict - immutable)
        if 'dockerfile_path' in serializer.data.keys():
            serialized_data['dockerfile_path'] = request.data['dockerfile_path'].read().decode("utf-8")  # change key that contains null to data from Dockefile

        build_image.delay(serialized_data)
        return Response(serialized_data)


# container list
class ContainersViewSet(ViewSet):
    serializer_class = ContainerSerializer

    def list(self, request, format=None):
        items = json.loads(redis_instance.get('/containers'))
        return Response(items)

    def post(self, request, *args, **kwargs):
        # set id's of containers to values of checkboxes by using react
        selected_values = request.POST.getlist('container')  # get list of checked items (id's of containers) by name of checkboxes

        # [454a18c9701, 134b18z9483, 984a18v0904] - example

        # in loop do start/stop/restart/pause/kill/resume/remove container

        # get name of pressed button
        # implement logic of interaction with this id's
        if request.POST.get("start"):
            pass
        elif request.POST.get("stop"):
            pass

        # ...

        return Response(request.POST)


# container create and start
class CreateContainerViewSet(ViewSet):
    serializer_class = CreateContainerSerializer

    def list(self, request, format=None):
        return Response('ok')

    def create(self, request):
        serializer = CreateContainerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_container.delay(serializer.data)
        return Response(serializer.data)


# network list
class NetworksViewSet(ViewSet):
    serializer_class = NetworkSerializer

    def list(self, request, format=None):
        items = json.loads(redis_instance.get('/networks'))
        return Response(items)


# network create
class CreateNetworkViewSet(ViewSet):
    serializer_class = CreateNetworkSerializer

    def list(self, request, format=None):
        return Response('ok')

    def create(self, request):
        serializer = CreateNetworkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_network.delay(serializer.data)
        return Response(serializer.data)


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
