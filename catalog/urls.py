from django.urls import path
from .views import (SubmitDataView, ProductListView, ProductDetailView, ProductTemplateView,
                    ProductCreateView, ProductUpdateView, ProductDeleteView, PublishListView, CategoryProductsView)

app_name = "catalog"

urlpatterns = [
    path('home/', ProductListView.as_view(), name='home'),
    path('contacts/', ProductTemplateView.as_view(), name='contacts'),
    path('submit_data/', SubmitDataView.as_view(), name='submit_data'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/new/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name="product_update"),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name="product_delete"),
    path('publish/<int:product_id>/', PublishListView.as_view(), name='publish'),
    path('category/<int:category_id>/', CategoryProductsView.as_view(), name='category'),
]
