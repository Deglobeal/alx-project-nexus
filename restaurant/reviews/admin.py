from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "rating", "comment", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("user__username", "comment")
    ordering = ("-created_at",)
