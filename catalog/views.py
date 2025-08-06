from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Product


# Create your views here.

def submit_data(request):
    if request.method == "POST":
        return HttpResponse("Данные отправлены")

def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, "catalog/home.html", context=context)

def contacts(request):
    return render(request, "catalog/contacts.html")

def product_information(request):
    product = Product.objects.get(id=3)
    context = {
        "product_name": f'{product.title}',
        'product_description': f'{product.description}',
        'product_image': product.image , # передаем само поле image - product.image, а не его строковое представление f'{product.image}'
    }
    return render(request, "catalog/productinform.html", context=context)


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)

        if not product.image:
            print("Изображение не загружено")
        elif not product.image.storage.exists(product.image.name):
            print(f"Файл не существует по пути: {product.image.path}")
        print(f"Путь в БД: {product.image.name}")  # Должно быть photos/Buckwheat.jpg
        print(f"URL: {product.image.url}")  # Должно быть /media/photos/Buckwheat.jpg
        print(f"Физический путь: {product.image.path}")  # Полный путь к файлу
        print(f"Полный путь к файлу: {product.image.path}")
    except Product.DoesNotExist:
        product = None
    context = {
        "product": product,
    }
    return render(request, 'catalog/product_detail.html', context)


def index(request):
    return render(request, "catalog/index.html")


def base(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/base.html', context=context)