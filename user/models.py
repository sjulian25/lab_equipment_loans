from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class LabUser(AbstractUser):
    email = models.EmailField(unique=True)  # Campo de correo electrónico único
    phone_number = models.CharField(unique=True, max_length=15, blank=True, null=True) # Campo único

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'Se creo el usuario {self.username}'