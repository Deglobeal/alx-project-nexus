from rest_framework import serializers
from .models import Restaurant, MenuCategory, MenuItem, SpecialOffer, Table

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = MenuItem
        fields = [
            'id', 'category', 'category_name', 'name', 'description', 
            'price', 'image', 'is_available', 'order'
        ]

class SpecialOfferSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    
    class Meta:
        model = SpecialOffer
        fields = [
            'id', 'menu_item', 'menu_item_name', 'title', 'description',
            'discount_percentage', 'start_date', 'end_date', 'is_active'
        ]

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'