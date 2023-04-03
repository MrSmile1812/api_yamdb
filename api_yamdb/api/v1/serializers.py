from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('Недопустимое имя!')
        return data


class ObtainTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        if not username and not confirmation_code:
            raise serializers.ValidationError(
                f'Нет {username}, {confirmation_code}'
            )
        return data
