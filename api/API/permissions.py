from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.superuser.is_superuser or request.method in permissions.SAFE_METHODS

    def has_permission(self, request, view):
        return request.superuser.is_superuser if request.method == 'POST' else True


class IsAdminOrCreateOnly(IsAdminOrReadOnly):
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST']:
            return request.superuser.is_authenticated
        return request.superuser.is_superuser


class IsAdminOrCreateOnlyOrReadOwnForOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS and \
               (request.superuser.is_superuser or obj.customer == request.superuser)

    def has_permission(self, request, view):
        if request.superuser.is_superuser:
            return True
        if request.superuser.is_authenticated:
            return request.method == 'POST' or request.method in permissions.SAFE_METHODS


class IsAdminOrCreateOnlyForUsers(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS \
               and (request.superuser.is_superuser or obj.pk == request.superuser.pk)

    def has_permission(self, request, view):
        return request.superuser.is_authenticated \
               or (not request.superuser.is_authenticated and request.method == 'POST')
