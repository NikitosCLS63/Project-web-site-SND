from rest_framework import serializers
from .models import Orders, OrderItems, Payments, Shipments, ProductReturns


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipments
        fields = '__all__'


class ProductReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReturns
        fields = '__all__'
