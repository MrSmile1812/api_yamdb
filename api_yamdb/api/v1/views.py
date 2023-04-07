import uuid

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from api.filters import TitleFilter
from api.v1.mixins import ModelMixinSet
from api.v1.permissions import (
    AdminOnly,
    AdminOrReadOnly,
    AuthorOrStaffOrReadOnly,
)
from api.v1.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    NotAdminSerializer,
    ReviewSerializer,
    TitleSerializer,
    UserSerializer,
)
from reviews.models import Category, Genre, Review, Title
from user.models import User

from .serializers import (
    CommentSerializer,
    CreateUserSerializer,
    ObtainTokenSerializer,
    ReviewSerializer,
)


User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def create_user(request):
    """Создание нового пользователя."""
    serializer = CreateUserSerializer(data=request.data)
    if serializer.user_already_created(request.data):
        return Response(request.data, status=status.HTTP_200_OK)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    email = serializer.validated_data.get("email")
    confirmation_code = uuid.uuid4()
    if serializer.is_valid():
        user, created = User.objects.get_or_create(
            username=username, email=email, confirmation_code=confirmation_code
        )
        send_mail(
            "Your confirmation code",
            str(confirmation_code),
            None,
            [email],
            fail_silently=False,
        )
        return Response(request.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def create_token(request):
    """Получение токена."""
    serializer = ObtainTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    username = data.get("username")
    user = get_object_or_404(User, username=username)
    confirmation_code = data.get("confirmation_code")
    if data.get("confirmation_code") != user.confirmation_code:
        return Response(
            [f"{user}, {confirmation_code}", "Ошибка"],
            status=status.HTTP_400_BAD_REQUEST,
        )
    token = RefreshToken.for_user(user).access_token
    return Response({"token": str(token)}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Класс для работы с пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    permission_classes = (
        IsAuthenticated,
        AdminOnly,
    )
    http_method_names = ["get", "patch", "delete", "post"]

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path="me",
    )
    def get_current_user_info(self, request):
        serializer = UserSerializer(request.user)
        if request.method == "PATCH":
            if request.user.is_admin:
                serializer = UserSerializer(
                    request.user, data=request.data, partial=True
                )
            else:
                serializer = NotAdminSerializer(
                    request.user, data=request.data, partial=True
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class CategoryViewSet(ModelMixinSet):
    """Класс для работы с категориями."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    permission_classes = [AdminOrReadOnly]


class GenreViewSet(ModelMixinSet):
    """Класс для работы с жанрами."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    permission_classes = [AdminOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    """Класс для работы с произведениями."""

    queryset = (
        Title.objects.select_related("category")
        .annotate(rating=Avg("reviews__score"))
        .all()
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    serializer_class = TitleSerializer
    permission_classes = [AdminOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс для работы с отзывами."""

    serializer_class = ReviewSerializer
    permission_classes = [AuthorOrStaffOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        current_title = get_object_or_404(
            Title.objects,
            pk=title_id,
        )
        return current_title.reviews.select_related("author").all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        current_title = get_object_or_404(
            Title.objects,
            pk=title_id,
        )
        serializer.save(author=self.request.user, title=current_title)


class CommentViewSet(viewsets.ModelViewSet):
    """Класс для работы с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = [AuthorOrStaffOrReadOnly]

    def get_queryset(self):
        current_review = get_object_or_404(
            Review.objects.select_related("title", "author"),
            pk=self.kwargs.get("review_id"),
        )
        return current_review.comments.select_related("author").all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(
            Review.objects.select_related("title", "author"),
            id=review_id,
            title=title_id,
        )
        serializer.save(author=self.request.user, review=review)
