from django.contrib import admin
from .models import Carts, CartItems, Wishlists

admin.site.register(Carts)
admin.site.register(CartItems)
admin.site.register(Wishlists)