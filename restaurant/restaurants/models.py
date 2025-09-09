from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    opening_hours = models.CharField(max_length=100)
    closing_hours = models.CharField(max_length=100)
    image = models.ImageField(upload_to='restaurant/', blank=True, null=True)  

    def save (self, *args, **kwargs):
        # Custom save logic can be added here
        # Ensure only one restaurant instance exists

        if not self.pk and Restaurant.objects.exists():
            raise ValueError('Only one restaurant instance is allowed.')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
# model for Category
# define category name and description
# group menu items into categories like appetizers, main courses, desserts, beverages
# each category can have multiple menu items

class MenuCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Menu Categories'


    def __str__(self):
        return self.name




# model for Menu Item
# define item availability status
# list of items under each category
# price, description, image of each item
# 

class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, related_name='menu_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Menu Items'

    def __str__(self):
        return self.name
    


# model for Special Offers
# define special offers or discounts on certain menu items
# start and end date for each offer
# percentage or fixed amount discount


class SpecialOffer(models.Model):
    menu_item = models.ForeignKey(MenuItem, related_name='special_offers', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = 'Special Offers'

    def __str__(self):
        return f"{self.title} - {self.menu_item.name}"
    

class Table(models.Model):
    TABLE_SIZES_CHOICES = [
        (2, '2 seats'),
        (4, '4 seats'),
        (6, '6 seats'),
        (8, '8 seats'),
        (10, '10 seats'),
    ]


    number = models.PositiveIntegerField(unique=True)
    size = models.IntegerField(choices=TABLE_SIZES_CHOICES)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.number} - {self.size} seats"