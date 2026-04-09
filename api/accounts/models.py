from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from .utils import hash_password
from django.conf import settings

# Custom manager for handling user creation logic
class UserManager(BaseUserManager):
    def create_user(self, username, password=""):
        # Ensure username is provided
        if not username:
            raise ValueError("Username is required")
        
        # Get the latest pepper version from settings
        latest_version = settings.LATEST_PEPPER_VERSION

        # Retrieve the pepper string using the version and encode it to bytes
        pepper = settings.PEPPERS[latest_version].encode()

        # Hash the password using custom hash function
        # Returns both hashed password and generated salt
        hashed_password, salt = hash_password(password, pepper=pepper)

        # Create user instance with hashed password, salt, and pepper version
        user = self.model(
            username=username,
            password=hashed_password,
            salt=salt,
            pepper_version=latest_version
        )

        # Save user to database
        user.save()

        # Return the created user instance
        return user


# Custom User model extending Django's AbstractBaseUser
class User(AbstractBaseUser):
    # Unique username field
    username = models.CharField(unique=True, max_length=150)

    # Stores the hashed password (NOT raw password)
    password = models.CharField(max_length=256)

    # Stores the salt used during hashing
    salt = models.CharField(max_length=32)

    # Tracks which pepper version was used (for future rotation support)
    pepper_version = models.IntegerField(default=1)

    # Field used by Django for authentication (login identifier)
    USERNAME_FIELD = "username"

    # Attach custom user manager
    objects = UserManager()