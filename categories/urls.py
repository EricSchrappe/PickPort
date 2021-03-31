from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from categories import views

app_name = 'categories'

urlpatterns = [
	path('list/', views.ListCategoryView.as_view(), name='list'),
	path('userlist/<int:pk>', views.UserListCategoryView.as_view(), name='userlist'),
	path('detail/<slug:slug>/', views.DetailCategoryView.as_view(), name='single'),
	path('create/', views.CreateCategoryView.as_view(), name='create'),
	path('update/<slug:slug>/', views.UpdateCategoryView.as_view(), name='update'),
	path('delete/<slug:slug>/', views.DeleteCategoryView.as_view(), name='delete'),
	path('search/', views.SearchCategoryView.as_view(), name='search'),
	path('subscribe/<slug:slug>/', views.SubCategoryView.as_view(), name='subscribe'),
	path('unsubscribe/<slug:slug>/', views.UnSubCategoryView.as_view(), name='unsubscribe'),
	path('like/<slug:slug>/', views.LikeCategoryView.as_view(), name='like'),
	path('unlike/<slug:slug>/', views.UnLikeCategoryView.as_view(), name='unlike'),
	path('sublist/<int:pk>', views.SubListCategoryView.as_view(), name='sublist'),
	path('contriblist/<int:pk>', views.RequestListContribView.as_view(), name='contriblist'),
	path('requestcontrib/<slug:slug>/', views.RequestContribView.as_view(), name='requestcontrib'),
	path('approvecontrib/<int:owner>/<int:pk>', views.ApproveContribView.as_view(), name='approvecontrib'),
	path('removecontrib/<int:owner>/<int:pk>', views.RemoveContribView.as_view(), name='removecontrib'),
]

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)