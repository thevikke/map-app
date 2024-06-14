from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, mixins, permissions
from .models import PointOfInterest
from .serializers import PointOfInterestSerializer

class HelloWorldView(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"})

class PointOfInterestViewSet(mixins.ListModelMixin,
                             mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    queryset = PointOfInterest.objects.all()
    serializer_class = PointOfInterestSerializer
    # TODO: Check if this is needed?
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)