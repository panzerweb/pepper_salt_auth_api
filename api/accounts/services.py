from .models import User
from django.conf import settings
from .utils import hash_password, verify_password
import base64

# Service function for registering a new user
def register_user(username, password):
    # Delegates user creation to the custom manager (handles hashing, salt, pepper)
    return User.objects.create_user(username=username, password=password)
    

# Service function for logging in a user
def login_user(username, password):
    try:
        # Retrieve user by username
        user = User.objects.get(username=username)

        # Get the user's current pepper based on stored version
        # Default to empty bytes if version not found
        user_pepper = settings.PEPPERS.get(user.pepper_version, b"").encode()

        # Verify the provided password against stored hash
        if verify_password(password, user.password, user.salt, pepper=user_pepper):

            # If user's pepper version is outdated, upgrade it
            if user.pepper_version < settings.LATEST_PEPPER_VERSION:
                new_version = settings.LATEST_PEPPER_VERSION

                # Get the latest pepper value
                new_pepper = settings.PEPPERS[new_version].encode()

                # Re-hash the password using the new pepper and existing salt
                new_hash, new_salt = hash_password(
                    password,
                    salt=base64.b64decode(user.salt),  # Decode stored salt back to bytes
                    pepper=new_pepper
                )

                # Update user credentials with new hash, salt, and pepper version
                user.password = new_hash
                user.salt = new_salt
                user.pepper_version = new_version

                # Save updated user data
                user.save()

            # Return authenticated user
            return user

        # Return None if password verification fails
        return None

    except User.DoesNotExist:
        # Return None if user is not found
        return None