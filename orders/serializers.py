from datetime import datetime
from rest_framework import serializers

from buyer.models import Buyer
from crops.models import Crop
from crops.serializers import CropSerializer
from farmer.models import Farmer
from .models import Product
from .models import Order


class CropeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crop
        fields = ("name",)


class ProductSerializer(serializers.ModelSerializer):
    # name = serializers.PrimaryKeyRelatedField(
    #     queryset=Crop.objects.all(), write_only=True
    # )
    # product_name = serializers.CharField(source="name.name", read_only=True)
    farmer = serializers.CharField(source="farmer.user.username", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    # def create(self, validated_data):
    #     user = self.context["request"].user
    #     farmer_instance, _ = Farmer.objects.get_or_create(user=user)
    #     validated_data["farmer"] = farmer_instance
    #     return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    farmer_name = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "buyer",
            "buyer_name",
            # "farmer",
            "farmer_name",
            "description",
            "total_cost",
            "created_at",
            "processed",
        ]
        # fields = '__all__'

        read_only_fields = (
            "buyer",
            # "farmer",
            "farmer_name",
            "buyer_name",
            "product_name",
            "total_cost",
            "processed",
            "created_at",
        )

    # def create(self, validated_data):
    #     user = self.context["request"].user
    #     validated_data["buyer"] = user
    #     return super().create(validated_data)

    def get_farmer_name(self, obj):
        # Assuming you have a ForeignKey relationship between Order and Farmer
        farmer_id = obj.farmer_id
        try:
            farmer = Farmer.objects.get(id=farmer_id)
            return farmer.user.username
        except Farmer.DoesNotExist:
            return 
            
    def get_buyer_name(self, obj):
        buyer_id = obj.buyer_id
        try:
            buyer = Buyer.objects.get(user__id=buyer_id)
            return buyer.user.username
        except Buyer.DoesNotExist:
            return None




class DateFieldFromDateTime(serializers.DateField):
    def to_representation(self, value):
        if isinstance(value, datetime):
            value = value.date()
        return super().to_representation(value)


class WeeklyOrderSerializer(serializers.Serializer):
    week = DateFieldFromDateTime()
    product = serializers.CharField(source="product__name__name")
    total_quantity = serializers.IntegerField()


class MonthlyOrderSerializer(serializers.Serializer):
    month = DateFieldFromDateTime()
    product = serializers.CharField(source="product__name__name")
    total_quantity = serializers.IntegerField()
