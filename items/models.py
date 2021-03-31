from django.db import models
from django.utils import timezone
from django.urls import reverse
from categories.models import Category

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class Items(models.Model):
	name = models.CharField(max_length=255)
	category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
	created_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('categories:single')