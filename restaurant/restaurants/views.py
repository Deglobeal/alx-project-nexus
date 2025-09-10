from rest_framework import viewsets
from .models import Restaurant, MenuCategory, MenuItem, SpecialOffer, Table
from .serializers import (
    RestaurantSerializer, 
    MenuCategorySerializer, 
    MenuItemSerializer, 
    SpecialOfferSerializer, 
    TableSerializer
)

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class MenuCategoryViewSet(viewsets.ModelViewSet):
    queryset = MenuCategory.objects.filter(is_active=True)
    serializer_class = MenuCategorySerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.filter(is_available=True)
    serializer_class = MenuItemSerializer

class SpecialOfferViewSet(viewsets.ModelViewSet):
    queryset = SpecialOffer.objects.filter(is_active=True)
    serializer_class = SpecialOfferSerializer

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.filter(is_available=True)
    serializer_class = TableSerializer