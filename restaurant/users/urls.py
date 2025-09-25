from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PasswordResetView, PasswordResetConfirmView, UserRegisterView, UserLoginView, UserLogoutView, CurrentUserView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [

    # path for the user viewset
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),  # For browsable API login

    path('me/', CurrentUserView.as_view(), name='current-user'),

    # Separate auth endpoints - these will be under /api/users/auth/
    path("auth/register/", UserRegisterView.as_view(), name="register"),
    path("auth/login/", UserLoginView.as_view(), name="login"),
    path("auth/logout/", UserLogoutView.as_view(), name="logout"),

    # Password reset endpoints
    path("auth/password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path("auth/reset-password/<str:uidb64>/<str:token>/", 
         PasswordResetConfirmView.as_view(), 
         name="password_reset_confirm"),
]

