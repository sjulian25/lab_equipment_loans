from django.db import models

# Create your models here.
class Equipment(models.Model):
    equipment_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True, null=True)
    aviable = models.BooleanField(default=False)

    def __str__(self):
        return self.name