from django.db import models
from users.models import User
from restaurants.models import Table

# Create your models here.
# Model for Reservation
# link reservation to user and table
# reservation time, date, party size
# status can be pending, confirmed, seated, completed, cancelled, no_show

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('seated', 'Seated'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    reservation_time = models.DateTimeField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    party_size = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # ensure a table cannot be double-booked for the same date and time
    class Meta:
        unique_together = ['table', 'date', 'time']
    
    # string representation of the reservation
    def __str__(self):
        return f"Reservation for {self.party_size} on {self.date} at {self.time}"