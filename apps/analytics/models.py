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
class AnalyticsSnapshots(models.Model):
    snapshot_id = models.AutoField(primary_key=True)
    snapshot_type = models.CharField(max_length=50)
    snapshot_date = models.DateTimeField(blank=True, null=True)
    data = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'analytics_snapshots'


class AnalyticsMetrics(models.Model):
    metric_id = models.AutoField(primary_key=True)
    metric_name = models.CharField(max_length=100)
    metric_value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    calculated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'analytics_metrics'


class Reports(models.Model):
    report_id = models.AutoField(primary_key=True)
    report_name = models.CharField(max_length=100)
    report_type = models.CharField(max_length=50)
    created_by = models.ForeignKey(Customers, models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reports'


class ReportItems(models.Model):
    item_id = models.AutoField(primary_key=True)
    report = models.ForeignKey(Reports, models.DO_NOTHING, blank=True, null=True)
    entity_type = models.CharField(max_length=50, blank=True, null=True)
    entity_id = models.IntegerField(blank=True, null=True)
    product = models.ForeignKey(Products, models.DO_NOTHING, blank=True, null=True)
    metric_name = models.CharField(max_length=50, blank=True, null=True)
    metric_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    additional_info = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_items'


class AuditLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Customers, models.DO_NOTHING, blank=True, null=True)
    action_type = models.CharField(max_length=50)
    table_name = models.CharField(max_length=50)
    record_id = models.IntegerField(blank=True, null=True)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audit_log'


class BackupLogs(models.Model):
    backup_id = models.AutoField(primary_key=True)
    backup_date = models.DateTimeField(blank=True, null=True)
    initiated_by = models.ForeignKey(Customers, models.DO_NOTHING, db_column='initiated_by', blank=True, null=True)
    backup_type = models.CharField(max_length=50, blank=True, null=True)
    file_path = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'backup_logs'
