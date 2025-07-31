from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product
from django.db import connection
from django.utils import timezone

class Command(BaseCommand):
    help = 'Load test data from fixture'

    def handle(self, *args, **options):
        # Удаляем существующие записи
        Category.objects.all().delete()
        Product.objects.all().delete()

        # Сброс автоинкремента
        with connection.cursor() as cursor:
            cursor.execute('ALTER SEQUENCE catalog_category_id_seq RESTART WITH 1;')

        call_command('loaddata','catalog_fixture.json' )

        # Обновляем `created_at` и `updated_at` для всех объектов
        for product in Product.objects.all():
            product.created_at = timezone.now()
            product.updated_at = timezone.now()
            product.save()

        self.stdout.write(self.style.SUCCESS("Успешно загруженные данные из fixture"))