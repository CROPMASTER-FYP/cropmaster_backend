from django.db import IntegrityError
from django.utils.text import slugify
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from crops.models import Crop, CropDescription, Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["rating", "comment", "user"]
        read_only_fields = ["user"]


class CropDescriptionSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)

    class Meta:
        model = CropDescription
        # fields = "__all__"
        extra_kwargs = {"crop": {"required": False}}
        fields = [
            "planting_requirements",
            "irrigation_schedule",
            "fertilizer_recommendations",
            "pest_management",
            "harvesting_techniques",
            "total_rating",
            "total_ratings_count",
            "ratings",
        ]
        read_only_fields = ["total_rating", "total_ratings_count"]


class CropSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    # description = CropDescriptionSerializer()
    # description = serializers.StringRelatedField(many=True, read_only=True, source="cropdescription_set")
    description = CropDescriptionSerializer(many=True, source="cropdescription_set")

    class Meta:
        model = Crop
        fields = "__all__"
        read_only_fields = ["added_by"]
        # fields = ['id', 'slug', 'name', 'image', 'description', 'created_at', 'updated_at']
        # read_only =
        # fields = ["name", "image", "description"]

    def get_slug(self, instance):
        if isinstance(instance, Crop):
            return slugify(instance.name)
        return None

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("id")
        return ret

    def create(self, validated_data):
        description_data = validated_data.pop("cropdescription_set", [])
        try:
            if self.context["request"].user.is_authenticated:
                validated_data["added_by"] = self.context["request"].user
            else:
                raise ValidationError("Please login or create an account to add crops")
            crop = Crop.objects.create(**validated_data)
            if description_data:
                for desc_data in description_data:
                    CropDescription.objects.create(crop=crop, **desc_data)
            return crop
        except IntegrityError:
            raise serializers.ValidationError("Crop with this name already exists")
