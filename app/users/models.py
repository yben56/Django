from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin

class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    birthday = models.DateField(blank=False, null=False)
    gender = models.BooleanField(blank=False, null=False)
    username = models.CharField(max_length=30, null=True)
    is_active = models.BooleanField(default=False)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password', 'birthday', 'gender']