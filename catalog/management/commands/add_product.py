from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product
from django.db import connection
from django.utils import timezone

class Command(BaseCommand):
    help = "Добавление продукта с тестами в базу данных"

    def handle(self, *args, **options):
        category, _ = Category.objects.get_or_create(title = "Фрукт")

        products = [
            {'title': 'Красное яблоко', 'description':"Красное яблоко — это плод, "
                                             "который содержит антоцианы — пигменты, "
                                             "придающие плодам красный, синий или фиолетовый оттенок. ",
             "image": "photos/Apple_is_Red.jpg", 'category_id': 8, 'purchase_price': 86.59}
        ]

        for product in products:
            prod, created = Product.objects.get_or_create(**product)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Успешно добавленный продукт: {prod.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Продукт уже существует: {prod.title}'))