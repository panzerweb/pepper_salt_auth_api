from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

def hash_password(password: str) -> str:
    pepper = settings.PEPPER or ""
    return make_password(password + pepper)

def verify_password(password:str, hashed_password:str) -> bool:
    pepper = settings.PEPPER or ""
    return check_password(password + pepper, hashed_password)