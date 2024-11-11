from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from loans.models import Loan
from user.models import LabUser    
from equipment.models import Equipment
from rest_framework_simplejwt.tokens import AccessToken

class LoanTests(APITestCase):
    def setUp(self):
        # Crear un usuario de prueba con un email
        self.user = LabUser.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        self.token = AccessToken.for_user(self.user)
        
        # Crear equipos de prueba con IDs únicos
        self.equipment1 = Equipment.objects.create(equipment_id='EQUIP1', name='Equipo 1', description='Descripción 1')
        self.equipment2 = Equipment.objects.create(equipment_id='EQUIP2', name='Equipo 2', description='Descripción 2')
        
        # Iniciar sesión con el usuario de prueba
        self.client.login(username='testuser', password='testpass')

    def test_create_loan(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        url = reverse('loan-create')
        data = {
            'user': self.user.id,
            'equipment': [self.equipment1.id, self.equipment2.id],
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 1)
        self.assertEqual(Loan.objects.get().user, self.user)

    def test_return_loan(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        # Crear un préstamo
        loan = Loan.objects.create(user=self.user)
        loan.equipment.set([self.equipment1, self.equipment2])  # Asignar equipos
        url = reverse('loan-return', args=[loan.id])
        
        # Datos para la devolución
        data = {
            'return_date': '2024-11-11T10:00:00Z',
            'is_active': False
        }
        
        # Realizar la solicitud PATCH para devolver el préstamo
        response = self.client.patch(url, data, format='json')
        
        # Verificar que la respuesta sea correcta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Recargar el objeto de préstamo desde la base de datos
        loan.refresh_from_db()
        
        # Verificar que la fecha de devolución y el estado activo se hayan actualizado
        self.assertIsNotNone(loan.return_date)
        self.assertFalse(loan.is_active)