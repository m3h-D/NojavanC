  
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from nojavan.utils import create_slug
from .models import Post


@receiver(post_save, sender=Post)
def add_previous_post(sender, instance, created, *args, **kwargs):
    if created:
        instance.previous = instance.__class__.objects.filter(
            id__lt=instance.id).order_by('-id').first()
        instance.save()


@receiver(pre_save, sender=Post)
def post_slug_pre_populade(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)