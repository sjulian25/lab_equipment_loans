from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

# Create your models here.
class LabUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('El nombre de usuario debe ser proporcionado')
        if not email:
            raise ValueError('El email debe ser proporcionado')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Asegúrate de almacenar la contraseña de forma segura
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


class LabUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(unique=True, max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = LabUserManager()

    USERNAME_FIELD = 'username'  # El campo que se usará para la autenticación
    REQUIRED_FIELDS = ['email']  # Campos requeridos al crear un superusuario

    def __str__(self):
        return f'Se creó el usuario {self.username}'