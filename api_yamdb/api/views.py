from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from reviews.models import Comment, Title
from .serializer import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        pk = self.kwargs.get('title_id')
        review_queryset = get_object_or_404(Title, pk=pk)
        return review_queryset.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    pass