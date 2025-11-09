from django.shortcuts import render

# Create your views here.
    
# apps/catalog/api/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.products.models import Brands, Categories, Products
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer
from apps.users.models import Users
import os
from django.conf import settings

class IsAdminUser(IsAuthenticated):
    def has_permission(self, request, view):
        try:
            return Users.objects.filter(
                customer_id=request.user.customer_id,
                role__role_name='admin'
            ).exists()
        except:
            return False

# === БРЕНДЫ ===
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brands.objects.all().order_by('brand_name')
    serializer_class = BrandSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        name = request.data.get('brand_name')
        if Brands.objects.filter(brand_name=name).exists():
            return Response({'error': 'Бренд с таким названием уже существует'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        name = request.data.get('brand_name')
        pk = kwargs.get('pk')
        if Brands.objects.filter(brand_name=name).exclude(brand_id=pk).exists():
            return Response({'error': 'Бренд с таким названием уже существует'}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().update(request, *args, **kwargs)

# === КАТЕГОРИИ ===
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.select_related('parent').all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    
    
    



from django.core.files.storage import default_storage
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        files = request.FILES.getlist('images')

        if not 3 <= len(files) <= 5:
            return Response({"error": "Нужно от 3 до 5 изображений"}, status=status.HTTP_400_BAD_REQUEST)

        image_urls = []
        for file in files:
            path = default_storage.save(f'products/{file.name}', file)
            image_urls.append(default_storage.url(path))

        data.setlist('images', image_urls)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        files = request.FILES.getlist('images')

        if files:
            if not 3 <= len(files) <= 5:
                return Response({"error": "Нужно от 3 до 5 изображений"}, status=status.HTTP_400_BAD_REQUEST)

            image_urls = []
            for file in files:
                path = default_storage.save(f'products/{file.name}', file)
                image_urls.append(default_storage.url(path))

            data.setlist('images', image_urls)

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)