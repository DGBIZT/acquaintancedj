from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from blog.models import Blog


# Create your views here.
class SubmitDataView(View): # SubmitDataView — это гибкий инструмент для обработки HTTP-запросов в Django

    def post(self, request, *args, **kwargs): # def post(self, request, *args, **kwargs):
        return HttpResponse("Данные отправлены")

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blogs_list.html'
    context_object_name = 'blogs'

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

class BlogCreateView(CreateView):
    model = Blog
    fields = ['title', 'content', 'image']
    template_name = 'blog/blog_form.html'
    # success_url = reverse_lazy('blog:blog_detail')

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.object.pk})

class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['title', 'content', 'image']
    template_name = 'blog/blog_form.html'
    # success_url = reverse_lazy('blog:blog_detail')

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.object.pk})

class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'Blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:blogs_list')

