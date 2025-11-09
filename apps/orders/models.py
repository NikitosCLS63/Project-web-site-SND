# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from apps.users.models import Customers, Addresses
from apps.products.models import Products


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customers, models.DO_NOTHING)
    order_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=20, blank=True, null=True)
    payment_status = models.CharField(max_length=20, blank=True, null=True)
    shipping_address = models.ForeignKey(Addresses, models.DO_NOTHING, blank=True, null=True)
    tracking_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class OrderItems(models.Model):
    item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, models.DO_NOTHING)
    product = models.ForeignKey(Products, models.DO_NOTHING)
    quantity = models.IntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'order_items'


class Shipments(models.Model):
    shipment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, models.DO_NOTHING)
    shipment_date = models.DateTimeField(blank=True, null=True)
    shipping_address = models.ForeignKey(Addresses, models.DO_NOTHING, blank=True, null=True)
    tracking = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shipments'


class ProductReturns(models.Model):
    product_return_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, models.DO_NOTHING)
    item = models.ForeignKey(OrderItems, models.DO_NOTHING)
    reason = models.TextField()
    return_date = models.DateTimeField()
    status = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_returns'


class Payments(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.OneToOneField(Orders, models.DO_NOTHING)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payments'
