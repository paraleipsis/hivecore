from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
import pprint

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


urlpatterns = router.urls
