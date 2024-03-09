from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from crops.serializers import CropSerializer
from .models import Crop


class CropsViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    lookup_field = "slug"
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["name", "price", "quantity", "farmer", "description", "image"]
    # search_fields = ["name", "price", "quantity", "farmer", "description", "image"]
    # ordering_fields = ["name", "price", "quantity", "farmer", "description", "image"]
    # ordering = ["-created_at"]
    # lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
