from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = "Вы не администратор."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )

    def has_object_permission(self, request, view, obj):
        print(request.user.role)
        return request.user.role == "admin"


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
