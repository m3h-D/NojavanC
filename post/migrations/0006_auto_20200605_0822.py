# Generated by Django 2.2.10 on 2020-06-05 08:22

from django.db import migrations, models
import nojavan.utils


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20200520_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=nojavan.utils.hash_file_name, validators=[nojavan.utils.validate_image_extention]),
        ),
        migrations.AlterField(
            model_name='post',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to=nojavan.utils.hash_file_name),
        ),
    ]
