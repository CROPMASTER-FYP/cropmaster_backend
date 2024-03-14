from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from cropmaster import perms
from rest_framework.filters import SearchFilter
from cropmaster.pagination import StandardResultsSetPagination
from .models import Thread, Post, Comment
from .serializers import ThreadSerializer, PostSerializer, CommentSerializer


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsFarmerOrExtensionOfficer]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["title"]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsFarmerOrExtensionOfficer]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsFarmerOrExtensionOfficer]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["content"]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
