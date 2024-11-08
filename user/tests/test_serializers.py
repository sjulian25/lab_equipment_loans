from django.test import TestCase
from user.models import LabUser 
from user.serializers import LabUserSerializer, LabUserDetailSerializer

class LabUserSerializerTest(TestCase):

    def setUp(self):
        self.valid_payload = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'full_name': 'Test User',
            'phone_number': '1234567890',
            'password': 'securepassword123'
        }
        self.invalid_payload = {
            'username': '',
            'email': 'invalidemail',
            'full_name': 'Test User',
            'phone_number': '1234567890',
            'password': 'securepassword123'
        }

    def test_create_user_with_valid_payload(self):
        serializer = LabUserSerializer(data=self.valid_payload)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, self.valid_payload['username'])
        self.assertEqual(user.email, self.valid_payload['email'])

        # Verificar que la contraseña se haya almacenado de forma segura
        self.assertNotEqual(user.password, self.valid_payload['password'])
        self.assertTrue(user.check_password(self.valid_payload['password']))

    def test_create_user_with_invalid_payload(self):
        serializer = LabUserSerializer(data=self.invalid_payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
        self.assertIn('email', serializer.errors)

    def test_create_user_with_existing_username(self):
        LabUser .objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='securepassword123'
        )
        serializer = LabUserSerializer(data=self.valid_payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_create_user_with_existing_email(self):
        LabUser .objects.create_user(
            username='anotheruser',
            email='testuser@example.com',
            password='securepassword123'
        )
        serializer = LabUserSerializer(data=self.valid_payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_user_detail_serialization(self):
        user = LabUser .objects.create_user(**self.valid_payload)
        detail_serializer = LabUserDetailSerializer(user)
        self.assertEqual(detail_serializer.data['username'], user.username)
        self.assertEqual(detail_serializer.data['email'], user.email)
        self.assertEqual(detail_serializer.data['full_name'], user.full_name)
        self.assertEqual(detail_serializer.data['phone_number'], user.phone_number)