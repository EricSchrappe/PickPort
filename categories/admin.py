from django.contrib import admin
from categories import models

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)


admin.site.register(models.Category, CategoryAdmin)