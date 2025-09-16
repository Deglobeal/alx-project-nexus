from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PasswordResetView, PasswordResetConfirmView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),  # For browsable API login


    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    # Add this new pattern for password reset confirmation
    path("reset-password/<str:uidb64>/<str:token>/", 
         PasswordResetConfirmView.as_view(), 
         name="password_reset_confirm"),
]