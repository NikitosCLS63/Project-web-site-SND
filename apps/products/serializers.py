from rest_framework import serializers
from .models import Categories, Brands, Suppliers, Products
import os
from django.conf import settings


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(write_only=True, required=False)  # Принимаем файл
    class Meta:
        model = Brands
        fields = ['brand_id', 'brand_name', 'logo', 'logo_url']  # УБРАЛ logo_url
    def create(self, validated_data):
        logo_file = validated_data.pop('logo', None)
        brand = Brands(**validated_data)
        brand.save()  # Сначала сохраняем без файла

        if logo_file:
            # Путь: media/brands/название_файла.jpg
            filename = logo_file.name
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'brands')
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, filename)

            # Сохраняем файл
            with open(file_path, 'wb+') as f:
                for chunk in logo_file.chunks():
                    f.write(chunk)

            # Записываем путь в logo_url
            brand.logo_url = f'{settings.MEDIA_URL}brands/{filename}'
            brand.save()

        return brand

    def update(self, instance, validated_data):
        logo_file = validated_data.pop('logo', None)

        instance.brand_name = validated_data.get('brand_name', instance.brand_name)

        if logo_file:
            # Удаляем старый файл (по желанию)
            if instance.logo_url:
                old_path = instance.logo_url.replace(settings.MEDIA_URL, '')
                old_full_path = os.path.join(settings.MEDIA_ROOT, old_path)
                if os.path.exists(old_full_path):
                    os.remove(old_full_path)

            # Сохраняем новый
            filename = logo_file.name
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'brands')
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, filename)

            with open(file_path, 'wb+') as f:
                for chunk in logo_file.chunks():
                    f.write(chunk)

            instance.logo_url = f'{settings.MEDIA_URL}brands/{filename}'

        instance.save()
        return instance
        

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.FileField(write_only=True, required=False)  # ФАЙЛ С КОМПА

    category_id = serializers.IntegerField(write_only=True, required=False)
    brand_id = serializers.IntegerField(write_only=True, required=False)
    supplier_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Products
        fields = [
            'product_id', 'sku', 'product_name', 'description', 'price',
            'stock_quantity', 'image_url', 'status', 'specifications',
            'category_id', 'brand_id', 'supplier_id', 'image'
        ]
        extra_kwargs = {
            'image_url': {'read_only': True},
        }

    
    def validate_images(self, value):
        if not 3 <= len(value) <= 5:
            raise serializers.ValidationError("Нужно от 3 до 5 изображений")
        return value
    
    
    def create(self, validated_data):
        image_file = validated_data.pop('image', None)
        category_id = validated_data.pop('category_id', None)
        brand_id = validated_data.pop('brand_id', None)
        supplier_id = validated_data.pop('supplier_id', None)

        # Создаём продукт
        product = Products(**validated_data)

        if category_id:
            product.category = Categories.objects.get(category_id=category_id)
        if brand_id:
            product.brand = Brands.objects.get(brand_id=brand_id)
        if supplier_id:
            product.supplier = Suppliers.objects.get(supplier_id=supplier_id)

        product.save()

        # Загрузка фото
        if image_file:
            filename = image_file.name
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'products')
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, filename)

            with open(file_path, 'wb+') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)

            product.image_url = f'{settings.MEDIA_URL}products/{filename}'
            product.save()

        return product

    def update(self, instance, validated_data):
        image_file = validated_data.pop('image', None)
        category_id = validated_data.pop('category_id', None)
        brand_id = validated_data.pop('brand_id', None)
        supplier_id = validated_data.pop('supplier_id', None)

        instance.sku = validated_data.get('sku', instance.sku)
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.stock_quantity = validated_data.get('stock_quantity', instance.stock_quantity)
        instance.status = validated_data.get('status', instance.status)
        instance.specifications = validated_data.get('specifications', instance.specifications)

        if category_id:
            instance.category = Categories.objects.get(category_id=category_id)
        if brand_id:
            instance.brand = Brands.objects.get(brand_id=brand_id)
        if supplier_id:
            instance.supplier = Suppliers.objects.get(supplier_id=supplier_id)

        if image_file:
            # Удаляем старое фото
            if instance.image_url:
                old_path = instance.image_url.replace(settings.MEDIA_URL, '')
                old_full_path = os.path.join(settings.MEDIA_ROOT, old_path)
                if os.path.exists(old_full_path):
                    os.remove(old_full_path)

            # Сохраняем новое
            filename = image_file.name
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'products')
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, filename)

            with open(file_path, 'wb+') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)

            instance.image_url = f'{settings.MEDIA_URL}products/{filename}'

        instance.save()
        return instance



