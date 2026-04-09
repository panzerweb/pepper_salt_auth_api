from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from .utils import hash_password
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, username, password=""):
        if not username:
            raise ValueError("Username is required")
        
        latest_version = settings.LATEST_PEPPER_VERSION
        pepper = settings.PEPPERS[latest_version].encode()

        hashed_password, salt = hash_password(password, pepper=pepper)
        user = self.model(
            username=username,
            password=hashed_password,
            salt=salt,
            pepper_version=latest_version
        )
        user.save()
        return user


class User(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=256)
    salt = models.CharField(max_length=32)
    pepper_version = models.IntegerField(default=1)

    USERNAME_FIELD = "username"
    objects = UserManager()