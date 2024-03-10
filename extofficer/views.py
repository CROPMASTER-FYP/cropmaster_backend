from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets

from extofficer.models import ExtensionOfficer, Message
from extofficer.serializers import ExtensionOfficerSerializer, MessageSerializer
from farmer.models import Farmer

# Create your views here.


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        user = self.request.user
        farmer_instance, _ = Farmer.objects.get_or_create(user=user)
        serializer.save(farmer=farmer_instance)


class ExtensionOfficerViewSet(viewsets.ModelViewSet):
    serializer_class = ExtensionOfficerSerializer

    def get_queryset(self):
        User = get_user_model()
        return User.objects.filter(role="agricultural_officer")
