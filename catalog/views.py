from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from catalog.models import Product
from django.urls import reverse_lazy


from catalog.forms import ProductForm
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver


@receiver([post_save, post_delete, pre_save], sender=Product)
def clear_product_cache(sender, **kwargs):
    # Очищаем оба кэша при любом изменении продукта
    cache.delete('products_queryset_admin')
    cache.delete('products_queryset')

def my_view(request):
    data = cache.get('my_key') # Пытаемся получить данные из кэша

    if not data:
        data = 'some expensive computation' # выполняются «дорогостоящие» вычисления
        cache.set('my_key', data, 60 * 15) # Сохраняем результат в кэш на 15 минут

    return HttpResponse(data)  # Возвращаем ответ пользователю

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
        user = self.request.user
        cache_key = 'products_queryset_admin' if user.is_staff else 'products_queryset'

        queryset = cache.get(cache_key)
        if not queryset:
            if user.is_staff:
                queryset = Product.objects.all()
            else:
                queryset = Product.objects.filter(is_published=True)
            cache.set(cache_key, queryset, 60 * 15)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_publish'] = self.request.user.has_perm('catalog.can_publish_product')
        context['can_unpublish'] = self.request.user.has_perm('catalog.can_unpublish_product')
        return context


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        # Создаем уникальный ключ кэша для каждого продукта
        cache_key = f'product_detail_{self.kwargs["pk"]}'

        # Пытаемся получить объект из кэша
        obj = cache.get(cache_key)
        if not obj:
            # Если объект не найден в кэше, получаем его из базы данных
            obj = super().get_object(queryset)
            # Сохраняем полученный объект в кэш на 15 минут
            cache.set(cache_key, obj, 60 * 15)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['can_edit'] = product.owner == self.request.user or self.request.user.has_perm(
            'catalog.can_publish_product')
        return context

    # def get_object(self, queryset=None):
    #     # Создаем уникальный ключ кэша для каждого продукта
    #     cache_key = f'product_detail_{self.kwargs["pk"]}'
    #
    #     # Пытаемся получить объект из кэша
    #     obj = cache.get(cache_key)
    #     if not obj:
    #         obj = super().get_object(queryset)
    #         # Увеличиваем счетчик просмотров
    #         obj.views_count += 1
    #         obj.save()
    #         # Сохраняем в кэш на 15 минут
    #         cache.set(cache_key, obj, 60 * 15)
    #
    #     return obj


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
