from django.contrib import admin
from .models import Restaurant, MenuCategory, MenuItem, SpecialOffer, Table


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "opening_hours", "closing_hours")
    search_fields = ("name", "phone", "email")
    list_filter = ("opening_hours", "closing_hours")


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name",)
    ordering = ("order",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available", "order")
    list_editable = ("price", "is_available", "order")
    list_filter = ("category", "is_available")
    search_fields = ("name", "description")


@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ("title", "menu_item", "discount_percentage", "start_date", "end_date", "is_active")
    list_filter = ("is_active", "start_date", "end_date")
    search_fields = ("title", "menu_item__name")


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "size", "is_available")
    list_editable = ("is_available",)
    list_filter = ("size", "is_available")
    search_fields = ("number",)
