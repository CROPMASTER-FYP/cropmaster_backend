from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.UserCreateAPIView.as_view(), name='user-create'),
    path('users/', views.UserListAPIView.as_view(), name='user-list'),
]
