from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Crop(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="crops/", null=True, blank=True)
    # description = models.ForeignKey("CropDescription", on_delete=models.CASCADE, related_name="crop_description", null=True, blank=True) # TODO has to be null?
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("crop-detail", kwargs={"slug": self.slug})


class CropDescription(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    planting_requirements = models.TextField()
    irrigation_schedule = models.TextField()
    fertilizer_recommendations = models.TextField()
    pest_management = models.TextField()
    harvesting_techniques = models.TextField()

    def __str__(self):
        return self.crop.name
