from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline display of OrderItems inside an Order."""
    model = OrderItem
    extra = 1
    fields = ('menu_item', 'quantity', 'price')
    readonly_fields = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    ordering = ('-created_at',)
    inlines = [OrderItemInline]

    fieldsets = (
        (None, {
            'fields': ('user', 'status', 'total_price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('total_price', 'created_at', 'updated_at')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'menu_item', 'quantity', 'price')
    list_filter = ('menu_item',)
    search_fields = ('order__id', 'menu_item__name')
    ordering = ('order',)
