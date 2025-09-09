from django.db import models
from users.models import User
from restaurants.models import MenuItem
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal

# Create your models here.

"""
# model for Order
# link order to user who placed it
# multiple items in an order with quantity and price
# total price, status, timestamps
# order can have multiple items
# status can be pending, preparing, delivered, cancelled
# timestamps for created and updated
# calculate total price based on items and their quantities
# method to update order status
# string representation of the order
# order history for users
# order can be linked to a reservation since a user can reserve a table and place an order
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
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username} - {self.status}'  
     
    # method to calculate total price
    # sum of (item price * quantity) for all items in the order
    # update total_price field
    def update_total(self):
        total = Decimal('0.00')
        for order_item in self.order_items.all():
            total += order_item.price * order_item.quantity
        self.total_price = total
        self.save(update_fields=['total_price'])

    # method to update order status
    # validate new status
    # update status and updated_at timestamp
    # save changes
    def update_status(self, new_status):
        if new_status in dict(self.STATUS_CHOICES).keys():
            self.status = new_status
            self.save()
        else:
            raise ValueError('Invalid status')

# model for OrderItem to link Order and MenuItem with quantity
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f'{self.quantity} x {self.menu_item.name} in Order {self.order.id}'
    
    def save(self, *args, **kwargs):
        # Set price from menu_item if not already set
        if self.price == Decimal('0.00'):
            self.price = self.menu_item.price
        super().save(*args, **kwargs)


# signal to update order total when an OrderItem is saved or deleted
@receiver(post_save, sender=OrderItem)
def update_order_total_on_save(sender, instance, **kwargs):
    instance.order.update_total()

@receiver(post_delete, sender=OrderItem)
def update_order_total_on_delete(sender, instance, **kwargs):
    instance.order.update_total()