from django.urls import include, path
from .views import HelloWorldView
from rest_framework.routers import DefaultRouter
from .views import PointOfInterestViewSet

router = DefaultRouter()
router.register(r'points', PointOfInterestViewSet)

urlpatterns = [
    # Example endpoint to test authentication.
    path('hello/', HelloWorldView.as_view(), name='hello_world'),
    path('', include(router.urls)),
]
