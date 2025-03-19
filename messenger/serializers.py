from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Chat, Message


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = Profile
        fields = ['id', 'name', 'avatar']

    def create(self, validated_data):
        # Получаем текущего пользователя из контекста
        user = self.context['request'].user
        if not user.is_authenticated:
            raise serializers.ValidationError("Только зарегистрированные пользователи могут загружать аватар.")

        # Убираем 'user' из validated_data, чтобы избежать дублирования
        validated_data.pop('user', None)

        # Создаем профиль с указанием пользователя
        return Profile.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'profile']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
