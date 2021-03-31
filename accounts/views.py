from django.shortcuts import render
from django.contrib.auth import login, logout
from django.views.generic import CreateView
from django.urls import reverse_lazy
from accounts.forms import UserSignUpForm

# Create your views here.
class SignUpView(CreateView):
	template_name = 'accounts/signup.html'
	form_class = UserSignUpForm
	success_url = reverse_lazy('login')