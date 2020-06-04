from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from nojavan.utils import create_slug
from .models import Group, Profile
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def assign_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
