# C:\WebsiteDjSND\main\views.py
from django.shortcuts import render
from django.http import JsonResponse
from apps.users.decorators import require_role

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


# Админ-панель - доступна только для admin и employee
@require_role('admin', 'employee')
def admin_panel(request):
    return render(request, 'admin/admin_panel.html')


# Управление пользователями - только для admin
@require_role('admin')
def admin_users(request):
    return render(request, 'admin/users.html')