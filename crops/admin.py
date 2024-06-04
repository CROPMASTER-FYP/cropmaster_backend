from django.contrib import admin

from crops.models import Crop, CropCategory, Rating

# Register your models here.

admin.site.register(CropCategory)
admin.site.register(Crop)
admin.site.register(Rating)
