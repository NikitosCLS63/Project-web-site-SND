# apps/products/urls.py
from django.urls import path, include
from django.shortcuts import render
from rest_framework.routers import DefaultRouter
from api.views import BrandViewSet, CategoryViewSet, ProductViewSet 

# API
router = DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    # API
    path('api/', include(router.urls)),

    # Списки
    path('admin-panel/brands/', lambda r: render(r, 'admin/brands.html'), name='brands_list'),
    path('admin-panel/categories/', lambda r: render(r, 'admin/categories.html'), name='categories_list'),

    # Формы
    path('admin-panel/brand/add/', lambda r: render(r, 'admin/brand_form.html'), name='brand_add'),
    path('admin-panel/brand/edit/<int:pk>/', lambda r, pk: render(r, 'admin/brand_form.html', {'brand_id': pk}), name='brand_edit'),
    path('admin-panel/category/add/', lambda r: render(r, 'admin/category_form.html'), name='category_add'),
    path('admin-panel/category/edit/<int:pk>/', lambda r, pk: render(r, 'admin/category_form.html', {'category_id': pk}), name='category_edit'),
    
    #продукты 
      #СПИСОК ТОВАРОВ
    path('admin-panel/products/', lambda r: render(r, 'admin/product_list.html'), name='product_list'),

    # ДОБАВЛЕНИЕ ТОВАРА
    path('admin-panel/product/add/', lambda r: render(r, 'admin/product_form.html'), name='product_add'),

    #РЕДАКТИРОВАНИЕ ТОВАРА
    path('admin-panel/product/edit/<int:pk>/',
         lambda r, pk: render(r, 'admin/product_form.html', {'product_id': pk}),
         name='product_edit'),
]