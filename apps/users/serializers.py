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

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = '__all__'
        