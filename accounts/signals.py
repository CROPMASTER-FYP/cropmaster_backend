from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import UserVisit

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserVisit.objects.create(user=user)
