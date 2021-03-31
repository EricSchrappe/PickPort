from django.contrib import admin
from items.models import Items

# Register your models here.

class ItemsAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(Items, ItemsAdmin)