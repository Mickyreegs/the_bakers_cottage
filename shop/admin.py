from django.contrib import admin
from .models import Cake, SelectionBox

# Register your models here.

@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ("cake_type", "price")
    search_fields = ("cake_type",)


@admin.register(SelectionBox)
class SelectionBoxAdmin(admin.ModelAdmin):
    list_display = ("box_type", "price")
    search_fields = ("box_type",)

