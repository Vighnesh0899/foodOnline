from django.contrib import admin
from .models import *

class OrderedFoodInline(admin.TabularInline):
    model = OrderedFood
    readonly_fields =('order', 'payment', 'user', 'fooditem', 'quantity', 'price', 'amount')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display =['order_number', 'name', 'phone', 'email', 'payment_method', 'status', 'is_ordered', 'order_place_to']
    inlines =[OrderedFoodInline]

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedFood)

