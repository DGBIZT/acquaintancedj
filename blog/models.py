from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(null=True, blank=True, verbose_name='содержимое')
    image = models.ImageField(upload_to='photos/', verbose_name='превью (изображение)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    # Поле для признака публикации, признак публикации (булевое поле)
    is_published = models.BooleanField(
        default=False,  # по умолчанию запись не публикуется
        db_index=True,  # для оптимизации запросов
        help_text='Установите флажок для публикации записи на сайте',
        verbose_name = 'Опубликован',
    )
    # Поле для подсчета просмотров
    views_count = models.PositiveIntegerField(default=0, db_index=True, verbose_name="Количество просмотров")


    def __str__(self):
        return self.title



    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ['title']
