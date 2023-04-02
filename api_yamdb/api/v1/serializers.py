from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    class Meta:
        model = User
        fields = ('username','email',)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('Недопустимое имя!')
        return data
    