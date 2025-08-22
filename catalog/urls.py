from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import SubmitDataView, ProductListView, ProductDetailView, ProductTemplateView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = "catalog"

urlpatterns = ([
    path('home/', ProductListView.as_view(), name='home'),
    path('contacts/', ProductTemplateView.as_view(), name='contacts'),
    path('submit_data/', SubmitDataView.as_view(), name='submit_data'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/new/',ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name="product_update"),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name="product_delete")


] )

# urlpatterns = ([
#     path('home/', views.home, name='home'),
#     path('contacts/', views.contacts, name='contacts'),
#     path('submit_data/', views.submit_data, name='submit_data'),
#     path('productinform/', views.product_information, name='product_information'),
#     path('index/', views.index, name='index'),
#     path('product_detail/<int:product_id>', views.product_detail, name='product_detail'),
#     path('base/', views.base, name='base'),
# ] )