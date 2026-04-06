from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from .utils import hash_password

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=''):
        if not email:
            raise ValueError("Email is required")
        
        user = self.model(email=self.normalize_email(email))
        user.password = hash_password(password) 
        user.save()

        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)

    USERNAME_FIELD = 'email'

    objects = UserManager()