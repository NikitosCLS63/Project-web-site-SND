




from django.db import models
from apps.users.models import Customers
from apps.products.models import Products



class Carts(models.Model):
    cart_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customers, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'carts'


class CartItems(models.Model):
    item_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Carts, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cart_items'


class Wishlists(models.Model):
    wishlist_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customers, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wishlists'
