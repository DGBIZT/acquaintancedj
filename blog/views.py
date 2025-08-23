from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.forms import BlogForm
from blog.models import Blog


# Create your views here.
class SubmitDataView(View): # SubmitDataView — это гибкий инструмент для обработки HTTP-запросов в Django

    def post(self, request, *args, **kwargs): # def post(self, request, *args, **kwargs):
        return HttpResponse("Данные отправлены")

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blogs_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        # Фильтруем только опубликованные статьи
        return Blog.objects.filter(is_published=True)

class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_object(self, queryset=None): # Счетчик просмотра страницы блога
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    # success_url = reverse_lazy('blog:blog_detail')

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.object.pk})

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    # success_url = reverse_lazy('blog:blog_detail')

    def get_success_url(self): # Возвращение на страницу только что отредактируемого блога
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = 'blog/blog_config_delete.html'
    success_url = reverse_lazy('blog:blog_list')

