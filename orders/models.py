import uuid
from django.db import models

from crops.models import Crop
from farmer.models import Farmer

# Create your models here.


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.OneToOneField(Crop, on_delete=models.CASCADE, related_name="product")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    farmer = models.ForeignKey(
        Farmer, on_delete=models.CASCADE, related_name="products", null=True, blank=True
    )
    description = models.TextField()
    image = models.ImageField(upload_to="products/")
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name.name


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="orders"
    )
    farmer = models.ForeignKey(
        "farmer.Farmer", on_delete=models.CASCADE, related_name="orders"
    )
    product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, related_name="orders"
    )
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    # order_status = models.CharField(max_length=20, default="pending")
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.buyer.username

    # def save(self, *args, **kwargs):
    #     self.total_cost = self.product.price * self.quantity
    #     super().save(*args, **kwargs)
