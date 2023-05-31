from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Review, Title, User
from .permissions import (
    IsAdmin,
    IsAdminModeratorOrReadOnly,
    ExcludePut,
    IsAdminOrReadOnly
)
from .filters import TitleFilter

from .serializers import (
    CommentSerializer,
    UserSerializer,
    AuthSerializer,
    CategorySerializer,
    GenreSerializer,
    ReadTitleSerializer,
    WriteTitleSerializer,
    ReviewSerializer,
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
    permission_classes = [
        permissions.IsAuthenticated,
        ExcludePut,
        IsAdmin,
    ]
    pagination_class = PageNumberPagination
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)

    @action(
        detail=False,
        methods=["GET", "PATCH"],
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserSerializer,
    )
    def me(self, request):
        """view функция на эндройнт /users/me/"""
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        if "role" in request.data:
            serializer.validated_data["role"] = request.user.role
        serializer.save()
        return Response(serializer.data)


class CategoryViewSet(ListCreateDestroyViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(ListCreateDestroyViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Genre.objects.all().order_by("name")
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination
    queryset = (
        Title.objects.all().annotate(Avg("reviews__score")).order_by("name")
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return WriteTitleSerializer
        return ReadTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminModeratorOrReadOnly]

    def get_queryset(self):
        pk = self.kwargs.get("title_id")
        review_queryset = get_object_or_404(Title, pk=pk)
        return review_queryset.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id, title=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
