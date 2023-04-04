from rest_framework import permissions

ROLE = ['moderator', 'superuser', 'admin']


class AuthorOrStaffOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method == 'GET'
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.role in ROLE
        )


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method == 'GET'

    def has_object_permission(self, request, view, obj):
        return (request.user.is_admin
                or request.user.is_superuser)
