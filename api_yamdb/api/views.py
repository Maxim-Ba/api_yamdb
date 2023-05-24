from rest_framework import viewsets, permissions, status
from rest_framework.response import Response  # Импортировали класс Response
from rest_framework.decorators import api_view  # Импортировали декоратор
from django.shortcuts import get_object_or_404

from reviews.models import User
from .permissions import IsAdmin
from .serializers import UserSerializer, AuthSerializer
from .helpers import send_email, get_confirmation_code


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
