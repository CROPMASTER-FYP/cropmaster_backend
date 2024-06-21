from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from farmer.models import Farmer
from farmer.serializers import FarmeraSerializer
from .models import User
from dj_rest_auth.serializers import UserDetailsSerializer
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    farmer = FarmeraSerializer(required=False)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    repeat_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "repeat_password",
            "email",
            "role",
            "phone_number",
            "location",
            "profile_photo",
            "farmer",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["repeat_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields do not match."}
            )
        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        farmer_data = validated_data.pop("farmer", None)
        validated_data.pop("repeat_password")

        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if user.role == "farmer" and farmer_data:
                Farmer.objects.create(user=user, **farmer_data)

            verification_url = request.build_absolute_uri(
                reverse("verify-email", args=[user.id])
            )
            send_mail(
                "Verify your email",
                f"Click the link to verify your email: {verification_url}",
                "no-reply@yourdomain.com",
                [user.email],
                fail_silently=False,
            )
        return user

    def update(self, instance, validated_data):
        farmer_data = validated_data.pop("farmer", None)  # Add this line
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.location = validated_data.get("location", instance.location)
        instance.profile_photo = validated_data.get(
            "profile_photo", instance.profile_photo
        )
        instance.save()
        if instance.role == "farmer" and farmer_data:  # Add this line
            Farmer.objects.update_or_create(
                user=instance, defaults=farmer_data
            )  # Add this line
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.role != "farmer":  # Add this line
            representation.pop("farmer", None)  # Add this line
        return representation


from rest_framework.decorators import action
from .models import UserVisit


class UserVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVisit
        fields = "__all__"


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = (
            "pk",
            "username",
            "email",
            "role",
            "phone_number",
            "location",
            "first_name",
            "last_name",
        )
        read_only_fields = ("pk", "email")

    def to_representation(self, instance):
        print("Using CustomUserDetailsSerializer")
        return super().to_representation(instance)
