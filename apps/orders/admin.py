from django.contrib import admin
from .models import Orders, OrderItems, Shipments, ProductReturns, Payments

admin.site.register(Orders)
admin.site.register(OrderItems)
admin.site.register(Shipments)
admin.site.register(ProductReturns)
admin.site.register(Payments)