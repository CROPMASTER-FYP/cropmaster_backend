from django.urls import path
from .views import PostViewSet, CommentViewSet

urlpatterns = [
    # path(
    #     "threads/",
    #     ThreadViewSet.as_view({"get": "list", "post": "create"}),
    #     name="thread-list",
    # ),
    # path(
    #     "threads/<int:pk>/",
    #     ThreadViewSet.as_view(
    #         {"get": "retrieve", "put": "update", "delete": "destroy"}
    #     ),
    #     name="thread-detail",
    # ),
    path(
        "posts/<int:pk>/add_comment/",
        CommentViewSet.as_view({"post": "add_comment"}),
        name="post-add-comment",
    ),
    path(
        "posts/<int:pk>/like/",
        PostViewSet.as_view({"post": "like_post"}),
        name="post-like",
    ),
    path(
        "posts/<int:pk>/unlike/",
        PostViewSet.as_view({"post": "unlike_post"}),
        name="post-unlike",
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
    # path(
    #     "comments/",
    #     CommentViewSet.as_view({"get": "list", "post": "create"}),
    #     name="comment-list",
    # ),
    # path(
    #     "comments/<int:pk>/",
    #     CommentViewSet.as_view(
    #         {"get": "retrieve", "put": "update", "delete": "destroy"}
    #     ),
    #     name="comment-detail",
    # ),
]
