"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from messenger import views
from django.conf import settings
from django.conf.urls.static import static

# Создаем роутер для API
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.ProfileViewSet, basename='profile')
router.register(r'messages', views.MessageViewSet, basename='message')
router.register(r'chats', views.ChatViewSet, basename='chat')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Страница регистрации
    path('register/', views.register, name='register'),

    # Страница логина
    path('login/', LoginView.as_view(), name='login'),

    # Страница логаута
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # Главная страница
    path('', views.index, name='index'),

    # API маршруты
    path('api/', include(router.urls)),
]

# Добавляем поддержку медиа-файлов (для аватарок и прочего)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

