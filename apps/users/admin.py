from django.contrib import admin
from .models import Customers, Roles, Users, Addresses

admin.site.register(Customers)
admin.site.register(Roles)
admin.site.register(Users)
admin.site.register(Addresses)