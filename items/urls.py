from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from items import views

app_name = 'items'

urlpatterns = [
	path('create/<int:pk>', views.CreateItem, name='create'),
	path('delete/<int:pk>', views.DeleteItem, name='delete'),
	path('update/<int:pk>', views.UpdateItem, name='update'),
	path('shuffle/<int:pk>', views.ShuffleItem, name='shuffle'),
]

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)