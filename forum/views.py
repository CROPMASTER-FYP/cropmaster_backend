from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from cropmaster import perms
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from cropmaster.pagination import StandardResultsSetPagination
from .models import Like, Post, Comment
from .serializers import PostSerializer, CommentSerializer


# class ThreadViewSet(viewsets.ModelViewSet):
#     queryset = Thread.objects.all()
#     serializer_class = ThreadSerializer
#     permission_classes = [permissions.IsAuthenticated, perms.IsFarmerOrExtensionOfficer]
#     pagination_class = StandardResultsSetPagination
#     filter_backends = [SearchFilter, DjangoFilterBackend]
#     search_fields = ["title"]

#     def perform_create(self, serializer):
#         serializer.save(creator=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsFarmerOrExtensionOfficer]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
    
    @action(detail=True, methods=["post"])
    def like_post(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            # Check if the user already liked the post
            like = Like.objects.get(post=post, user=user)
            return Response({"error": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        except Like.DoesNotExist:
            # Create a new like
            like = Like.objects.create(post=post, user=user)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        
    @action(detail=True, methods=["post"])
    def unlike_post(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            # Check if the user already liked the post
            like = Like.objects.get(post=post, user=user)
            like.delete()
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Like.DoesNotExist:
            return Response({"error": "You haven't liked this post yet."}, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsFarmerOrExtensionOfficer]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["content"]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def add_comment(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
