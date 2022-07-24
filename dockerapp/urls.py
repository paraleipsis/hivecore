from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# urlpatterns = [
#     path('images/', views.image_list),
#     # path('images/<id>/', views.image_detail),
#     path('containers/', views.container_list),
#     # path('containers/<id>/', views.container_detail),
#     path('networks/', views.network_list),
#     # path('containers/<id>/', views.network_detail)
#     path('volumes/', views.volume_list),
#     path('services/', views.service_list),
#     path('nodes/', views.node_list),
#     path('swarm/', views.swarm_list),
#     path('info/', views.node_system_info),
# ]

router = DefaultRouter()
router.register(r'images', views.ImagesViewSet, basename='images')
router.register(r'images/build', views.BuildImagesViewSet, basename='build')

router.register(r'containers', views.ContainersViewSet, basename='containers')
router.register(r'containers/create_container', views.CreateContainerViewSet, basename='create_container')

router.register(r'networks', views.NetworksViewSet, basename='networks')
router.register(r'networks/create_network', views.CreateNetworkViewSet, basename='create_network')

router.register(r'volumes', views.VolumesViewSet, basename='volumes')
router.register(r'volumes/create_volume', views.CreateVolumeViewSet, basename='create_volume')

router.register(r'services', views.ServicesViewSet, basename='services')
router.register(r'services/create_service', views.CreateServiceViewSet, basename='create_service')

router.register(r'nodes', views.NodesViewSet, basename='nodes')
router.register(r'swarm', views.SwarmViewSet, basename='swarm')
router.register(r'status', views.StatusViewSet, basename='status')

router.register(r'configs', views.ConfigsViewSet, basename='configs')
router.register(r'configs/create_config', views.CreateConfigViewSet, basename='create_config')

router.register(r'secrets', views.SecretsViewSet, basename='secrets')
router.register(r'secrets/create_secret', views.CreateSecretViewSet, basename='create_secret')


urlpatterns = router.urls
