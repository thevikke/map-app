# api/tests.py

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = APIClient()

    def test_login(self):
        response = self.client.post('/api-token-auth/', {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        token = response.data['token']
        self.assertTrue(Token.objects.filter(key=token).exists())

    def test_invalid_login(self):
        response = self.client.post('/api-token-auth/', {'username': self.username, 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_access_with_token(self):
        # Obtain the token
        response = self.client.post('/api-token-auth/', {'username': self.username, 'password': self.password})
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        
        # Access the protected endpoint
        response = self.client.get('/api/hello/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Hello, world!')

    def test_access_without_token(self):
        # Access the protected endpoint without a token
        response = self.client.get('/api/hello/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
