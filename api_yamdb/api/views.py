from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response  # Импортировали класс Response
from rest_framework.decorators import api_view  # Импортировали декоратор
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from reviews.models import User, Category, Genre, Title
from .permissions import IsAdmin
from .serializers import (
    UserSerializer,
    AuthSerializer,
    CategorySerialiser,
    GenreSerialiser,
    ReadTitleSerializer,
    WriteTitleSerializer
)
from .helpers import send_email, get_confirmation_code
from .mixins import ListCreateDestroyViewSet


@api_view(["POST"])
def signup(request):
    serializer = AuthSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        send_email(request.data["email"], request.data["email"])
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def token(request):
    user = get_object_or_404(User, username=request.data["username"])

    code = get_confirmation_code(user)
    if code == request.data["confirmation_code"]:
        return Response({"token": user.token})
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class CategoriesViewSet(ListCreateDestroyViewSet):
    serializer_class = CategorySerialiser
    permission_classes = []  #нужен пермишен "Создавать/ удалять может только администратор, остальные читают"
    pagination_class = LimitOffsetPagination
    queryset = Category.objects.all()
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(ListCreateDestroyViewSet):
    serializer_class = GenreSerialiser
    permission_classes = []  #нужен пермишен "Создавать/ удалять может только администратор, остальные читают"
    pagination_class = LimitOffsetPagination
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = []  #нужен пермишен "Создавать/ удалять может только администратор, остальные читают"
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
