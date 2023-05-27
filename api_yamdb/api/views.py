from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from reviews.models import User
from .permissions import IsAdmin, ExcludePut
from .serializers import UserSerializer, AuthSerializer
from .helpers import send_email, get_confirmation_code


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
