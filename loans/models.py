from django.db import models
from equipment.models import Equipment
from user.models import LabUser


# Create your models here.
class Loan(models.Model):
    user = models.ForeignKey(LabUser, on_delete=models.CASCADE)
    equipment = models.ManyToManyField(Equipment)
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Se presto {self.equipment.name} a {self.user.get_full_name()} el {self.loan_date}'