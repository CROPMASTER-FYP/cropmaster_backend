from django.db import models
from django.contrib.auth import get_user_model


class ExtensionOfficer(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="extension_officer"
    )


class Message(models.Model):
    extension_officer = models.ForeignKey(
        ExtensionOfficer, on_delete=models.CASCADE, related_name="messages"
    )
    farmer = models.ForeignKey(
        "farmer.Farmer", on_delete=models.CASCADE, related_name="messages"
    )
    topic = models.CharField(
        max_length=255, default=""
    )  # TODO topic will be get or created
    message = models.TextField()
    image_or_video = models.FileField(
        upload_to="forum/media/", blank=True, null=True
    )  # TODO this field to be added in serializers
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic


class Response(models.Model):
    message = models.ForeignKey(
        "Message", on_delete=models.CASCADE, related_name="responses"
    )
    responder = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    response_text = models.TextField()
    image_or_video = models.FileField(
        upload_to="forum/media/", blank=True, null=True
    )  # TODO this field to be added in serializers
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Response by {self.responder.username} on {self.message.topic}"
