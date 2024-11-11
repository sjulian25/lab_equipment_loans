from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from equipment.models import Equipment
from django.contrib.auth.models import Group
from user.models import LabUser
from rest_framework_simplejwt.tokens import AccessToken

class EquipmentViewTests(APITestCase):

    def setUp(self):
        # Crear un grupo 'admin'
        self.admin_group, _ = Group.objects.get_or_create(name='admin')

        # Crear un usuario que será parte del grupo 'admin'
        self.admin_user = LabUser.objects.create_user(username='adminuser', email='adminuser@mail.com', password='adminpass')
        self.admin_user.groups.add(self.admin_group)  # Agregar al grupo 'admin'
        self.admin_user.save()
        self.admin_token = AccessToken.for_user(self.admin_user)

        # Crear un usuario que NO será parte del grupo 'admin'
        self.non_admin_user = LabUser.objects.create_user(username='nonadminuser', email='noadminuser@mail.com', password='nonadminpass')
        self.non_admin_token = AccessToken.for_user(self.non_admin_user)

        # Crear un equipo para las pruebas
        self.equipment = Equipment.objects.create(equipment_id='EQUIP001', name='Test Equipment', description='Test Description')

        # URL de la vista
        self.url = reverse('equipment-list')  # Asegúrate de que esta URL esté definida en tus rutas
        self.equipment_url = reverse('equipment-detail', args=[self.equipment.equipment_id])  # URL para el detalle del equipo

    def test_create_equipment_as_admin(self):
        # Autenticarse como el usuario admin
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.admin_token))

        data = {
            'equipment_id': 'EQUIP002',
            'name': 'New Equipment',
            'description': 'New Description'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Equipment.objects.count(), 2)  # Debería haber dos equipos ahora

    def test_create_equipment_as_non_admin(self):
        # Autenticarse como el usuario no admin
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.non_admin_token))

        data = {
            'equipment_id': 'EQUIP002',
            'name': 'New Equipment',
            'description': 'New Description'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Debería ser prohibido

    def test_update_equipment_as_admin(self):
        # Autenticarse como el usuario admin
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.admin_token))

        data = {
            'equipment_id': 'EQUIP002',
            'name': 'Updated Equipment',
            'description': 'Updated Description'
        }
        response = self.client.put(self.equipment_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar que el equipo se haya actualizado
        self.equipment.refresh_from_db()
        self.assertEqual(self.equipment.name, 'Updated Equipment')

    def test_update_equipment_as_non_admin(self):
        # Autenticarse como el usuario no admin
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.non_admin_token))

        data = {
            'name': 'Updated Equipment',
            'description': 'Updated Description'
        }
        response = self.client.put(self.equipment_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Debería ser prohibido

    def test_delete_equipment_as_admin(self):
        # Autenticarse como el usuario admin
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.admin_token))

        response = self.client.delete(self.equipment_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_equipment_as_non_admin(self):
        # Autenticarse como el usuario admin
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.non_admin_token))

        response = self.client.delete(self.equipment_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

