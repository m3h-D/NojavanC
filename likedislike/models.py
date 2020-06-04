from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
from django.template.defaultfilters import truncatewords_html, truncatewords, truncatechars_html
from django.utils.html import strip_tags
# from .manager import likedislike_manager
from nojavan.utils import get_client_ip, is_auth_or_not
from .signals import like_signal
# Create your models here.


User = get_user_model()


class LikeDislikeManager(models.Manager):
    """mesle manager e Comments"""

    def filter_by_model(self, instance):
        """bar assasse model filter mikonim"""
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        queryset = super(LikeDislikeManager, self).filter(
            content_type=content_type, object_id=obj_id)
        return queryset

    @is_auth_or_not
    def create_for_instance_model(self, instance, request, likedislike, user=None):
        """
        bar assasse model create mkonim
        age user anonymous bud bar assasse IP_address taghirat emal mishe
        age authenticate bud ke nega mikone bebine ip sh hast ya na age bud
        faqat user behesh mide...
        """
        ip_address = get_client_ip(request)
        content_type = ContentType.objects.get_for_model(instance.__class__)
        try:
            queryset = self.get(
                models.Q(
                    user=user,
                    content_type=content_type,
                    object_id=instance.id,
                ) |
                models.Q(
                    ip_address=ip_address,
                    content_type=content_type,
                    object_id=instance.id,
                )

            )

        except:
            queryset = self.create(
                user=user,
                ip_address=ip_address,
                content_type=content_type,
                object_id=instance.id,
                likedislike=likedislike,
            )
        else:
            like_signal.send(sender=queryset, ip_address=ip_address, likedislike=likedislike, request=request)

        return queryset


class LikeDislike(models.Model):
    """modeli baraye like o dislike eyek post ya comment"""
    user = models.ForeignKey(User, related_name='likedislike', blank=True, null=True,
                             on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=200, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    LIKED_OR_DISLIKE = (
        ('like', 'دوست دارد'),
        ('dislike', 'دوست ندارد'),
    )
    likedislike = models.CharField(
        max_length=10, blank=True, choices=LIKED_OR_DISLIKE)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = LikeDislikeManager()

    class Meta:
        """order kardan bar assasse timestamp"""
        ordering = ('-timestamp',)

    def __str__(self):
        try:
            return self.user.username
        except:
            return self.ip_address