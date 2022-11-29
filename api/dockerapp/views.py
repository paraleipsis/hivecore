from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .serializers import (ContainerSerializer, ImageSerializer, BuildImageSerializer, CreateContainerSerializer, 
                          CreateNetworkSerializer, NetworkSerializer, CreateVolumeSerializer, VolumesSerializer, 
                          ConfigsSerializer, CreateConfigSerializer, SecretsSerializer, CreateSecretSerializer, 
                          ServicesSerializer, CreateServiceSerializer, ImagePruneSerializer, ImagePullSerializer,
                          ImageSerializer)
from .tasks import (pull_image, build_image, container_action, 
                    create_container, create_network, create_volume, 
                    create_config, create_secret, create_service,
                    prune_images)
from django.conf import settings
import json

redis_instance = settings.REDIS_INSTANCE

# image list, image pull
class ImagesViewSet(ViewSet):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ImagePullSerializer
        if self.request.method == 'DELETE':
            return ImagePruneSerializer
        return ImageSerializer
    # serializer_class = ImageSerializer

    # pull images
    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        # pull_image.delay(serializer.data)
        items = json.loads(redis_instance.get('/images'))
        return Response(items)

    def delete(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        prune_images.delay(serializer.data)
        items = json.loads(redis_instance.get('/images'))
        return Response(items)

    def list(self, request, format=None):
        # serializer = self.get_serializer_class()(data=request.data)
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
        serializer = ContainerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        container_action.delay(serializer.data)
        items = json.loads(redis_instance.get('/containers'))
        return Response(items)


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
    serializer_class = VolumesSerializer

    def list(self, request, format=None):
        items = json.loads(redis_instance.get('/volumes'))
        return Response(items)


class CreateVolumeViewSet(ViewSet):
    serializer_class = CreateVolumeSerializer

    def list(self, request, format=None):
        return Response('ok')

    def create(self, request):
        serializer = CreateVolumeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_volume.delay(serializer.data)
        return Response(serializer.data)


class ConfigsViewSet(ViewSet):
    serializer_class = ConfigsSerializer

    def list(self, request, format=None):
        items = json.loads(redis_instance.get('/configs'))
        return Response(items)


class CreateConfigViewSet(ViewSet):
    serializer_class = CreateConfigSerializer

    def list(self, request, format=None):
        return Response('ok')

    def create(self, request):
        serializer = CreateConfigSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serialized_data = serializer.data  # copy of serializer.data (property returns OrderedDict - immutable)
        if 'data_path' in serializer.data.keys():
            serialized_data['data_path'] = request.data['data_path'].read().decode("utf-8")  # change key that contains null to data from file

        create_config.delay(serialized_data)
        return Response(serialized_data)


class SecretsViewSet(ViewSet):
    serializer_class = SecretsSerializer

    def list(self, request, format=None):
        items = json.loads(redis_instance.get('/secrets'))
        return Response(items)


class CreateSecretViewSet(ViewSet):
    serializer_class = CreateSecretSerializer

    def list(self, request, format=None):
        return Response('ok')

    def create(self, request):
        serializer = CreateSecretSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serialized_data = serializer.data  # copy of serializer.data (property returns OrderedDict - immutable)
        if 'data_path' in serializer.data.keys():
            serialized_data['data_path'] = request.data['data_path'].read().decode("utf-8")  # change key that contains null to data from file

        create_secret.delay(serialized_data)
        return Response(serialized_data)


class ServicesViewSet(ViewSet):
    serializer_class = ServicesSerializer

    def list(self, request, format=None):
        items = json.loads(redis_instance.get('/services'))
        return Response(items)


class CreateServiceViewSet(ViewSet):
    serializer_class = CreateServiceSerializer

    def list(self, request, format=None):
        return Response('ok')

    def create(self, request):
        serializer = CreateServiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data
        print(serialized_data)

        for i in ('configs', 'secrets'):
            if len(serialized_data[i]) > 0:
                serialized_data[i] = '\r\n'.join(serialized_data[i])
            else:
                serialized_data[i] = None

        serialized_data['networks'] = list(serialized_data['networks'])
        create_service.delay(serialized_data)
        return Response(serializer.data)


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


class HostStatusViewSet(ViewSet):

    def list(self, request, format=None):
        items = json.loads(redis_instance.get('hosts_errors'))
        return Response(items)
