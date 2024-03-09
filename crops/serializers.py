from django.utils.text import slugify
from rest_framework import serializers
from crops.models import Crop, CropDescription


class CropDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropDescription
        # fields = "__all__"
        extra_kwargs = {"crop": {"required": False}}
        fields = ['planting_requirements', 'irrigation_schedule', 'fertilizer_recommendations', 'pest_management', 'harvesting_techniques']


class CropSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    # description = CropDescriptionSerializer()
    # description = serializers.StringRelatedField(many=True, read_only=True, source="cropdescription_set")
    description = CropDescriptionSerializer(many=True, source="cropdescription_set")

    class Meta:
        model = Crop
        fields = "__all__"
        # fields = ['id', 'slug', 'name', 'image', 'description', 'created_at', 'updated_at']
        # read_only =
        # fields = ["name", "image", "description"]

    def get_slug(self, instance):
        return slugify(instance.name)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("id")
        return ret

    def create(self, validated_data):
        description_data = validated_data.pop("description")
        crop = Crop.objects.create(**validated_data)
        CropDescription.objects.create(crop=crop, **description_data)
        return crop
