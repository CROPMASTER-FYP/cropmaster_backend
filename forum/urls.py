from django.urls import path
from rest_framework import routers
from .views import ThreadViewSet, PostViewSet, CommentViewSet

urlpatterns = [
    path(
        "threads/",
        ThreadViewSet.as_view({"get": "list", "post": "create"}),
        name="thread-list",
    ),
    path(
        "threads/<int:pk>/",
        ThreadViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="thread-detail",
    ),
    path(
        "posts/",
        PostViewSet.as_view({"get": "list", "post": "create"}),
        name="post-list",
    ),
    path(
        "posts/<int:pk>/",
        PostViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="post-detail",
    ),
    path(
        "comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="comment-list",
    ),
    path(
        "comments/<int:pk>/",
        CommentViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="comment-detail",
    ),
]
