from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['can_edit'] = product.owner == self.request.user or self.request.user.has_perm(
            'catalog.can_publish_product')
        return context

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


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Убираем поле is_published, если у пользователя нет права публиковать
        if not self.request.user.has_perm('catalog.can_publish_product'):
            form.fields.pop('is_published', None)
        return form


class ProductUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/catalog_form.html'
    # success_url = reverse_lazy('blog:blog_detail')

    def test_func(self):
        product = self.get_object()
        return product.owner == self.request.user or self.request.user.has_perm('catalog.can_publish_product')

    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет прав для редактирования этого продукта.")

    def get_success_url(self): # Возвращение на страницу только что отредактируемого блога
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Показываем is_published только если есть право
        if not self.request.user.has_perm('catalog.can_publish_product'):
            form.fields.pop('is_published', None)
        return form

    def get_queryset(self):
        user = self.request.user
        # Модераторы и админы видят все товары
        if user.has_perm('catalog.can_publish_product'):
            return Product.objects.all()
        # Обычные пользователи — только свои
        return Product.objects.filter(owner=user)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_config_delete.html'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        product = self.get_object()
        # Модератор может удалить ЛЮБОЙ продукт, если у него есть право 'catalog.delete_product'
        # Владелец может удалить только свой продукт
        return product.owner == self.request.user or self.request.user.has_perm('catalog.delete_product')

    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет прав для удаления этого продукта.")
