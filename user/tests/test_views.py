from django.urls import reverse
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from user.models import LabUser

class RegisterLabUserViewTests(APITestCase):

    def setUp(self):
        # Crear grupos
        self.admin_group = Group.objects.create(name='admin')
        self.user = LabUser.objects.create_user(username='testuser', password='testpass', email='testuser@mail.com')
        self.user.groups.add(self.admin_group)
        self.token = AccessToken.for_user(self.user)

    def test_register_lab_user_success(self):
        url = reverse('register_user')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        data = {
            'username': 'testuser_unique',
            'password': 'testpassword',
            'email': 'testuser@example.com',
            'full_name': 'Test User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['message'], "Se ha creado el usuario")

    def test_register_lab_user_invalid(self):
        url = reverse('register_user') 
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        data = {
            'username': '',  # Campo vacío para probar la validación
            'password': 'testpassword',
            'email': 'testuser@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_register_lab_user_without_authentication(self):
        url = reverse('register_user')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com',
            'full_name': 'Test User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_lab_user_without_group(self):
        non_admin_user = LabUser.objects.create_user(username='nonadmin', password='testpass', email='noadmin@mail.com')
        token = AccessToken.for_user(non_admin_user)
        url = reverse('register_user')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token))
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com',
            'full_name': 'Test User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)