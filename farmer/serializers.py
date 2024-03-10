from rest_framework import serializers
from .models import Farmer
from accounts.serializers import UserSerializer


class FarmerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Farmer
        fields = ["user", "farm_size", "crops_grown"]
