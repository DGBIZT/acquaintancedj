from django.urls import path
from .views import BlogListView, BlogDetailView, BlogUpdateView, SubmitDataView, BlogCreateView, BlogDeleteView

app_name = "blog"

urlpatterns = [
    path('blog_list/', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetailView.as_view() , name="blog_detail"),
    path('blog/new/', BlogCreateView.as_view(), name="blog_create"),
    path('blog/update/<int:pk>/', BlogUpdateView.as_view(), name="blog_update"),
    path('blog/delete/<int:pk>/', BlogDeleteView.as_view(), name="blog_delete"),
    path('submit_data/', SubmitDataView.as_view(), name='submit_data'),

]