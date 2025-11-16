from rest_framework import serializers
from .models import Customers, Roles, Users, Addresses

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    # Публичный вид для списка пользователей, использует связанные поля customer и role
    email = serializers.CharField(source='customer.email', read_only=True)
    first_name = serializers.CharField(source='customer.first_name', read_only=True, default='-')
    last_name = serializers.CharField(source='customer.last_name', read_only=True, default='-')
    role_name = serializers.CharField(source='role.role_name', read_only=True, default='client')

    class Meta:
        model = Users
        fields = ('users_id', 'email', 'first_name', 'last_name', 'role_name')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = '__all__'


