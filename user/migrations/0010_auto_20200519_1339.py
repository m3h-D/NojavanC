# Generated by Django 2.2.8 on 2020-05-19 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20200519_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='national_code',
            field=models.CharField(blank=True, max_length=120, null=True, unique=True),
        ),
    ]