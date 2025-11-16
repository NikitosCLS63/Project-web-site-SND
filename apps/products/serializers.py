from rest_framework import serializers
from .models import Categories, Brands, Suppliers, Products
import os
import json
import time
from django.conf import settings
from apps.reviews.models import Reviews
from django.db.models import Avg


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
    images = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    image_files = serializers.ListField(
        child=serializers.FileField(),
        required=False,
        write_only=True
    )

    brand_name = serializers.SerializerMethodField(read_only=True)
    brand_logo_url = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)
    template = serializers.SerializerMethodField(read_only=True)

    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    brand_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    supplier_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Products
        fields = [
            'product_id', 'sku', 'product_name', 'description', 'price',
            'stock_quantity', 'image_url', 'status', 'specifications',
            'category_id', 'brand_id', 'supplier_id', 'images', 'image_files',
            'brand_name', 'brand_logo_url', 'rating', 'category_name', 'template'
        ]
        extra_kwargs = {'image_url': {'read_only': True}}

    def _save_product_images(self, image_files, existing_urls):
        """Save uploaded image files and combine with existing URLs. Max 5 images total."""
        saved_urls = []
        
        # Clean existing URLs first
        if existing_urls:
            if isinstance(existing_urls, str):
                try:
                    parsed = json.loads(existing_urls)
                    existing_urls = parsed if isinstance(parsed, list) else [existing_urls]
                except:
                    existing_urls = [existing_urls]
            
            if isinstance(existing_urls, list):
                # Use the same cleaning logic as to_representation
                cleaned = self._flatten_and_clean_images(existing_urls)
                saved_urls.extend(cleaned[:5])
        
        # Add new uploaded files (up to 5 total)
        if image_files:
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'products')
            os.makedirs(upload_dir, exist_ok=True)
            
            remaining_slots = 5 - len(saved_urls)
            for image_file in image_files[:remaining_slots]:
                filename = f"{int(time.time())}_{image_file.name}"
                file_path = os.path.join(upload_dir, filename)
                
                with open(file_path, 'wb+') as f:
                    for chunk in image_file.chunks():
                        f.write(chunk)
                
                saved_urls.append(f'{settings.MEDIA_URL}products/{filename}')
        
        return saved_urls[:5]  # Ensure max 5 images

    def get_brand_name(self, obj):
        try:
            return obj.brand.brand_name if obj.brand else None
        except Exception:
            return None

    def get_brand_logo_url(self, obj):
        try:
            return obj.brand.logo_url if obj.brand else None
        except Exception:
            return None

    def get_rating(self, obj):
        try:
            agg = Reviews.objects.filter(product=obj).aggregate(avg=Avg('rating'))
            if agg and agg.get('avg') is not None:
                return round(float(agg.get('avg')), 1)
            return None
        except Exception:
            return None

    def get_category_name(self, obj):
        try:
            return obj.category.category_name if obj.category else None
        except Exception:
            return None

    def get_template(self, obj):
        try:
            return obj.category.template if obj.category else None
        except Exception:
            return None

    def to_representation(self, instance):
        """Ensure images field is always a clean list of URLs"""
        ret = super().to_representation(instance)
        
        # Clean up images field - recursively parse and flatten all URLs
        if 'images' in ret and ret['images']:
            images_data = ret['images']
            clean_images = self._flatten_and_clean_images(images_data)
            ret['images'] = clean_images if clean_images else []
        else:
            ret['images'] = []
        
        return ret

    def _flatten_and_clean_images(self, data, depth=0):
        """Recursively flatten and clean image URLs from nested JSON structures"""
        if depth > 5:  # Prevent infinite recursion
            return []
        
        result = []
        
        if isinstance(data, str):
            # Try to parse as JSON
            data_str = data.strip()
            if data_str.startswith('[') or data_str.startswith('"'):
                try:
                    parsed = json.loads(data_str)
                    return self._flatten_and_clean_images(parsed, depth + 1)
                except:
                    # Not valid JSON, treat as URL if not blob
                    if not data_str.startswith('blob:'):
                        result.append(data_str)
            elif not data_str.startswith('blob:') and data_str:
                result.append(data_str)
        
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, str):
                    item_str = item.strip()
                    # Skip blob URLs
                    if item_str.startswith('blob:'):
                        continue
                    # Try to parse nested JSON
                    if item_str.startswith('[') or item_str.startswith('"'):
                        try:
                            parsed = json.loads(item_str)
                            result.extend(self._flatten_and_clean_images(parsed, depth + 1))
                            continue
                        except:
                            pass
                    # Add as URL if valid
                    if item_str and not item_str.startswith('blob:'):
                        result.append(item_str)
                elif isinstance(item, list):
                    result.extend(self._flatten_and_clean_images(item, depth + 1))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_result = []
        for url in result:
            if url not in seen:
                seen.add(url)
                unique_result.append(url)
        
        return unique_result

    def create(self, validated_data):
        image_files = validated_data.pop('image_files', [])
        images = validated_data.pop('images', [])
        category_id = validated_data.pop('category_id', None)
        brand_id = validated_data.pop('brand_id', None)
        supplier_id = validated_data.pop('supplier_id', None)

        product = Products(**validated_data)

        if category_id:
            product.category_id = int(category_id) if isinstance(category_id, str) else category_id
        if brand_id:
            product.brand_id = int(brand_id) if isinstance(brand_id, str) else brand_id
        if supplier_id:
            product.supplier_id = int(supplier_id) if isinstance(supplier_id, str) else supplier_id

        # Save uploaded images and combine with any URLs
        saved_images = self._save_product_images(image_files, images)
        product.images = saved_images if saved_images else None
        product.save()
        return product

    def update(self, instance, validated_data):
        image_files = validated_data.pop('image_files', [])
        images = validated_data.pop('images', None)
        category_id = validated_data.pop('category_id', None)
        brand_id = validated_data.pop('brand_id', None)
        supplier_id = validated_data.pop('supplier_id', None)
        
        instance.sku = validated_data.get('sku', instance.sku)
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.description = validated_data.get('description', instance.description)
        
        # Обрабатываем цену (может прийти как строка из FormData)
        price = validated_data.get('price', instance.price)
        if price is not None:
            try:
                instance.price = float(price)
            except (ValueError, TypeError):
                instance.price = instance.price
        
        # Обрабатываем stock_quantity
        stock = validated_data.get('stock_quantity', instance.stock_quantity)
        if stock is not None:
            try:
                instance.stock_quantity = int(stock) if stock else 0
            except (ValueError, TypeError):
                instance.stock_quantity = instance.stock_quantity
        
        instance.status = validated_data.get('status', instance.status)
        instance.specifications = validated_data.get('specifications', instance.specifications)

        if category_id is not None:
            instance.category_id = int(category_id) if isinstance(category_id, str) and category_id else category_id
        if brand_id is not None:
            instance.brand_id = int(brand_id) if isinstance(brand_id, str) and brand_id else brand_id
        if supplier_id is not None:
            instance.supplier_id = int(supplier_id) if isinstance(supplier_id, str) and supplier_id else supplier_id

        # Handle images: combine existing URLs with newly uploaded files
        if images is not None or image_files:
            existing_urls = images if isinstance(images, list) else []
            saved_images = self._save_product_images(image_files, existing_urls)
            instance.images = saved_images if saved_images else None
        elif images == []:  # If explicitly set to empty array, clear images
            instance.images = []

        instance.save()
        return instance
