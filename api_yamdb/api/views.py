from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response  # Импортировали класс Response
from rest_framework.decorators import api_view  # Импортировали декоратор
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from reviews.models import User, Category, Genre, Title
from .permissions import IsAdmin
from .serializers import (
    UserSerializer,
    AuthSerializer,
    CategorySerializer,
    GenreSerializer,
    ReadTitleSerializer,
    WriteTitleSerializer,
    ReviewSerializer
)
from .helpers import send_email, get_confirmation_code
from .mixins import ListCreateDestroyViewSet


@api_view(["POST"])
def signup(request):
    serializer = AuthSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        send_email(request.data["email"], request.data["email"])
        if User.objects.filter(
            email=request.data["email"], username=request.data["username"]
        ).exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def token(request):
    if "username" in request.data:
        user = get_object_or_404(User, username=request.data["username"])

        code = get_confirmation_code(user)
        if code == request.data["confirmation_code"]:
            return Response({"token": user.token})

    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    pagination_class = LimitOffsetPagination
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).all()
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return WriteTitleSerializer
        return ReadTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        pk = self.kwargs.get('title_id')
        review_queryset = get_object_or_404(Title, pk=pk)
        return review_queryset.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    pass
