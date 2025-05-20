from django.contrib import admin
from .models import Cake, SelectionBox, Order, OrderItem

# Register your models here.

@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ("cake_type", "price")
    search_fields = ["cake_type",]


@admin.register(SelectionBox)
class SelectionBoxAdmin(admin.ModelAdmin):
    list_display = ("box_type", "price")
    search_fields = ["box_type",]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "email", "total_price", "pickup_time", "created_at")
    search_fields = ["email", "user__username"]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "cake", "box", "quantity")
    search_fields = ["order__user__username"]


