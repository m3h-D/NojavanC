# Generated by Django 2.2.8 on 2020-05-19 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20200519_0907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='national_code',
        ),
        migrations.AddField(
            model_name='user',
            name='national_code',
            field=models.CharField(blank=True, max_length=120, unique=True),
        ),
    ]
