from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Review, Title

from django.shortcuts import get_object_or_404

from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс для работы с отзывами."""

    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = IsAuthenticatedOrReadOnly

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        current_title = get_object_or_404(
            Title.objects.select_related("category", "genre"),
            pk=title_id,
        )
        return current_title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        current_title = get_object_or_404(
            Title.objects.select_related("category", "genre"),
            pk=title_id,
        )
        serializer.save(author=self.request.user, title=current_title)


class CommentViewSet(viewsets.ModelViewSet):
    """Класс для работы с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = IsAuthenticatedOrReadOnly

    def get_queryset(self):
        current_review = get_object_or_404(
            Review.objects.select_related("title", "author"),
            pk=self.kwargs.get("review_id"),
        )
        return current_review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(
            Review.objects.select_related("title", "author"),
            id=review_id,
            title=title_id,
        )
        serializer.save(author=self.request.user, review=review)
