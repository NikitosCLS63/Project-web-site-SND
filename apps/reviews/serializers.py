from rest_framework import serializers
from .models import Reviews
from apps.products.serializers import ProductSerializer
from apps.users.serializers import CustomerSerializer

class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Reviews
        fields = '__all__'
