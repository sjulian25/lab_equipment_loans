from .models import LabUser
from rest_framework import serializers

class LabUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabUser
        fields = '__all__'

class LabUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabUser
        fields = ['id', 'username', 'email', 'full_name', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if LabUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("El nombre de usuario ya está en uso.")
        return value

    def validate_email(self, value):
        if LabUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("El email ya está en uso.")
        return value    
    
    def validate_phone_number(self, value):
        if LabUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("El número de celular ya está en uso.")
        return value

    def create(self, validated_data):
        user = LabUser.objects.create_user(**validated_data)
        return user