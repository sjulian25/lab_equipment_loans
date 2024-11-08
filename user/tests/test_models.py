from django.test import TestCase
from user.models import LabUser

class LabUserModelTests(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'securepassword123'
        self.user = LabUser .objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def test_user_creation(self):
        """Prueba que un usuario se crea correctamente."""
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(self.user.email, self.email)
        self.assertTrue(self.user.check_password(self.password))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

    def test_create_superuser(self):
        """Prueba que un superusuario se crea correctamente."""
        superuser = LabUser .objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_without_username(self):
        """Prueba que se lanza un ValueError si no se proporciona un nombre de usuario."""
        with self.assertRaises(ValueError):
            LabUser .objects.create_user(username='', email=self.email)

    def test_user_without_email(self):
        """Prueba que se lanza un ValueError si no se proporciona un email."""
        with self.assertRaises(ValueError):
            LabUser .objects.create_user(username=self.username, email='')

    def test_str_method(self):
        """Prueba que el método __str__ devuelve el nombre de usuario correcto."""
        self.assertEqual(str(self.user), f'Se creó el usuario {self.username}')