# Generated by Django 2.2.8 on 2020-05-16 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usertracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertracker',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
