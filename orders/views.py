from rest_framework import viewsets, permissions
from rest_framework.response import Response
from buyer.models import Buyer

from farmer.models import Farmer
from .models import Product
from .serializers import ProductSerializer

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from rest_framework import status


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(serializer.data)

    # def perform_create(self, serializer):
    #     serializer.save(farmer=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        farmer_instance, _ = Farmer.objects.get_or_create(user=user)
        serializer.save(farmer=farmer_instance)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [YourAuthenticationClass]

    def perform_create(self, serializer):
        user = self.request.user
        buyer_instance, _ = Buyer.objects.get_or_create(user=user)
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]
        total_cost = product.price * quantity

        farmer_instance = product.farmer

        serializer.validated_data["total_cost"] = total_cost
        serializer.validated_data["buyer"] = user
        serializer.validated_data["farmer"] = farmer_instance

        # serializer.save(buyer=self.request.user)
        # serializer.save(buyer=buyer_instance)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
