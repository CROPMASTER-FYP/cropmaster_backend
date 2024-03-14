from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from buyer.models import Buyer
from cropmaster import perms
from cropmaster.pagination import StandardResultsSetPagination
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
    permission_classes = [permissions.IsAuthenticated] # , perms.IsFarmerOrBuyer TODO is this required in real sense?

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, perms.IsFarmerOrBuyer]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["description", "total_cost"]

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
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def buyer_orders(self, request, pk=None):
        user = self.request.user
        orders = self.get_queryset().filter(buyer=user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def farmer_orders(self, request, pk=None):
        user = self.request.user
        farmer_instance, _ = Farmer.objects.get_or_create(user=user)
        orders = self.get_queryset().filter(farmer=farmer_instance)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["put"])
    def mark_as_processed(self, request, pk=None):
        order = self.get_object()
        if request.user != order.buyer:
            return Response(
                {"message": "You are not authorized to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        order.processed = True
        order.save()
        return Response(
            {"message": "Order marked as processed"}, status=status.HTTP_200_OK
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.buyer:
            return Response(
                {"message": "You are not authorized to view this order."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.buyer:
            return Response(
                {"message": "You are not authorized to edit this order."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.buyer:
            return Response(
                {"message": "You are not authorized to delete this order."},
                status=status.HTTP_403_FORBIDDEN,
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
