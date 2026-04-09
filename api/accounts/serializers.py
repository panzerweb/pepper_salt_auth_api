from rest_framework import serializers
from .models import User


# Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        # Link serializer to the custom User model
        model = User

        # Fields required for registration
        fields = ("username", "password")

    # Custom validation to ensure username is unique
    def validate_username(self, value):
        # Check if a user with the same username already exists
        if User.objects.filter(username=value).exists():
            # Raise validation error if username is already taken
            raise serializers.ValidationError("Username already used by other user.")
        
        # Return validated username if no duplicates found
        return value


# Serializer for user login (no model binding, just input validation)
class LoginSerializer(serializers.Serializer):
    # Field for username input
    username = serializers.CharField()

    # Field for password input
    password = serializers.CharField()