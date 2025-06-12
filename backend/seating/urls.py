from django.urls import path
from rest_framework.routers import DefaultRouter
# ↓ ここに SeatViewSet を追加します
from .views import StudentViewSet, UserCreateView, SeatLayoutViewSet, SeatViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'seat-layouts', SeatLayoutViewSet, basename='seat-layout')
# ↓ この一行を追加して、新しいAPIの住所を登録します
router.register(r'seats', SeatViewSet, basename='seat')

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
]

urlpatterns += router.urls