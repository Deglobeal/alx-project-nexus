from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    table_number = serializers.IntegerField(source='table.number', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'user', 'user_name', 'table', 'table_number', 
            'reservation_time', 'party_size', 
            'status', 'special_requests', 'created_at'
        ]