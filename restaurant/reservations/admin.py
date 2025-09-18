from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'table',
        'reservation_time',
        'party_size',
        'status',
        'created_at',
    )
    list_filter = ('status', 'reservation_time', 'table')
    search_fields = ('user__username', 'special_requests')
    ordering = ('-reservation_time',)
    date_hierarchy = 'reservation_time'
