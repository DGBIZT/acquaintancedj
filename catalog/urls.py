from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "catalog"

urlpatterns = ([
    path('home/', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('submit_data/', views.submit_data, name='submit_data'),
    path('productinform/', views.product_information, name='product_information'),
    path('index/', views.index, name='index'),
    path('product_detail/<int:product_id>', views.product_detail, name='product_detail'),
    path('base/', views.base, name='base'),
] )

