"""
URL configuration for restaurant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'orders': reverse('order-list', request=request, format=format),
        'reservations': reverse('reservation-list', request=request, format=format),
        'restaurants': reverse('restaurant-list', request=request, format=format),
        'reviews': reverse('review-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/orders/', include('orders.urls')),
    path('api/reservations/', include('reservations.urls')),
    path('api/restaurants/', include('restaurants.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/users/', include('users.urls')),


]