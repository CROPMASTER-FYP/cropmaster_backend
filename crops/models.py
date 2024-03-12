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
    total_rating = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    total_ratings_count = models.PositiveIntegerField(default=0)

    # def update_rating(self):
    #     ratings = self.ratings.all()
    #     total = 0
    #     for rating in ratings:
    #         total += rating.rating
    #     self.total_rating = total / len(ratings)
    #     self.total_ratings_count = len(ratings)
    #     self.save()

    def update_rating(self):
        ratings = self.ratings.all()
        total = sum([rating.rating for rating in ratings])
        count = len(ratings)
        self.total_rating = total / count if count > 0 else 0
        self.total_ratings_count = count
        self.save()

    def __str__(self):
        return self.crop.name



class Rating(models.Model):
    crop_description = models.ForeignKey(
        CropDescription, on_delete=models.CASCADE, related_name="ratings"
    )
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.crop_description.update_rating()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.crop_description.update_rating()

    def __str__(self):
        return f"{self.user.username} rated {self.crop_description.crop.name} {self.rating}"
