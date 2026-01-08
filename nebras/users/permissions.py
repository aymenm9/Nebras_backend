from rest_framework import permissions
from .models import Ban
from django.utils import timezone
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
        user = request.user
        if not user :
            return False
        is_banned = Ban.objects.filter(user=user, is_banned=True, banned_end__gt=timezone.now()).exists()
        return bool(not is_banned and request.user.is_staff)
