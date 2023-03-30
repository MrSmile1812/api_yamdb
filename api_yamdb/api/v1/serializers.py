from rest_framework import serializers
from rest_framework.serializers import CurrentUserDefault, SlugRelatedField
from reviews.models import Comment, Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field="username", default=CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ("id", "title", "text", "author", "score", "pub_date")

        def validate(self, data):
            request = self.context["request"]
            author = request.user
            title = self.context["request"].parser_context["kwargs"][
                "title_id"
            ]

            if request.method == "POST":
                if Review.objects.filter(author=author, title=title).exists():
                    raise serializers.ValidationError(
                        "Вами уже был оставлен отзыв на это произведение"
                    )

            return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
