from django.contrib import admin
from .models import Booking, TeaPackage


# Register your models here.
@admin.register(TeaPackage)
class TeaPackageAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "tiers", "sweet_options", "savoury_options", "includes_prosecco")
    search_fields = ("name",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("customer", "guest_name", "guest_email", "package", "date", "time", "number_of_guests", "guests_with_special_requests", "special_requests", "status")
    search_fields = ("customer__username", "guest_name", "guest_email", "package__name")
    list_filter = ("date", "status", "package")
    ordering = ("date", "time")
    list_editable = ("status",)
    readonly_fields = ("created_at", "updated_at")


