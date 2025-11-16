# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from apps.users.models import Customers, Roles, Users  
from apps.products.models import Brands, Categories
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    role_name = serializers.CharField(write_only=True, default='client')

    class Meta:
        model = Customers
        fields = ['first_name', 'last_name', 'email', 'password', 'phone', 'role_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        role_name = validated_data.pop('role_name', 'client')

        customer = Customers.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone=validated_data.get('phone'),
            password_hash=make_password(password)
        )

        role, _ = Roles.objects.get_or_create(role_name=role_name)
        Users.objects.create(customer=customer, role=role)

        return customer


# api/serializers.py (в LoginSerializer)
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']

        try:
            customer = Customers.objects.get(email=email)
        except Customers.DoesNotExist:
            raise serializers.ValidationError("Неверный email или пароль")

        if not check_password(password, customer.password_hash):
            raise serializers.ValidationError("Неверный email или пароль")

        try:
            role = Users.objects.get(customer=customer).role.role_name
        except Users.DoesNotExist:
            role = 'client'

        data['customer'] = customer
        data['role'] = role
        return data
    
    
    
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = ['brand_id', 'brand_name', 'logo_url']

class CategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.category_name', read_only=True)

    class Meta:
        model = Categories
        fields = ['category_id', 'category_name', 'description', 'parent', 'parent_name']
        
        
        
# api/serializers.py  (или в apps/users/serializers.py)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.users.models import Customers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавляем роль
        try:
            user_obj = user.users_set.first()  # Users -> customer (обратная связь)
            if user_obj and user_obj.role:
                token['role'] = user_obj.role.role_name
            else:
                token['role'] = 'client'
        except:
            token['role'] = 'client'

        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return token