from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'user', 'equipment', 'loan_date', 'return_date', 'is_active']
        read_only_fields = ['loan_date']