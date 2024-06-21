from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
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


class PostSerializer(serializers.ModelSerializer):
    # title = models.
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(read_only=True)

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
        ]
        read_only_fields = ["author"]


# class ThreadSerializer(serializers.ModelSerializer):
#     posts = PostSerializer(many=True, read_only=True)

#     class Meta:
#         model = Thread
#         fields = ["id", "title", "creator", "created_at", "posts"]
#         read_only_fields = ["creator"]
