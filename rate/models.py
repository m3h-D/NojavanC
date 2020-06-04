from django.db import models
from django.db.models import Count, Avg
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
from post.models import Post

import logging
import sys

User = get_user_model()

# Create your models here.


# def error_handling():
#     return f"{sys.exc_info()[0]}. ({sys.exc_info()[1]}) in Line {sys.exc_info()[2].tb_lineno}"


class RateManager(models.Manager):
    def get_avg_rate(self, post):
        """emtiaz dehi be post bar assasse rate entekhab shude (az 1 ta 5) taghsim bar tedad e user haey ke be in post emtiaz dadan"""

        try:
            # my_avg = self.filter_by_model(
            #     instance).aggregate(Avg('rating'))
            my_avg = super().filter(post=post).aggregate(Avg('rating'))
        except ZeroDivisionError:
            pass
        if my_avg['rating__avg'] is None:
            return 0.0
        return my_avg['rating__avg']




class Rate(models.Model):
    """modele emtiaz (rating star)"""
    user = models.ForeignKey(User, related_name="rate",
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='rate', on_delete=models.CASCADE)
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')
    RATING_LEVEL = (
        (1, 'خیلی بد'),
        (2, 'بد'),
        (3, 'متوسط'),
        (4, 'خوب'),
        (5, 'خیلی خوب'),
    )
    rating = models.IntegerField(choices=RATING_LEVEL, blank=True)
    objects = RateManager()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'post'),)
        verbose_name = "امتیاز"
        verbose_name_plural = "امتیاز ها"

    def __str__(self):
        return ("{} به ( {} ) امتیاز ( {} ) داده").format(self.user.username, self.post.title, self.get_rating_display())
    
    
