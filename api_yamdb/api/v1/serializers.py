from rest_framework import serializers
from reviews.models import Comment, Review, Title
class ReviewSerializer(serializers.ModelSerializer):
     class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
