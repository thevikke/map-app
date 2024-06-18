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
        response = self.client.post('/api-token-auth/', {'username': self.username, 'password': self.password})
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response = self.client.get('/api/auth/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.username)

    def test_access_without_token(self):
        response = self.client.get('/api/auth/user/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PointOfInterestAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/api-token-auth/', {'username': 'testuser', 'password': 'testpassword'})
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_add_point(self):
        data = {
            "name": "Point 1",
            "description": "A description",
            "latitude": 30.0,
            "longitude": 10.0
        }
        response = self.client.post('/api/points/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PointOfInterest.objects.count(), 1)
        self.assertEqual(PointOfInterest.objects.get().name, 'Point 1')

    def test_list_points(self):
        PointOfInterest.objects.create(
            name="Point 1", description="A description", location=Point(30, 10), created_by=self.user
        )
        response = self.client.get('/api/points/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Point 1')

    def test_delete_point(self):
        point = PointOfInterest.objects.create(
            name="Point 1", description="A description", location=Point(30, 10), created_by=self.user
        )
        response = self.client.delete(f'/api/points/{point.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PointOfInterest.objects.count(), 0)

    def test_access_without_token(self):
        self.client.credentials()
        response = self.client.get('/api/points/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)