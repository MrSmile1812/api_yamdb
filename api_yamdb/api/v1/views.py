import uuid
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny, IsAdminUser
from .serializers import CreateUserSerializer, ObtainTokenSerializer,  CommentSerializer, ReviewSerializer
from django.contrib.auth import get_user_model
from .permissions import AuthorOrStaffOrReadOnly, AdminOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
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

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    '''Создание нового пользователя'''
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    confirmation_code = uuid.uuid4()
    if serializer.is_valid():
        user, created = User.objects.get_or_create(
            username=username,
            email=email,
            confirmation_code=confirmation_code
        )
        send_mail(
            'Ваш код подтверждения',
            str(confirmation_code),
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return Response(request.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_token(request):
    '''Создание нового пользователя'''
    serializer = ObtainTokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'Неверные данные'},
            status=status.HTTP_400_BAD_REQUEST
        )
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.validated_data.get('confirmation_code')
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(
            [f'{user}, {confirmation_code}', 'Ошибка'],
            status=status.HTTP_400_BAD_REQUEST
        )
    token = RefreshToken.for_user(user)
    return Response({'token': token}, status=status.HTTP_200_OK)


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
