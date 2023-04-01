from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from user.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Review
        fields = ("id", "title", "text", "author", "score", "pub_date")

    def validate(self, data):
        request = self.context["request"]
        author = request.user
        title = self.context["request"].parser_context["kwargs"]["title_id"]

        if request.method == "POST":
            if Review.objects.filter(author=author, title=title).exists():
                raise serializers.ValidationError(
                    "Вами уже был оставлен отзыв на это произведение"
                )

        return data


class TitleSerializerGet(serializers.ModelSerializer):
    category = SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = SlugRelatedField(slug_field="slug", queryset=Genre.objects.all())

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

    """def create(self, validated_data):
        if "genre" not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title
        else:
            genre = validated_data.pop("genre")
            print(genre)
            title = Title.objects.create(**validated_data)
            for g in genre:
                current_genre, status = Genre.objects.get_or_create(**g)
                GenreTitle.objects.create(achievement=current_genre, g=g)
            return g"""


class TitleSerializerPost(serializers.ModelSerializer):
    category = SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = SlugRelatedField(slug_field="slug", queryset=Genre.objects.all())

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


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")


class UserSerializer(serializers.ModelSerializer):
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
