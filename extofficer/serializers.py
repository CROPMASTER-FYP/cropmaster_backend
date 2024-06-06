from rest_framework import serializers

from accounts.models import User
from .models import ExtensionOfficer, Message, Response
from django.contrib.auth import get_user_model


class ResponseSerializer(serializers.ModelSerializer):
    responder_name = serializers.SerializerMethodField()

    class Meta:
        model = Response
        # fields = "__all__"
        fields = ["response_text", "created_at", "responder", "responder_name", "image_or_video"]
        read_only_fields = [
            "id",
            "responder",
            "responderr",
            "created_at",
            "updated_at",
            "message",
        ]

    def create(self, validated_data):
        message = self.context["message"]
        validated_data["message_id"] = message
        return super().create(validated_data)

    def get_responder_name(self, obj):
        return obj.responder.username


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiving_officer = serializers.SerializerMethodField()
    responses = ResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        # fields = "__all__"
        fields = [
            "topic",
            "message",
            "created_at",
            "updated_at",
            "sender",
            "receiving_officer",
            # "extension_officer",
            "responses",
            "image_or_video",
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

    def validate(self, data):
        if "extension_officer" in self.context:
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
            "location",
        ]

    # def get_fields(self):
    #     fields = super().get_fields()
    #     for field_name in fields:
    #         fields[field_name].read_only = True
    #     return fields

    # def to_representation(self, instance):
    #     """
    #     Serialize the user instance only if the role is 'extension_officer'
    #     """
    #     if instance.role == "extension_officer":
    #         return super().to_representation(instance)
    #     return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["role"] = "extension_officer"
        return data
