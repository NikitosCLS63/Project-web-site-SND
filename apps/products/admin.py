from django.contrib import admin
from .models import Categories, Brands, Suppliers, Products, Inventory

# ОСТАВЬ ТОЛЬКО @admin.register ДЛЯ ВСЕХ

@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'logo_url']
    search_fields = ['brand_name']
    list_editable = ['logo_url']
    ordering = ['brand_name']

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'parent']
    list_filter = ['parent']
    search_fields = ['category_name']
    ordering = ['category_name']


# ДОБАВЬ ДЛЯ ОСТАЛЬНЫХ (Suppliers, Products, Inventory)

@admin.register(Suppliers)
class SuppliersAdmin(admin.ModelAdmin):
    list_display = ['supplier_name', 'email', 'phone']
    search_fields = ['supplier_name', 'email']
    ordering = ['supplier_name']


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'brand', 'category', 'price']
    list_filter = ['brand', 'category']
    search_fields = ['product_name']
    ordering = ['product_name']


# apps/products/admin.py
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'warehouse_id', 'updated_at']
    list_filter = ['warehouse_id', 'updated_at']
    search_fields = ['product__product_name', 'product__sku']
    readonly_fields = ['updated_at']
    ordering = ['-updated_at']