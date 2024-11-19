from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Registrations

@receiver(post_save, sender=User)
def create_registration(sender, instance, created, **kwargs):
    if created:
        Registrations.objects.create(user=instance)
