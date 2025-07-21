from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def submit_data(request):
    if request.method == "POST":
        return HttpResponse("Данные отправлены")

def home(request):
    return render(request, "catalog/home.html")

def contacts(request):
    return render(request, "catalog/contacts.html")
