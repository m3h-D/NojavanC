from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()



class ChatRoom(models.Model):
    receivers = models.ManyToManyField(User, related_name='chatroomreceivers', blank=True)
    # title = models.CharField(max_length=120, blank=True, null=True)
    # slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    # messages = models.ManyToManyField('Message', blank=True)


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='message', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messagesender', blank=True, null=True, on_delete=models.SET_NULL)
    # receiver = models.ForeignKey(User, related_name='messagereceiver', blank=True, null=True, on_delete=models.SET_NULL)
    # group = models.ManyToManyField(User, related_name='messagegroup', blank=True)
    content = models.TextField()
    is_readed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)

