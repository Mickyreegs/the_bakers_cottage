from django.contrib import admin
from .models import Review

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "comment", "rating", "created_at")
    search_fields = ("user__username", "comment")
    list_filter = ("rating", "created_at")
    ordering = ("-created_at",)


