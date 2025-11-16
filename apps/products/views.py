from django.shortcuts import render

# Create your views here.
    
# apps/catalog/api/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, BasePermission
from apps.products.models import Brands, Categories, Products
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer
from apps.users.models import Users
import os
from django.conf import settings

class IsAdminUser(BasePermission):
    """
    Allows access only to admin users for write operations.
    Read operations are allowed for everyone.
    """
    
    def has_permission(self, request, view):
        # Allow read operations for everyone
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
            
        # For write operations, check if user is admin
        try:
            # Получаем customer_id из объекта customer (если есть)
            customer_id = None
            if hasattr(request.user, 'customer') and request.user.customer:
                customer_id = request.user.customer.customer_id
            elif hasattr(request.user, 'customer_id'):
                customer_id = request.user.customer_id
            
            if not customer_id:
                return False
            
            return Users.objects.filter(
                customer_id=customer_id,
                role__role_name='admin'
            ).exists()
        except Exception as e:
            print(f"IsAdminUser error: {e}")
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
    
# === ПРОДУКТЫ ===
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # Разрешаем всем доступ к продуктам

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]  # Только админы могут создавать/редактировать/удалять
        else:
            permission_classes = [AllowAny]  # Все могут просматривать
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()