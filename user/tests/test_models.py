from django.test import TestCase
from user.models import LabUser

class LabUserModelTest(TestCase):

    def setUp(self):
        self.user = LabUser.objects.create(username='GadoDev', email='gadodev@mail.com', phone_number='1234567890')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'GadoDev')
        self.assertEqual(self.user.email, 'gadodev@mail.com')
        self.assertEqual(self.user.phone_number, '1234567890')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

    def test_user_str(self):
        # Verifica el método __str__ si lo has definido
        self.assertEqual(str(self.user), 'Se creo el usuario GadoDev')