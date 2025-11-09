# C:\WebsiteDjSND\main\views.py
from django.shortcuts import render

def home(request):
    brands = ['Brand1', 'Brand2', 'Brand3', 'Brand4']  # Заглушка для брендов
    context = {'brands': brands}
    return render(request, 'home.html', context)

def catalog(request):
    return render(request, 'catalog.html')  # Заглушка

def promotions(request):
    return render(request, 'promotions.html')  # Заглушка

def register(request):
    return render(request, 'register.html')  # Заглушка

def login(request):
    return render(request, 'login.html')  # Заглушка