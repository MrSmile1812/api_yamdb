from rest_framework import viewsets
from serializers import CommentSerializer, ReviewSerializer
from rest_framework.pagination import LimitOffsetPagination

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = ...


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = ...
