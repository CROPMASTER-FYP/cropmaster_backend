from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import permissions, viewsets, status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from cropmaster import perms
from .models import ExtensionOfficer, Message, Response as ExpertResponse
from .serializers import (
    ResponseSerializer,
    ExtensionOfficerSerializer,
    MessageSerializer,
)
from farmer.models import Farmer

# Create your views here.


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        perms.IsFarmer,
        perms.IsSenderOrReceiver,
    ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        if "responses" in request.path:
            responses_serializer = ResponseSerializer(
                instance.responses.all(), many=True
            )
            data = serializer.data
            data["responses"] = responses_serializer.data
            return Response(data)

        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, "farmer"):
            farmer_instance = user.farmer
        else:
            farmer_instance, _ = Farmer.objects.get_or_create(user=user)

        extension_officer_id = self.kwargs.get("extension_officer_id")
        print(f"Extension officer ID from URL: {extension_officer_id}")
        User = get_user_model()
        try:
            user = User.objects.get(id=extension_officer_id)
            print(f"User found: {user}")

            extension_officer, created = ExtensionOfficer.objects.get_or_create(
                user=user
            )
            if created:
                print("ExtensionOfficer created.")
            else:
                print(f"Extension officer found: {extension_officer}")
        except User.DoesNotExist:
            raise ValidationError("User not found")

        serializer.save(farmer=farmer_instance, extension_officer=extension_officer)

        serializer.save(farmer=farmer_instance, extension_officer=extension_officer)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["extension_officer"] = self.kwargs.get("extension_officer_id")
        return context


class ExtensionOfficerViewSet(viewsets.ModelViewSet):
    serializer_class = ExtensionOfficerSerializer

    def get_queryset(self):
        User = get_user_model()
        return User.objects.filter(role="extension_officer")

    # def get_queryset(self):
    #     return ExtensionOfficer.objects.all()


class ExtensionOfficerMessagesViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsExtensionOfficerSender]

    def get_queryset(self): 
        extension_officer_id = self.kwargs.get("extension_officer_id")
        extension_officer = ExtensionOfficer.objects.filter(
            user__id=extension_officer_id
        ).first()
        if extension_officer:
            return Message.objects.filter(extension_officer=extension_officer)
        else:
            return Message.objects.none()


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = ExpertResponse.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        perms.IsSenderOrReceiver,
        perms.IsExtensionOfficerSender,
        perms.IsFarmerOrExtensionOfficer,
    ]

    def get_queryset(self):
        message_id = self.kwargs.get("message_id")
        return ExpertResponse.objects.filter(message=message_id)

    def perform_create(self, serializer):
        message_id = self.kwargs.get("message_id")
        message_instance = Message.objects.get(pk=message_id)
        serializer.save(responder=self.request.user, message=message_instance)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["message"] = self.kwargs.get("message_id")
        return context
