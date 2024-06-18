from django.contrib.gis.db import models
from django.contrib.auth.models import User

class PointOfInterest(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.PointField(geography=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
