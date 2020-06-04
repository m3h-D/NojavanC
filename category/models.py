from django.db import models
from nojavan.utils import hash_file_name

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    image = models.ImageField(blank=True, null=True, upload_to=hash_file_name)
    description = models.TextField()


class Favorite(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    image = models.ImageField(blank=True, null=True, upload_to=hash_file_name)
    description = models.TextField()