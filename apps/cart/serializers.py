from rest_framework import serializers
from .models import Carts, CartItems, Wishlists


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlists
        fields = '__all__'
