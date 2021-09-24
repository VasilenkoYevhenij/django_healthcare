from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import MyUser

CLIENT_REGISTER_URL = '/users/client/register/'
DOCTOR_REGISTER_URL = '/users/doctor/register/'
HOSPITAL_ADMIN_REGISTER_URL = '/users/hospital-admin/register/'


def sample_user(email, password, is_doctor, is_hospital_admin):
    """Create and return user object"""
    return MyUser.objects.create_user(email, is_hospital_admin, is_doctor, password)


class UsersRegistrationTestCase(APITestCase):
    """Test users registration"""

    def setUp(self):
        self.client = APIClient()

    def test_doctor_registration(self):
        """Test doctors registration"""

        payload = {
            "user": {
                "email": "user@user.com",
                "password": "useruser111",
                "is_doctor": True,
                "is_hospital_admin": False
            },
            'first_name': 'Doctor',
            'last_name': 'JaneDoe'
        }

        response = self.client.post(DOCTOR_REGISTER_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = MyUser.objects.get(email=response.data['user']['email'])
        self.assertTrue(user.check_password(payload['user']['password']))
        self.assertNotIn('password', response.data)
        self.assertIn('token', response.data['user'])
        self.assertTrue(user.is_doctor)

    def test_client_registration(self):
        """Test clients registration"""

        payload = {
            "user": {
                "email": "user1@user.com",
                "password": "useruser111",
                "is_doctor": False,
                "is_hospital_admin": False
            },
            'first_name': 'Client',
            'last_name': 'Test',
            'phone_number': '+38029342402',
            'gender': 'Male',
            'age': '20'
        }

        response = self.client.post(CLIENT_REGISTER_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = MyUser.objects.get(email=response.data['user']['email'])
        self.assertTrue(user.check_password(payload['user']['password']))
        self.assertNotIn('password', response.data)
        self.assertIn('token', response.data['user'])

    def test_hospital_admin_registration(self):
        """Test hospital admin registration"""

        payload = {
            "user": {
                "email": "user3@user.com",
                "password": "useruser111",
                "is_doctor": False,
                "is_hospital_admin": True
            },
            'first_name': 'Doctor',
            'last_name': 'JaneDoe'
        }

        response = self.client.post(HOSPITAL_ADMIN_REGISTER_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = MyUser.objects.get(email=response.data['user']['email'])
        self.assertTrue(user.check_password(payload['user']['password']))
        self.assertNotIn('password', response.data)
        self.assertIn('token', response.data['user'])
        self.assertTrue(user.is_hospital_admin)

    def test_create_user_exists(self):
        """Test creating a user that already exist fails"""
        payload = {
            "user": {
                "email": "user4@user.com",
                "password": "useruser111",
                "is_doctor": False,
                "is_hospital_admin": True
            },
            'first_name': 'Test',
            'last_name': 'JustUser'
        }
        sample_user(
            payload['user']['email'], payload['user']['password'],
            payload['user']['is_doctor'], payload['user']['is_hospital_admin']
        ),
        response = self.client.post(HOSPITAL_ADMIN_REGISTER_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be at least 8 characters"""

        payload = {
            "user": {
                "email": "user5@user.com",
                "password": "us",
                "is_doctor": False,
                "is_hospital_admin": True
            },
            'first_name': 'Test1',
            'last_name': 'JustUser2'
        }

        response = self.client.post(HOSPITAL_ADMIN_REGISTER_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UsersLoginTestCase(APITestCase):
    """Test users login"""

    def setUp(self):
        self.client = APIClient()

    def test_user_login(self):
        payload = {
            'email': 'user@user.com',
            'password': 'useruser111'
        }
        sample_user(payload['email'], payload['password'], False, False)

        response = self.client.post('/users/login/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
