from rest_framework import serializers
from .models import Like, Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "author",
            "content",
            "audio_video_or_image",
            "created_at",
        ]
        read_only_fields = ["author"]

    def get_author(self, obj):
        return obj.author.username if obj.author else None


class PostSerializer(serializers.ModelSerializer):
    # title = models.
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            # "thread",
            "author",
            "content",
            "created_at",
            "comments",
            # "thread",
            "audio_video_or_image",
            "likes_count",
            "liked_by_user",
        ]
        read_only_fields = ["author"]

    def get_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                Like.objects.get(post=obj, user=request.user)
                return True
            except Like.DoesNotExist:
                return False
        return False


# class ThreadSerializer(serializers.ModelSerializer):
#     posts = PostSerializer(many=True, read_only=True)

#     class Meta:
#         model = Thread
#         fields = ["id", "title", "creator", "created_at", "posts"]
#         read_only_fields = ["creator"]
