from django.contrib import admin

# Register your models here.
from cartinfo.models import CartInfo ,Order
admin.site.register(CartInfo)
admin.site.register(Order)