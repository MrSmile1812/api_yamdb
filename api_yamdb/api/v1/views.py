from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Review, Title
from django.shortcuts import get_object_or_404

from .serializers import CommentSerializer, ReviewSerializer

from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = IsAuthenticatedOrReadOnly

    def get_queryset(self):
        current_title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return current_title.reviews.all()

    def perform_create(self, serializer):
        current_title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=current_title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = IsAuthenticatedOrReadOnly

    def get_queryset(self):
        current_review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        )
        return current_review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)