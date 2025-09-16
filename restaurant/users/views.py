from django.contrib.auth import login, logout
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import update_session_auth_hash
from typing import Any, Dict
import logging
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str

from .serializers import (
    PasswordResetSerializer, 
    PasswordResetConfirmSerializer,
    UserSerializer, 
    UserRegisterSerializer, 
    UserLoginSerializer
)


logger = logging.getLogger(__name__)
User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get', 'post'])
    def register(self, request):
        if request.method == 'GET':
            return Response({"message": "Use POST to register a new user."})

        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user': UserSerializer(user).data,
                'message': 'User created successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
        if not isinstance(validated_data, dict) or 'user' not in validated_data:
            return Response({'error': 'Invalid login data'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = validated_data['user']
        login(request, user)
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Logged in successfully'
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

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