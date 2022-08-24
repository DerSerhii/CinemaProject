from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.method in permissions.SAFE_METHODS

    def has_permission(self, request, view):
        return request.user.is_superuser if request.method == 'POST' else True


class IsAdminOrCreateOnly(IsAdminOrReadOnly):
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST']:
            return request.user.is_authenticated
        return request.user.is_superuser


class IsAdminOrCreateOnlyOrReadOwnForOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS and \
               (request.user.is_superuser or obj.customer == request.user)

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            return request.method == 'POST' or request.method in permissions.SAFE_METHODS


class IsAdminOrCreateOnlyForUsers(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS \
               and (request.user.is_superuser or obj.pk == request.user.pk)

    def has_permission(self, request, view):
        return request.user.is_authenticated \
               or (not request.user.is_authenticated and request.method == 'POST')
