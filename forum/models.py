import uuid
from django.db import models

from accounts.models import User


# class Thread(models.Model):
#     title = models.CharField(max_length=200)
#     creator = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title


class Post(models.Model):
    # thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to="posts/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    audio_video_or_image = models.FileField(
        upload_to="audio_video_or_image/", blank=True, null=True
    )  # TODO this field to be added in serializers
    author = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="posts"
    )

    def __str__(self):
        return f"Post by {self.author.username} in {self.title}"


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    audio_video_or_image = models.FileField(
        upload_to="audio_video_or_image/", blank=True, null=True
    )  # TODO this field to be added in serializers
    author = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"

