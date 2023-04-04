from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from django.db.models import Avg
from django.shortcuts import get_object_or_404

from api.filters import TitleFilter
from api.permissions import AdminOrReadOnly, AuthorOrStaffOrReadOnly
from api.v1.mixins import ModelMixinSet
from api.v1.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    UserSerializer,
)
from reviews.models import Category, Genre, Review, Title
from user.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    permission_classes = IsAdminUser

    def retrieve(self, request, *args, **kwargs):
        self.object = get_object_or_404(
            User, username=self.request.user.username
        )
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)


class CategoryViewSet(ModelMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    permission_classes = AdminOrReadOnly


class GenreViewSet(ModelMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    permission_classes = AdminOrReadOnly


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg("reviews__score")).all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    serializer_class = TitleSerializer
    permission_classes = AdminOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс для работы с отзывами."""

    serializer_class = ReviewSerializer
    permission_classes = AuthorOrStaffOrReadOnly

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
    permission_classes = AuthorOrStaffOrReadOnly

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
