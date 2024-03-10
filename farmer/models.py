from django.db import models
from django.contrib.auth import get_user_model


class Farmer(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="farmer"
    )
    farm_size = models.PositiveIntegerField(null=True, blank=True)
    crops_grown = models.ManyToManyField("crops.Crop", related_name="farmers")
