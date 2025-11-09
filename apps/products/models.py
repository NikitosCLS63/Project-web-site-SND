# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    template = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'categories'


class Brands(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(unique=True, max_length=50)
    logo_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brands'


class Suppliers(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suppliers'



class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    sku = models.CharField(unique=True, max_length=50)
    product_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    brand = models.ForeignKey(Brands, models.DO_NOTHING, blank=True, null=True)
    supplier = models.ForeignKey(Suppliers, models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    specifications = models.JSONField(blank=True, null=True)
    row_version = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)  # одна главная картинка
    images = models.JSONField(blank=True, null=True)  # массив картинок JSONB
    
    
    class Meta:
        managed = False
        db_table = 'products'

class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, models.DO_NOTHING)
    quantity = models.IntegerField()
    warehouse_id = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventory'
