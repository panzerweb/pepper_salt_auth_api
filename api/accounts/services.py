from .models import User
from django.conf import settings
from .utils import hash_password, verify_password

def register_user(email, password):
    return User.objects.create_user(email=email, password=password)
    
def login_user(email, password):
    try:
        user = User.objects.get(email=email)
        if verify_password(password, user.password):    
            print("Users found, logging in")
            return user
        return None
    except User.DoesNotExist:
        return None
    