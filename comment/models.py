from django.db import models
from django.contrib.auth import get_user_model
from post.models import Post
from likedislike.models import LikeDislike

User = get_user_model()

# Create your models here.

class Comments(models.Model):
    """comment haye marboot be har user baraye har modeli"""
    user = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        """order kardane commentha barasase zamane sakht"""
        ordering = ('-timestamp',)

    def __str__(self):
        """neshun dadane karbar"""
        if self.parent is None:
            return "{} . کامنت گذاشت برای {} است".format(self.user.username,  self.content_object.title)
        else:
            return "جواب {} به کامنت {} در پست {}".format(self.user.username, self.parent.user.username, self.content_object.title)

    def children(self):
        """comment haye marboot be parent o barmigardoone """
        return Comments.objects.filter(parent=self, approved=True)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    @property
    def comment_like(self):
        """baraye neshun dadane tedad e like ha estefade mishe"""
        likes = LikeDislike.objects.filter_by_model(
            instance=self).filter(likedislike='like')

        return likes

    @property
    def comment_dislike(self):
        """baraye neshun dadane tedad e disloke ha estefade mishe"""
        dislikes = LikeDislike.objects.filter_by_model(
            instance=self).filter(likedislike='dislike')
        return dislikes