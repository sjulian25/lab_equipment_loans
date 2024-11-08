from .serializers import LabUserSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsInGroup
from rest_framework.response import Response
from rest_framework.views import APIView

class RegisterLabUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Verifica primero si es un admin
        if not IsInGroup(['admin']).has_permission(request, self):
            return Response({"detail": "No tiene permiso para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)

        serializer = LabUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": serializer.data,
                "message": "Se ha creado el usuario"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)