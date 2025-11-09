# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from apps.users.models import Customers
from apps.products.models import Products

class Reviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, models.DO_NOTHING, blank=True, null=True)
    customer = models.ForeignKey(Customers, models.DO_NOTHING)
    rating = models.IntegerField()
    reviews_comment = models.TextField(blank=True, null=True)
    publication_date = models.DateTimeField()
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reviews'
