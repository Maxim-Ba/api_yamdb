from rest_framework.permissions import BasePermission, SAFE_METHODS
from .exceptions import GenericAPIException


class ExcludePut(BasePermission):
    message = "PUT запрос не предусмотрен."

    def has_permission(self, request, view):
        if request.method == "PUT":
            raise GenericAPIException(
                detail="PUT запрос не предусмотрен.", status_code=405
            )
        return True


class IsAdmin(BasePermission):
    message = "Вы не администратор."

    def has_permission(self, request, view):
        return request.user and (
            (request.user.is_authenticated and request.user.role == "admin")
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return request.user.role == "admin" or request.user.is_superuser


class IsModerator(BasePermission):
    message = "Вы не модератор."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "moderator"
        )

    def has_object_permission(self, request, view, obj):
        return request.user.role == "moderator"


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Разрешено только аутентифицированным пользователям выполнять действия,
    кроме методов GET, HEAD и OPTIONS, которые разрешены для всех.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
