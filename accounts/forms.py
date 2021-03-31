from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class UserSignUpForm(UserCreationForm):
	class Meta():
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
		model = get_user_model()
