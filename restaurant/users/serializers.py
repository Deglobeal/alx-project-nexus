
from rest_framework import serializers
from django.contrib.auth import authenticate
import re
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.db import IntegrityError
from .models import User


# serializers for User model and authentication
# including registration, login, password reset, and password reset confirmation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'role', 'username', 'email', 'first_name',
            'last_name', 'date_joined', 'address', 'phone', 'password'
        ]

        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
        }

# New serializer for user registration with enhanced password validation
# and password confirmation
# Also includes address and phone fields 

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password', 'password2', 'address', 'phone'
        ]

    def validate(self, attrs):
        # Check if email already exists
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        password = attrs['password']
        username = attrs['username']

        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if username.lower() in password.lower():
            raise serializers.ValidationError("Password is too similar to the username.")
        if password.isdigit():
            raise serializers.ValidationError("Password cannot be entirely numeric.")
        if password.lower() in ['password', '12345678', 'qwerty', 'abc123']:
            raise serializers.ValidationError("Password is too common.")
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise serializers.ValidationError("Password must contain at least one special character.")

        return attrs

# Create method to handle user creation with hashed password
# and removal of password2 from validated data
# Also saves address and phone fields

    def create(self, validated_data):
        validated_data.pop('password2')
        raw_password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(raw_password)
        try:
            user.save()
        except IntegrityError as e:
            if 'email' in str(e).lower():
                raise serializers.ValidationError({"email": "A user with this email already exists."})
            raise
        return user

# Serializer for user login
# Validates username and password
# Authenticates user and checks if active
# Returns user object on successful validation

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Unable to log in with provided credentials.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        attrs['user'] = user
        return attrs
    
# New serializers for password reset and confirmation
# including email validation and password strength checks
# also handles token generation and user retrieval

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            # Now that emails are unique, we can safely use get()
            user = User.objects.get(email=value)
            # Store the user instance in the serializer context
            self.context['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError("No user with this email address.")
        return value

    def save(self, **kwargs):
        # Get the user from context
        user = self.context.get('user')
        if not user:
            raise serializers.ValidationError("User not found.")
            
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://localhost:8000/api/users/auth/reset-password/{uid}/{token}/"
        # In production, send via email
        return reset_link

# Serializer for confirming password reset
# with password validation and setting new password
# also checks token validity and user existence

class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        password = attrs['password']
        
        # Reuse the same password validation as in UserRegisterSerializer
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if password.isdigit():
            raise serializers.ValidationError("Password cannot be entirely numeric.")
        if password.lower() in ['password', '12345678', 'qwerty', 'abc123']:
            raise serializers.ValidationError("Password is too common.")
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise serializers.ValidationError("Password must contain at least one special character.")

        return attrs