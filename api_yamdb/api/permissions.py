from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = "Вы не администратор."

    def has_object_permission(self, request, view, obj):
        return request.user.role == "admin"


class IsModerator(BasePermission):
    message = "Вы не модератор."

    def has_object_permission(self, request, view, obj):
        return request.user.role == "moderator"
