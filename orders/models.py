import uuid
from django.db import models

# Create your models here.


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100) #TODO the name of the product is the name of the crop
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    farmer = models.ForeignKey(
        "farmer.Farmer", on_delete=models.CASCADE, related_name="products"
    )
    # TODO do we need a crop_ id here?
    description = models.TextField()
    image = models.ImageField(upload_to="products/")
    
    


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="orders"
    )
    farmer = models.ForeignKey(
        "farmer.Farmer", on_delete=models.CASCADE, related_name="orders"
    )
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="orders"
    )
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, default="pending")
    is_delivered = models.BooleanField(default=False)
