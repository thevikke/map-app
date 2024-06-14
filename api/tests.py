# api/tests.py

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import PointOfInterest
from django.contrib.gis.geos import Point

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

#TODO: Check the tests.
class PointOfInterestAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_authentication(self):
        response = self.client.post('/api-token-auth/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.token = response.data['token']

    def test_add_point(self):
        self.test_authentication()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        data = {
            "name": "Point 1",
            "description": "A description",
            "location": "POINT (30 10)"
        }
        response = self.client.post('/api/points/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PointOfInterest.objects.count(), 1)
        self.assertEqual(PointOfInterest.objects.get().name, 'Point 1')

    def test_list_points(self):
        PointOfInterest.objects.create(
            name="Point 1", description="A description", location=Point(30, 10), created_by=self.user
        )
        self.test_authentication()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get('/api/points/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Point 1')

    def test_delete_point(self):
        point = PointOfInterest.objects.create(
            name="Point 1", description="A description", location=Point(30, 10), created_by=self.user
        )
        self.test_authentication()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f'/api/points/{point.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PointOfInterest.objects.count(), 0)

    def test_access_without_token(self):
        response = self.client.get('/api/points/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)