from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

app_name = "user"

# / (GET, POST): 목록 조회, 생성
# /<pk>/ (GET, PUT, PATCH, DELETE) 조회, 업데이트
# /login/ (POST): 로그인
# /logout/ (POST): 로그아웃
router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
