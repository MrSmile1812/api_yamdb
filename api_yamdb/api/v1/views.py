import uuid
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny, IsAdminUser
from .serializers import CreateUserSerializer, ObtainTokenSerializer,  CommentSerializer, ReviewSerializer
from django.contrib.auth import get_user_model
from .permissions import AuthorOrStaffOrReadOnly, AdminOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Review, Title

from django.shortcuts import get_object_or_404


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
