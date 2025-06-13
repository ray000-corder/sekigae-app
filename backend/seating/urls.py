from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, UserCreateView, SeatLayoutViewSet, SeatViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'seat-layouts', SeatLayoutViewSet, basename='seat-layout')
router.register(r'seats', SeatViewSet, basename='seat') # ← SeatViewSetの登録

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'), # ← registerのパス
]

urlpatterns += router.urls