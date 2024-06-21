import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.conf import settings


class User(AbstractUser):
    USER_ROLES = (
        ("farmer", "Farmer"),
        ("buyer", "Buyer"),
        ("extension_officer", "Agricultural Officer"),
    )

    TANZANIAN_REGIONS = (
        ("Arusha", "Arusha"),
        ("Dar es Salaam", "Dar es Salaam"),
        ("Dodoma", "Dodoma"),
        ("Geita", "Geita"),
        ("Iringa", "Iringa"),
        ("Kagera", "Kagera"),
        ("Katavi", "Katavi"),
        ("Kigoma", "Kigoma"),
        ("Kilimanjaro", "Kilimanjaro"),
        ("Lindi", "Lindi"),
        ("Manyara", "Manyara"),
        ("Mara", "Mara"),
        ("Mbeya", "Mbeya"),
        ("Morogoro", "Morogoro"),
        ("Mtwara", "Mtwara"),
        ("Mwanza", "Mwanza"),
        ("Njombe", "Njombe"),
        ("Pwani", "Pwani"),
        ("Rukwa", "Rukwa"),
        ("Ruvuma", "Ruvuma"),
        ("Shinyanga", "Shinyanga"),
        ("Simiyu", "Simiyu"),
        ("Singida", "Singida"),
        ("Songwe", "Songwe"),
        ("Tabora", "Tabora"),
        ("Tanga", "Tanga"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=USER_ROLES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    profile_photo = models.ImageField(blank=True, null=True)

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,14}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.",
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, unique=True
    )

    location = models.CharField(max_length=15, choices=TANZANIAN_REGIONS)
    is_active = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=True) #TODO change to False
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "role",
        "first_name",
        "last_name",
        "phone_number",
        "location",
    ]

    def save(self, *args, **kwargs):
        if self.is_email_verified:
            self.is_active = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class UserVisit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} visited at {self.timestamp}"
