from django.db import models
from django.contrib.auth import get_user_model
from usertracker.models import UserTracker
from django.db.models import Count
from django.shortcuts import reverse
# from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField
from category.models import Category
from nojavan.utils import validate_image_extention
# Create your models here.
from nojavan.utils import hash_file_name

User = get_user_model()





class Tag(models.Model):
    title = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)

class PostManager(models.Manager):

    def published(self):
        return super().filter(status='published')


class Post(models.Model):
    author = models.ForeignKey(User, related_name='post', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=120, blank=True, allow_unicode=True)
    image = models.ImageField(blank=True, null=True, upload_to=hash_file_name, validators=[validate_image_extention,])
    video = models.FileField(blank=True, null=True, upload_to=hash_file_name)
    # content = RichTextUploadingField()
    content = models.TextField(blank=True, null=True)
    THE_STATUS = (
        ('published', 'منتشر شده'),
        ('draft', 'پیش نویس'),
        ('unpublished', 'منتشر نشده'),
    )
    category = models.ManyToManyField(
        Category, blank=True, related_name='post')
    # tag = models.ManyToManyField(
    #     Tag, related_name='post')
    previous = models.OneToOneField(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name="nextpost")
    special = models.BooleanField(default=False)
    status = models.CharField(max_length=11, choices=THE_STATUS)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    objects = PostManager()

    class Meta:
        ordering = ('-created_date',)
        index_together = (('id', 'slug'),)


    def recommended_posts(self, request):
        """
        category haye pishnahadi bar assasse view e user to har post.
        baraye inke az tedad like ha baraye post estefade konim ye
        GenericRelation ba Modele LikeDislike zadam
        """
        return UserTracker.objects.recommended_list(
            request=request, instance=self).annotate(count=Count('likes__likedislike')).order_by('-count')

    @property
    def post_viewed(self):
        """tedad view haey ke post khurde"""
        viewed_item = UserTracker.objects.filter_by_model(
            instance=self).values_list('ip_address', flat=True).distinct()
        return viewed_item

    @property
    def rated_post(self, **kwargs):
        if self.rate.filter(user=kwargs.get('request').user).exists():
            return True
        else:
            return False


    @property
    def get_absolute_url(self):
        return reverse('post:post_detail', args=[self.id, self.slug])

    @property
    def post_update_url(self):
        return reverse('post:update_post', args=[self.id, self.slug])
