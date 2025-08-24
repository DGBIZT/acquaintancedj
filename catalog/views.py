from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.models import Product
from django.urls import reverse_lazy


from catalog.forms import ProductForm




class PublishListView(LoginRequiredMixin, View):

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        is_published = request.POST.get('is_published', 'off') == 'on'

        if product.is_published == is_published:
            return redirect('catalog:home')  # Если состояние не изменилось, просто редиректим

        # Определяем действие на основе текущего состояния
        if is_published:
            # Если продукт уже опубликован - отменяем публикацию
            if not request.user.has_perm('catalog.can_unpublish_product'):
                return HttpResponseForbidden("У вас нет прав на отмену публикации")
        else:
            # Если продукт не опубликован - публикуем
            if not request.user.has_perm('catalog.can_publish_product'):
                return HttpResponseForbidden("У вас нет прав на публикации ")

        product.is_published = is_published
        product.save()

        return redirect('catalog:home')


class SubmitDataView(View): # SubmitDataView — это гибкий инструмент для обработки HTTP-запросов в Django

    def post(self): # def post(self, request, *args, **kwargs):
        return HttpResponse("Данные отправлены")

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Фильтруем только опубликованные статьи
        user = self.request.user
        if user.is_staff:
            return Product.objects.all()
        return Product.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_publish'] = self.request.user.has_perm('catalog.can_publish_product')
        context['can_unpublish'] = self.request.user.has_perm('catalog.can_unpublish_product')
        return context



class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    # def get_object(self, queryset=None): # Счетчик просмотра страницы продукта
    #     self.object = super().get_object(queryset)
    #     self.object.views_count += 1
    #     self.object.save()
    #     return self.object

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

    def form_valid(self, form):
        form.instance.owner = self.request.user  # автоматически устанавливаем владельца
        return super().form_valid(form)


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
