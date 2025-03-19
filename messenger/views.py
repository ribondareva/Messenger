from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Chat, Message, Profile
from .serializers import ChatSerializer, MessageSerializer, UserSerializer, ProfileSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Сохраняем форму и автоматически авторизуем пользователя
            user = form.save()
            login(request, user)  # автоматически логиним пользователя
            return redirect('index')
    else:
        # Если форма не отправлена, создаем ее
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def index(request):
    return render(request, 'index.html')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            raise PermissionDenied("Вы должны быть авторизованы для создания профиля.")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request_user'] = self.request.user  # Передаем данные текущего пользователя
        return context

    @action(detail=False, methods=['get'])
    def current_user_profile(self, request):
        profile = Profile.objects.filter(user=request.user).first()
        if profile:
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        return Response({"detail": "Профиль не найден."}, status=404)

    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        profile = Profile.objects.filter(user=request.user).first()
        if not profile:
            return Response({"detail": "Профиль не найден."}, status=404)

        # Обновление имени и аватара
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Устанавливаем пользователя автоматически
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Фильтруем сообщения по чату, если указан параметр в URL
        chat_id = self.request.query_params.get('chat', None)
        if chat_id is not None:
            return Message.objects.filter(chat__id=chat_id)
        return super().get_queryset()

    @action(detail=False, methods=['get'])
    def get_chat_messages(self, request):
        # Получаем все сообщения для указанного чата
        chat_id = request.query_params.get('chat', None)
        if not chat_id:
            return Response({"detail": "Chat ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        chat = Chat.objects.filter(id=chat_id).first()
        if not chat:
            return Response({"detail": "Chat not found."}, status=status.HTTP_404_NOT_FOUND)

        messages = Message.objects.filter(chat=chat)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
