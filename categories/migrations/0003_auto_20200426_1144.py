# Generated by Django 3.0.3 on 2020-04-26 11:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0002_auto_20200423_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(related_name='subscribers', through='categories.CategorySubscriber', to=settings.AUTH_USER_MODEL),
        ),
    ]
