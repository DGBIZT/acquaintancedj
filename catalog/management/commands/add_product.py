from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product
from django.db import connection
from django.utils import timezone

class Command(BaseCommand):
    help = "Добавление книги с тестами в базу данных"

    def handle(self, *args, **options):
        category, _ = Category.objects.get_or_create(title = "Фрукт")

        products = [
            {'title': 'Вишня', 'description':"Вишня — плодовое дерево или кустарник семейства розоцветных "
                                             "с мелкими сочными тёмно-красными плодами. "
                                             "Также вишней называют плод такого дерева или кустарника. ",
             "image": "Вишня.jpg", 'category_id': 8, 'purchase_price': 99.99}
        ]

        for product in products:
            prod, created = Product.objects.get_or_create(**product)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Успешно добавленный продукт: {prod.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Продукт уже существует: {prod.title}'))