from rest_framework import viewsets
from .models import Equipment
from .serializers import EquipmentSerializer
from user.permissions import IsInGroup 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class EquipmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Llama a la implementación base para obtener los permisos
        permissions = super().get_permissions()
        
        # Si el método es POST, PUT o DELETE, agrega el permiso IsInGroup
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            permissions.append(IsInGroup(['admin']))
        
        return permissions
    
    def post(self, request, *args, **kwargs):

        serializer = EquipmentSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "equipment": serializer.data,
                "message": "Se ha creado el equipo"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, equipment_id, *args, **kwargs):

        try:
            equipment = Equipment.objects.get(equipment_id=equipment_id)
        except Equipment.DoesNotExist:
            return Response({"detail": "No existe el equipo."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EquipmentSerializer(equipment, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "equipment": serializer.data,
                "message": "Se ha actualizado el equipo"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        equipments = Equipment.objects.all()
        serializer = EquipmentSerializer(equipments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, equipment_id, *args, **kwargs):
        try:
            equipment = Equipment.objects.get(equipment_id=equipment_id)
            equipment.delete()
            return Response({"detail": "Equipo eliminado con éxito."}, status=status.HTTP_204_NO_CONTENT)
        except Equipment.DoesNotExist:
            return Response({"detail": "Equipo no encontrado."}, status=status.HTTP_404_NOT_FOUND)

