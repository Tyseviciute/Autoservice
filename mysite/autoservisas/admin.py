from django.contrib import admin
from .models import AutoModel, Car, Order, OrderCar, Service

# Register your models here.

admin.site.register(AutoModel)
admin.site.register(Car)
admin.site.register(Order)
admin.site.register(Service)
admin.site.register(OrderCar)
