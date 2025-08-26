from django.db import models
from django.conf import settings

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    # author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='photos/', verbose_name='Фотография')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    is_published = models.BooleanField(
        default=False,  # по умолчанию запись не публикуется
        db_index=True,  # для оптимизации запросов
        help_text='Установите флажок для публикации записи на сайте',
        verbose_name='Опубликован',
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # удаляются продукты при удалении пользователя
        # on_delete=models.SET_NULL, при удалении пользователя, поле owner будет установлено в NULL
        null=True, blank=True, # позволяют полю быть пустым
        related_name='products', # позволяет получить все продукты пользователя через user.products.all()
        verbose_name='Владелец'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['title']
        permissions = [
            ('can_unpublish_product', 'can unpublish product'),
            ('can_publish_product', 'сan publish product')
        ]

