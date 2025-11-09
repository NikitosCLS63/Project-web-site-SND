from rest_framework import serializers
from .models import (
    AuditLog,
    Reports,
    ReportItems,
    AnalyticsSnapshots,
    AnalyticsMetrics,
    BackupLogs
)
from apps.users.serializers import CustomerSerializer

class AuditLogSerializer(serializers.ModelSerializer):
    user = CustomerSerializer(read_only=True)

    class Meta:
        model = AuditLog
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    created_by = CustomerSerializer(read_only=True)

    class Meta:
        model = Reports
        fields = '__all__'


class ReportItemSerializer(serializers.ModelSerializer):
    report = ReportSerializer(read_only=True)

    class Meta:
        model = ReportItems
        fields = '__all__'


class AnalyticsSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsSnapshots
        fields = '__all__'


class AnalyticsMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsMetrics
        fields = '__all__'


class BackupLogSerializer(serializers.ModelSerializer):
    initiated_by = CustomerSerializer(read_only=True)

    class Meta:
        model = BackupLogs
        fields = '__all__'
