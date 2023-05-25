from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

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
    permission_classes = [
        permissions.IsAuthenticated,
        IsAdmin,
    ]
    pagination_class = PageNumberPagination
    lookup_field = "username"


# class MeViewSet(generics.RetrieveUpdateAPIView):
#     serializer_class = UserSerializer
#     lookup_field = "username"
#     permission_classes = [
#         permissions.IsAuthenticated,
#     ]
#     queryset = User.objects.all()


#     @action(methods=["GET"], detail=True, url_path="v1/users/me/")
#     def me(self, username=None):
#         print("333", self.request.user.get_username())
#         # user = get_object_or_404(User, username=self.request.user)
#         username = self.request.user.get_username
#         return self.retrieve(self.request, username=username)
@api_view(
    ["GET", "PATCH"],
)
def me(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if request.method == "GET":
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
