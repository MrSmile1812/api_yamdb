from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.serializers import CurrentUserDefault, SlugRelatedField
from reviews.models import Comment, Review, Title

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
                'Пользователь не найден'
            )
        return data


class ReviewSerializer(serializers.ModelSerializer):
    """Класс для преобразования данных отзыва."""

    author = SlugRelatedField(
        read_only=True, slug_field="username", default=CurrentUserDefault()
    )

    def validate(self, data):
        """Валидируем, что на одно произведение
        пользователь может оставить только один отзыв."""
        request = self.context.get("request")
        if request.method == "POST":
            author = request.user
            title = self.context.get("view").kwargs.get("title_id")
            if Review.objects.filter(author=author, title=title).exists():
                raise serializers.ValidationError(
                    "Вы уже оставляли отзыв на это произведение"
                )
        return data

    class Meta:
        model = Review
        fields = ("id", "title", "text", "author", "score", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    """Класс для преобразования данных комментария."""

    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
