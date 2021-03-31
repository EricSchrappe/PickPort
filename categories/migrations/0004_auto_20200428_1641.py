# Generated by Django 3.0.3 on 2020-04-28 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0003_auto_20200426_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryContributors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contribs', to='categories.Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_contrib', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'category')},
            },
        ),
        migrations.AddField(
            model_name='category',
            name='contributors',
            field=models.ManyToManyField(related_name='contributors', through='categories.CategoryContributors', to=settings.AUTH_USER_MODEL),
        ),
    ]
