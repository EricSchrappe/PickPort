from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=255, unique=True)
	description = models.TextField(blank=True, default='')
	slug = models.SlugField(allow_unicode=True, unique=True)
	created_date = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, default=999, related_name='user_categories', on_delete= models.CASCADE)
	subscribers = models.ManyToManyField(User, related_name= 'subscribers',through='CategorySubscriber')
	likes = models.ManyToManyField(User,related_name='likes', through='CategoryLike')
	contributors = models.ManyToManyField(User, related_name='contributors', through='CategoryContributor')
	
	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('categories:userlist', kwargs={'pk': self.user.id})

class CategorySubscriber(models.Model):
	user = models.ForeignKey(User, related_name='user_subs', on_delete=models.CASCADE)
	category = models.ForeignKey(Category, related_name='subs', on_delete=models.CASCADE)
	sub_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.first_name

	class Meta:
		unique_together = ("user", "category")

class CategoryLike(models.Model):
	user = models.ForeignKey(User, related_name='user_likes', on_delete=models.CASCADE)
	category = models.ForeignKey(Category, related_name='category_likes', on_delete=models.CASCADE)

	def __str_(self):
		return self.user.username

	class Meta:
		unique_together = ('user', 'category')

class CategoryContributor(models.Model):
	user = models.ForeignKey(User, related_name='user_contrib', on_delete=models.CASCADE)
	category = models.ForeignKey(Category, related_name='contribs', on_delete=models.CASCADE)
	approved =models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

	class Meta:
		unique_together = ('user', 'category')