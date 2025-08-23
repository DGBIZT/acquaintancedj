from tempfile import template

from django.urls import path
from .views import RegisterView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomAuthenticationForm

app_name = "users"

urlpatterns = ([
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(form_class = CustomAuthenticationForm, template_name = 'users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page = 'catalog:home'), name='logout'),

])