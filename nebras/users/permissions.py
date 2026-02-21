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
        if not user:
            return False

        active_ban = Ban.objects.filter(user=user, is_banned=True).order_by('-banned_end').first()
        if active_ban:
            if active_ban.banned_end <= timezone.now():
                active_ban.is_banned = False
                active_ban.save(update_fields=['is_banned'])
            else:
                return False

        return bool(request.user.is_staff)
