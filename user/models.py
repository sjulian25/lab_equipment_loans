from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser ):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('assistant', 'Assistant'),
        ('customer', 'Customer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username