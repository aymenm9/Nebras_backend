from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    """
    Allows access only to super admins (is_superuser = True).
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class IsModerator(permissions.BasePermission):
    """
    Allows access to moderators and super admins (is_staff = True).
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
