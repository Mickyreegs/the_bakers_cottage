from django.contrib import admin
from .models import Cake, SelectionBox, Order, OrderItem


# Register your models here.
@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing Cake entries.
    """
    list_display = ("cake_type", "price")
    search_fields = ["cake_type"]


@admin.register(SelectionBox)
class SelectionBoxAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing SelectionBox entries.
    """
    list_display = ("box_type", "price")
    search_fields = ["box_type"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing customer orders.
    """
    list_display = (
        "user",
        "email",
        "total_price",
        "created_at",
        "pickup_time",
        "order_items_summary",
    )
    search_fields = ["email", "user__username"]

    def order_items_summary(self, obj):
        """
        Generates a summary of items in the order.
        Joins all items into a string.
        """
        return ", ".join(
            f"{item.quantity}x {item.name}"
            for item in obj.order_items.all()
        )

    order_items_summary.short_description = "Items Ordered"
