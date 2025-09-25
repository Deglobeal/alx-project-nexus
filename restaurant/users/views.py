from django.contrib.auth import login, logout
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import update_session_auth_hash
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import logging
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from .models import User
from .serializers import (
    PasswordResetSerializer, 
    PasswordResetConfirmSerializer,
    UserSerializer, 
    UserRegisterSerializer, 
    UserLoginSerializer
)


logger = logging.getLogger(__name__)

# defining the UserViewSet
# handles user registration, login, logout
# and listing users

# UserViewSet
# handles user registration, login, logout, and listing users

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Password reset views
# handles password reset requests and confirmations
# PasswordResetView
# PasswordResetConfirmView

# Password reset views
class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        logger.info(f"Password reset request data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            logger.error(f"Password reset validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        reset_link = serializer.save()
        logger.info(f"Password reset link generated: {reset_link}")
        return Response({"reset_link": reset_link}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token):
        try:
            # Decode the user id
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        # Check if the token is valid
        if user is not None and default_token_generator.check_token(user, token):
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Set the new password
            user.set_password(serializer.validated_data['password'])
            user.save()
            
            # Update session if user is logged in
            if request.user.is_authenticated:
                update_session_auth_hash(request, user)
                
            return Response({"message": "Password has been reset successfully."}, 
                          status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid reset link"}, 
                          status=status.HTTP_400_BAD_REQUEST)       

# Authentication views - Only one set of register, login, logout
class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user).data,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        login(request, user)
        
        # Return JSON response to prevent redirect
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Logged in successfully'
        }, status=status.HTTP_200_OK)

class UserLogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)