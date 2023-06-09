from rest_framework import serializers
from rest_framework.serializers import CurrentUserDefault, SlugRelatedField

from django.contrib.auth import get_user_model

from reviews.models import Category, Comment, Genre, Review, Title
from user.models import User


User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализация регистрации пользователя и создания нового.
    Проверки username пользователя на валидность и уже существующего
    пользвателя.
    """

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

    def validate(self, data):
        if data["username"] == "me":
            raise serializers.ValidationError("Недопустимое имя!")
        return data

    def user_already_created(self, data):
        data_username = data.get("username")
        data_email = data.get("email")
        if (
            User.objects.filter(username=data_username).exists()
            and User.objects.filter(email=data_email).exists()
        ):
            return data


class ObtainTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получения confirmation_code. И проверка валидности
    полученного confirmation_code."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "confirmation_code",
        )

    def validate(self, data):
        username = data.get("username")
        confirmation_code = data.get("confirmation_code")
        if not username and not confirmation_code:
            raise serializers.ValidationError("Пользователь не найден")
        return data


class NotAdminSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя, не администратора."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = ("name", "slug")


class SlugDictRelatedField(serializers.SlugRelatedField):
    """Сериализатор для корректного вывода данных при запросах."""

    def to_representation(self, obj):
        result = {"name": obj.name, "slug": obj.slug}
        return result


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""

    category = SlugDictRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = SlugDictRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Класс для преобразования данных отзыва."""

    title = serializers.SlugRelatedField(slug_field="name", read_only=True)
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
