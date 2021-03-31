from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from accounts import views

app_name = 'accounts'

urlpatterns = [
	path('signup/', views.SignUpView.as_view(), name='signup'),
	path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)