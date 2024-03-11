from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Response as ExpertResponse
from .serializers import ResponseSerializer
from extofficer.models import ExtensionOfficer, Message
from extofficer.serializers import ExtensionOfficerSerializer, MessageSerializer
from farmer.models import Farmer

# Create your views here.


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

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
        farmer_instance, _ = Farmer.objects.get_or_create(user=user)
        serializer.save(farmer=farmer_instance)


class ExtensionOfficerViewSet(viewsets.ModelViewSet):
    serializer_class = ExtensionOfficerSerializer

    def get_queryset(self):
        User = get_user_model()
        return User.objects.filter(role="agricultural_officer")


class ExtensionOfficerMessagesViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        extension_officer_uuid = self.kwargs.get("extension_officer_id")
        extension_officer = ExtensionOfficer.objects.filter(
            user__id=extension_officer_uuid
        ).first()
        if extension_officer:
            return Message.objects.filter(extension_officer=extension_officer)
        else:
            return Message.objects.none()


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = ExpertResponse.objects.all()
    serializer_class = ResponseSerializer

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
