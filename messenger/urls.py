from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Создаем роутер для API
router = DefaultRouter()
router.register(r'profile', views.ProfileViewSet)
router.register(r'chat', views.ChatViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # API маршруты
]

