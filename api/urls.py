from django.urls import path
from .views import HelloWorldView

urlpatterns = [
    # Example endpoint to test authentication.
    path('hello/', HelloWorldView.as_view(), name='hello_world'),
]