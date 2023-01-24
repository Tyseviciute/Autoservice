from django.contrib import admin
from .models import AutoModel, Car, Order, OrderCar, Service


# Register your models here.

# padaryti kad uzsakyme galima butu pamatyti ir uzsakomasinu pridejimas
class OrderCarInline(admin.TabularInline):
    model = OrderCar
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('car', 'date', 'status', 'owner', 'returne')
    inlines = [OrderCarInline]  # prijungimas uzsakymomasinos prie uzsakymo
    list_editable = ('date', 'status')


class CarAdmin(admin.ModelAdmin):
    list_display = ('client', 'valst_nr', 'vin_code')  # Kad butu rodomas ekranas su isvardintais pavadinimais stulepio pavidalu
    list_filter = ('client', 'automodel')  # filtras
    search_fields = ('valst_nr', 'vin_code')  # paieska pagal


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


admin.site.register(AutoModel)
admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(OrderCar)
