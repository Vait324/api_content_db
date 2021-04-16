from rest_framework import permissions

MODERATOR_METHODS = ('PATCH', 'DELETE',)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_staff
                or request.user.role == 'admin'
            )
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.role == 'admin'
        )


class IsAuthorOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.method == 'POST' and not request.user.is_anonymous
            or request.method in MODERATOR_METHODS
            and (
                request.user == obj.author
                or request.user.role == 'moderator'
            )
        )
