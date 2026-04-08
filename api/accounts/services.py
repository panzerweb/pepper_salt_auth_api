from .models import User
from django.conf import settings
from .utils import hash_password, verify_password
import base64

def register_user(username, password):
    return User.objects.create_user(username=username, password=password)
    

def login_user(username, password):
    try:
        user = User.objects.get(username=username)

        # Get user's current pepper
        user_pepper = settings.PEPPERS.get(user.pepper_version, b"").encode()

        # Verify password
        if verify_password(password, user.password, user.salt, pepper=user_pepper):

            # If Outdated then update it to the latest pepper used.
            if user.pepper_version < settings.LATEST_PEPPER_VERSION:
                new_version = settings.LATEST_PEPPER_VERSION
                new_pepper = settings.PEPPERS[new_version].encode()
                new_hash, new_salt = hash_password(password, salt=base64.b64decode(user.salt), pepper=new_pepper)

                user.password = new_hash
                user.salt = new_salt
                user.pepper_version = new_version
                user.save()

            return user

        return None
    except User.DoesNotExist:
        return None
    