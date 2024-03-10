import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    USER_ROLES = (
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
        ('agricultural_officer', 'Agricultural Officer'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=USER_ROLES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, unique=True)
    

    location = models.CharField(max_length=12)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role', 'first_name', 'last_name', 'phone_number', 'location']


    def __str__(self):
        return self.username
