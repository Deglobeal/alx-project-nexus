from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Fields to display in the admin list view
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email", "phone", "address")
    ordering = ("username",)

    # Fields to show in the admin detail/edit view
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email", "address", "phone")}),
        ("Roles & Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields to show when creating a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "role", "address", "phone", "password1", "password2", "is_staff", "is_active"),
        }),
    )
