from django.db import IntegrityError, transaction
from django.utils.text import slugify
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from crops.models import Crop, CropCategory, CropDescription, Rating


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CropCategory
        fields = ["name"]


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
    category = serializers.CharField(write_only=True)
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
        ret["category"] = instance.category.name if instance.category else None
        ret.pop("id")
        return ret

    @transaction.atomic
    def create(self, validated_data):
        description_data = validated_data.pop("cropdescription_set", [])
        category_name = validated_data.pop("category").lower()
        try:
            category, created = CropCategory.objects.get_or_create(name=category_name)
            validated_data["category"] = category

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

    @transaction.atomic
    def update(self, instance, validated_data):
        description_data = validated_data.pop("cropdescription_set", [])
        category_name = validated_data.pop("category").lower()

        try:
            category, created = CropCategory.objects.get_or_create(name=category_name)
            instance.category = category
            instance.name = validated_data.get("name", instance.name)
            instance.image = validated_data.get("image", instance.image)

            if self.context["request"].user.is_authenticated:
                instance.added_by = self.context["request"].user
            else:
                raise serializers.ValidationError(
                    "Please login or create an account to update crops"
                )

            instance.save()

            # Update or create descriptions
            existing_description_ids = {
                desc.id for desc in instance.cropdescription_set.all()
            }

            for desc_data in description_data:
                description_id = desc_data.get("id")
                if description_id and description_id in existing_description_ids:
                    description = CropDescription.objects.get(
                        id=description_id, crop=instance
                    )
                    description.planting_requirements = desc_data.get(
                        "planting_requirements", description.planting_requirements
                    )
                    description.irrigation_schedule = desc_data.get(
                        "irrigation_schedule", description.irrigation_schedule
                    )
                    description.fertilizer_recommendations = desc_data.get(
                        "fertilizer_recommendations",
                        description.fertilizer_recommendations,
                    )
                    description.pest_management = desc_data.get(
                        "pest_management", description.pest_management
                    )
                    description.harvesting_techniques = desc_data.get(
                        "harvesting_techniques", description.harvesting_techniques
                    )
                    description.save()
                else:
                    CropDescription.objects.create(crop=instance, **desc_data)

            # Remove descriptions not in the update data
            new_description_ids = {
                desc.get("id") for desc in description_data if desc.get("id")
            }
            ids_to_remove = existing_description_ids - new_description_ids
            CropDescription.objects.filter(id__in=ids_to_remove, crop=instance).delete()

            return instance
        except IntegrityError:
            raise serializers.ValidationError("Error updating crop description")
