from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from nojavan.utils import create_slug
from .models import Category, Favorite

@receiver(pre_save, sender=Category)
def category_slug_pre_populade(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

@receiver(pre_save, sender=Favorite)
def favorite_slug_pre_populade(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)