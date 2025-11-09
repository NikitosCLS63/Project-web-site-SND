from django.contrib import admin
from .models import AnalyticsSnapshots, AnalyticsMetrics, Reports, ReportItems, AuditLog, BackupLogs

admin.site.register(AnalyticsSnapshots)
admin.site.register(AnalyticsMetrics)
admin.site.register(Reports)
admin.site.register(ReportItems)
admin.site.register(AuditLog)
admin.site.register(BackupLogs)