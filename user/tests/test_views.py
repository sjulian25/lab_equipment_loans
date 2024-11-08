from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class RegisterLabUserViewTests(APITestCase):
    def test_register_lab_user(self):
        url = reverse('register_user')  # Cambiado para coincidir con urls.py
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com',
            'full_name': 'Test User'
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['message'], "Se ha creado el usuario")

    def test_register_lab_user_invalid(self):
        url = reverse('register_user')  # Cambiado para coincidir con urls.py
        data = {
            'username': '',  # Campo vacío para probar la validación
            'password': 'testpassword',
            'email': 'testuser@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)