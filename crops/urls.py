from django.urls import path
from .views import CropsViewSet


urlpatterns = [
    path('crops/', CropsViewSet.as_view({'get': 'list', 'post': 'create'}), name='crops'),
    path('crops/<slug:slug>/', CropsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='crop-detail')
]
