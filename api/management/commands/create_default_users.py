# create_default_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from api.models import PointOfInterest

class Command(BaseCommand):
    help = 'Create default users and points of interest'

    def handle(self, *args, **kwargs):
        users_data = [
            {'username': 'admin', 'email': 'admin@example.com', 'password': 'adminpassword', 'is_superuser': True, 'is_staff': True},
            {'username': 'user1', 'email': 'user1@example.com', 'password': 'user1password'},
            {'username': 'user2', 'email': 'user2@example.com', 'password': 'user2password'},
        ]

        points_data = {
            'admin': [
                {'name': 'Admin Point 1', 'description': 'Point created by admin', 'latitude': 40.712776, 'longitude': -74.005974},
                {'name': 'Admin Point 2', 'description': 'Another point created by admin', 'latitude': 34.052235, 'longitude': -118.243683},
            ],
            'user1': [
                {'name': 'User1 Point 1', 'description': 'Point created by user1', 'latitude': 51.507351, 'longitude': -0.127758},
                {'name': 'User1 Point 2', 'description': 'Another point created by user1', 'latitude': 48.856613, 'longitude': 2.352222},
            ],
            'user2': [
                {'name': 'User2 Point 1', 'description': 'Point created by user2', 'latitude': 35.689487, 'longitude': 139.691711},
                {'name': 'User2 Point 2', 'description': 'Another point created by user2', 'latitude': -33.868820, 'longitude': 151.209290},
            ]
        }

        for user_data in users_data:
            username = user_data['username']
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=user_data['email'],
                    password=user_data['password'],
                    is_superuser=user_data.get('is_superuser', False),
                    is_staff=user_data.get('is_staff', False)
                )
                self.stdout.write(self.style.SUCCESS(f'User {username} created'))

                if username in points_data:
                    for point in points_data[username]:
                        PointOfInterest.objects.create(
                            name=point['name'],
                            description=point['description'],
                            location=Point(point['longitude'], point['latitude']),
                            created_by=user
                        )
                        self.stdout.write(self.style.SUCCESS(f'Point {point["name"]} created for user {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'User {username} already exists'))
