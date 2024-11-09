from .models import LabUser
from .serializers import LabUserSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsInGroup
from rest_framework.response import Response
from rest_framework.views import APIView

class RegisterLabUserView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Llama a la implementación base para obtener los permisos
        permissions = super().get_permissions()
        
        # Agrega el permiso IsInGroup con el grupo 'admin'
        permissions.append(IsInGroup(['admin']))
        
        return permissions

    def post(self, request, *args, **kwargs):
        # Verifica primero si es un admin
        # if not IsInGroup(['admin']).has_permission(request, self):
        #     return Response({"detail": "No tiene permiso para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)

        serializer = LabUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": serializer.data,
                "message": "Se ha creado el usuario"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
class LabUserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not IsInGroup(['admin', 'lab_assistant']).has_permission(request, self):
            return Response({"detail": "No tiene permiso para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)
        
        users = LabUser.objects.all()
        serializer = LabUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LabUserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, username, *args, **kwargs):
        if not IsInGroup(['admin']).has_permission(request, self):
            return Response({"detail": "No tiene permiso para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = LabUser.objects.get(username=username)
        except LabUser.DoesNotExist:
            return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = LabUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "user": serializer.data,
                "message": "Usuario actualizado con éxito."
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LabUserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, username, *args, **kwargs):
        try:
            user = LabUser.objects.get(username=username)
            user.delete()
            return Response({"detail": "Usuario eliminado con éxito."}, status=status.HTTP_204_NO_CONTENT)
        except LabUser.DoesNotExist:
            return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)