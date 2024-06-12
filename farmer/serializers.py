from rest_framework import serializers
from crops.models import Crop
from .models import Farmer


class FarmeraSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    crops_grown = serializers.PrimaryKeyRelatedField(
        queryset=Crop.objects.all(), many=True, required=False
    )
    # crops_grown = CropSerializer(many=True, read_only=True)

    class Meta:
        model = Farmer
        fields = ["crops_grown"]

    def create(self, validated_data):
        crops_data = validated_data.pop("crops_grown")  # Add this line
        farmer = Farmer.objects.create(**validated_data)
        farmer.crops_grown.set(crops_data)  # Add this line
        return farmer

    def update(self, instance, validated_data):
        crops_data = validated_data.pop("crops_grown")  # Add this line
        # instance.farm_size = validated_data.get("farm_size", instance.farm_size)
        instance.save()
        instance.crops_grown.set(crops_data)  # Add this line
        return instance
