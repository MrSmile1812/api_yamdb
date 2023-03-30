from rest_framework import viewsets
from serializers import CommentSerializer, ReviewSerializer
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = ...

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

        


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = ...
