from django.urls import include, path
from .views import UserDetailView
from rest_framework.routers import DefaultRouter
from .views import PointOfInterestViewSet

router = DefaultRouter()
router.register(r'points', PointOfInterestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('auth/user/', UserDetailView.as_view(), name='user_detail')
]
