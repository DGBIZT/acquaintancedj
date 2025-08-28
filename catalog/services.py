from catalog.models import Product

def get_products_by_category(category_id: int):
    # Получаем все продукты указанной категории
    products = Product.objects.filter(category_id=category_id,
                                      is_active=True # Опционально: фильтрация по активности
                                      ).order_by('name') #Сортируем по названию
    return list(products)
