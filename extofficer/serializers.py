from rest_framework import serializers

from accounts.models import User
from .models import ExtensionOfficer, Message
from django.contrib.auth import get_user_model


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiving_officer = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "topic",
            "message",
            "created_at",
            "updated_at",
            "sender",
            "receiving_officer",
            "extension_officer",
        ]

    def get_sender(self, obj):
        farmer = obj.farmer
        return farmer.user.username if farmer else None

    def get_receiving_officer(self, obj):
        extension_officer = obj.extension_officer
        return extension_officer.user.username if extension_officer else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get("request") and self.context["request"].method == "GET":
            data.pop("extension_officer", None)
        return data


class ExtensionOfficerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), write_only=True
    )

    class Meta:
        model = User
        fields = [
            "user",
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
        ]

    def get_fields(self):
        fields = super().get_fields()
        for field_name in fields:
            fields[field_name].read_only = True
        return fields

    def to_representation(self, instance):
        """
        Serialize the user instance only if the role is 'agricultural_officer'
        """
        if instance.role == "agricultural_officer":
            return super().to_representation(instance)
        return None
