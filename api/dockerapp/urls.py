from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'images', views.ImagesViewSet, basename='images')
router.register(r'build_image', views.BuildImagesViewSet, basename='build_image')

router.register(r'containers', views.ContainersViewSet, basename='containers')
router.register(r'create_container', views.CreateContainerViewSet, basename='create_container')

router.register(r'networks', views.NetworksViewSet, basename='networks')
router.register(r'create_network', views.CreateNetworkViewSet, basename='create_network')

router.register(r'volumes', views.VolumesViewSet, basename='volumes')
router.register(r'create_volume', views.CreateVolumeViewSet, basename='create_volume')

router.register(r'services', views.ServicesViewSet, basename='services')
router.register(r'create_service', views.CreateServiceViewSet, basename='create_service')

router.register(r'nodes', views.NodesViewSet, basename='nodes')
router.register(r'swarm', views.SwarmViewSet, basename='swarm')
router.register(r'status', views.StatusViewSet, basename='status')

router.register(r'configs', views.ConfigsViewSet, basename='configs')
router.register(r'create_config', views.CreateConfigViewSet, basename='create_config')

router.register(r'secrets', views.SecretsViewSet, basename='secrets')
router.register(r'create_secret', views.CreateSecretViewSet, basename='create_secret')


urlpatterns = router.urls
