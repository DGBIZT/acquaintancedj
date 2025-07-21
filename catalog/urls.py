from django.urls import path, include
from . import views

app_name = "catalog"

urlpatterns = [
    path('home/', views.home, name='home' ),
    path('contacts/', views.contacts, name='contacts' ),
    path('submit_data/', views.submit_data, name='submit_data'),

]