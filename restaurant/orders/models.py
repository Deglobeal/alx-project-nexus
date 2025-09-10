from django.db import models
from users.models import User
from restaurants.models import MenuItem
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import OrderItem  # forward reference for type hints


"""
Model for Order
- Linked to user who placed it
- Can have multiple items (OrderItems)
- Tracks total price, status, and timestamps
- Supports status updates and recalculates totals on item changes
"""

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id: int  # Explicit annotation for Pylance/Django stubs
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    if TYPE_CHECKING:
        order_items: models.Manager["OrderItem"]  # reverse relation type hint

    def __str__(self) -> str:
        return f'Order {self.id} by {self.user.username} - {self.status}'

    def update_total(self) -> None:
        """Recalculate and update the total price of the order."""
        total = Decimal('0.00')
        for order_item in self.order_items.all():
            total += order_item.price * order_item.quantity
        self.total_price = total
        self.save(update_fields=['total_price'])

    def update_status(self, new_status: str) -> None:
        """Update the order status if valid, else raise error."""
        if new_status in dict(self.STATUS_CHOICES).keys():
            self.status = new_status
            self.save(update_fields=['status'])
        else:
            raise ValueError('Invalid status')


"""
Model for OrderItem
- Links Order and MenuItem
- Tracks quantity and price at time of order
"""

class OrderItem(models.Model):
    id: int
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))

    def __str__(self) -> str:
        return f'{self.quantity} x {self.menu_item.name} in Order {self.order.id}'

    def save(self, *args, **kwargs) -> None:
        """Ensure price is set from menu_item if not provided."""
        if self.price == Decimal('0.00'):
            self.price = self.menu_item.price
        super().save(*args, **kwargs)


# === SIGNALS ===
@receiver(post_save, sender=OrderItem)
def update_order_total_on_save(sender, instance: OrderItem, **kwargs) -> None:
    instance.order.update_total()


@receiver(post_delete, sender=OrderItem)
def update_order_total_on_delete(sender, instance: OrderItem, **kwargs) -> None:
    instance.order.update_total()
