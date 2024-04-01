from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator, MaxValueValidator, MinValueValidator

class Item(models.Model):
    name = models.CharField(max_length=200, null=False)
    created = models.DateField(auto_now_add=True)

    #models.CharField(max_length=200)
    #models.TextField()
    #models.DateField(auto_now_add=True)
    #models.EmailField(unique=True)
    #models.BooleanField(null=False)
