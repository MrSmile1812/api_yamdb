from rest_framework import filters, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from api.v1.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializerGet,
    TitleSerializerPost,
    UserSerializer,
)
from reviews.models import Category, Comment, Genre, Review, Title
from user.models import User


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()

    def get_serializer_class(self):
        if (
            self.action == "list"
            or self.action == "delete"
            or self.action == "retrieve"
        ):
            return TitleSerializerGet
        if self.action == "create" or self.action == "partial_update":
            return TitleSerializerPost


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        queryset = Title.objects.select_related("title").filter(title=title_id)
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)
        return Response(status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["user"]

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        self.object = get_object_or_404(
            User, username=self.request.user.username
        )
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)


class MeViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["user"]

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)
