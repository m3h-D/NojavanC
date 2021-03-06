# Generated by Django 2.2.10 on 2020-06-05 08:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('message', '0004_auto_20200526_0833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='chatroom',
            name='title',
        ),
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
        migrations.AddField(
            model_name='chatroom',
            name='receivers',
            field=models.ManyToManyField(blank=True, related_name='chatroomreceivers', to=settings.AUTH_USER_MODEL),
        ),
    ]
