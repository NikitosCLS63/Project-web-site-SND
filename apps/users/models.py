# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.utils import timezone
class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=100)
    password_hash = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    reset_token = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)
    password_reset_expires = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'customers'


class Roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'roles'


class Users(models.Model):
    users_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customers, models.DO_NOTHING)
    role = models.ForeignKey(Roles, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users'


class Addresses(models.Model):
    address_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customers, models.DO_NOTHING)
    country = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    house = models.CharField(max_length=20, blank=True, null=True)
    apartment = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=10)
    full_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addresses'
        unique_together = (('customer', 'type'),)
