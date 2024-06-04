from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from cropmaster import perms
from crops.serializers import CropSerializer, RatingSerializer
from .models import Crop, CropDescription, Rating


class CropsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing crops.
    """
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    lookup_field = "slug"
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    ordering = ["-created_at"]
    permission_classes = [permissions.IsAuthenticated, perms.ReadAccess]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single crop instance.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

    @action(detail=True, methods=["post"])
    def rate(self, request, pk=None):
        """
        Rate a crop.
        """
        crop = self.get_object()
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(crop=crop, user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        """
        Update a crop instance.
        """
        crop = self.get_object()
        if request.user != crop.added_by:
            return Response(
                {"message": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a crop instance.
        """
        crop = self.get_object()
        if request.user != crop.added_by:
            return Response(
                {"message": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)


class RateCropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsFarmerOrExtensionOfficer]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def rate(self, request, slug):
        try:
            crop = Crop.objects.get(slug=slug)
            crop_description = crop.cropdescription_set.first()
        except Crop.DoesNotExist:
            return Response(
                {"message": "Crop not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except CropDescription.DoesNotExist:
            return Response(
                {"message": "Crop description not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        rating_value = request.data.get("rating")

        if rating_value not in ["1", "2", "3", "4", "5"]:
            return Response(
                {"message": "Invalid rating value"}, status=status.HTTP_400_BAD_REQUEST
            )

        rating_value = int(rating_value)

        user = request.user

        try:
            previous_rating = Rating.objects.get(
                crop_description=crop_description, user=user
            )
            crop_description.total_rating -= previous_rating.rating
            crop_description.total_ratings_count -= 1
            previous_rating.rating = rating_value
            previous_rating.save()
        except Rating.DoesNotExist:
            previous_rating = None

        crop_description.total_rating = (
            crop_description.total_rating * crop_description.total_ratings_count
            + rating_value
        ) / (crop_description.total_ratings_count + 1)
        crop_description.total_ratings_count += 1
        crop_description.save()

        if not previous_rating:
            Rating.objects.create(
                crop_description=crop_description, user=user, rating=rating_value
            )

        return Response(
            {"message": "Rating added successfully"}, status=status.HTTP_201_CREATED
        )
