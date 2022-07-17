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
router.register(r'containers', views.ContainersViewSet, basename='containers')
router.register(r'networks', views.NetworksViewSet, basename='networks')
router.register(r'volumes', views.VolumesViewSet, basename='volumes')
router.register(r'services', views.ServicesViewSet, basename='services')
router.register(r'nodes', views.NodesViewSet, basename='nodes')
router.register(r'swarm', views.SwarmViewSet, basename='swarm')
router.register(r'status', views.StatusViewSet, basename='status')


urlpatterns = router.urls
