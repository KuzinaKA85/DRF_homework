from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Проверяет, является ли пользователь модератором."""

    message = "Вы не являетесь модератором"

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsNotModer(permissions.BasePermission):
    """НЕ модератор"""

    def has_permission(self, request, view):
        return not request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrModer(permissions.BasePermission):
    """Разрешение: владелец ИЛИ модератор"""

    def has_object_permission(self, request, view, obj):
        # Модератор может всё
        if request.user.groups.filter(name="moders").exists():
            return True
        # Обычный пользователь работает только со своими объектами
        return obj.owner == request.user
