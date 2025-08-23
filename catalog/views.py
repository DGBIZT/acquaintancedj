from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.models import Product
from django.urls import reverse_lazy

from catalog.forms import ProductForm




# Create your views here.
class SubmitDataView(View): # SubmitDataView — это гибкий инструмент для обработки HTTP-запросов в Django

    def post(self): # def post(self, request, *args, **kwargs):
        return HttpResponse("Данные отправлены")

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ProductTemplateView(TemplateView):
    model = Product
    template_name = 'catalog/contacts.html'
    context_object_name = 'contacts'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/catalog_form.html'
    # success_url = reverse_lazy('blog:blog_detail')

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(LoginRequiredMixin,UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/catalog_form.html'
    # success_url = reverse_lazy('blog:blog_detail')

    def get_success_url(self): # Возвращение на страницу только что отредактируемого блога
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_config_delete.html'
    success_url = reverse_lazy('catalog:home')
