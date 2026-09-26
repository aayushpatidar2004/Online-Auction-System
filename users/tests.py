from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser


class UserAuthTests(APITestCase):
    def test_user_registration_and_login(self):
        # Register user
        register_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'phone': '919876543210',
            'password': 'SecurePassword123!',
            'password2': 'SecurePassword123!',
        }
        res = self.client.post('/api/users/register/', register_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.filter(username='newuser').count(), 1)

        # Login with JWT
        login_data = {
            'username': 'newuser',
            'password': 'SecurePassword123!',
        }
        login_res = self.client.post('/api/token/', login_data)
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_res.data)
        self.assertIn('refresh', login_res.data)

        # Access profile with token
        token = login_res.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        profile_res = self.client.get('/api/users/profile/')
        self.assertEqual(profile_res.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_res.data['username'], 'newuser')
        self.assertEqual(profile_res.data['phone'], '919876543210')

    def test_duplicate_username_registration_is_rejected_with_clear_message(self):
        existing_user = CustomUser.objects.create_user(
            username='existinguser',
            email='existinguser@example.com',
            phone='919876543211',
            password='SecurePassword123!'
        )
        self.assertIsNotNone(existing_user)

        duplicate_data = {
            'username': 'existinguser',
            'email': 'different@example.com',
            'phone': '919876543212',
            'password': 'SecurePassword123!',
            'password2': 'SecurePassword123!',
        }

        res = self.client.post('/api/users/register/', duplicate_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', res.data)
        self.assertIn('already exists', str(res.data['username']))
