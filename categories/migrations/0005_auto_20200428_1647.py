# Generated by Django 3.0.3 on 2020-04-28 16:47

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0004_auto_20200428_1641'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CategoryContributors',
            new_name='CategoryContributor',
        ),
    ]
