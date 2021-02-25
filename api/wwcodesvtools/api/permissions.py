from rest_framework import permissions
from .models import UserProfile
import logging


logger = logging.getLogger('django')


class CanSendEmail(permissions.BasePermission):
    """
    Check if user can send email.
    """
    def has_permission(self, request, view):
        return has_director_permission(request, view)


class CanGetMemberInfo(permissions.BasePermission):
    """
    Check if user can get member infomation.
    """
    def has_permission(self, request, view):
        return has_director_permission(request, view)


class CanAddMember(permissions.BasePermission):
    """
    Check if user can add member.
    """
    def has_permission(self, request, view):
        return has_director_permission(request, view)


class CanDeleteMember(permissions.BasePermission):
    """
    Check if user can add member.
    """
    def has_permission(self, request, view):
        return has_director_permission(request, view)


def has_director_permission(request, view):
    """
    Check if logged in user has DIRECTOR role or IsSuperUser
    """
    try:
        user_profile = UserProfile.objects.get(user_id=request.user.id)
        if request.user.is_superuser or user_profile.role == UserProfile.DIRECTOR:
            return True
        return False
    except UserProfile.DoesNotExist as e:
        logger.error(f'has_director_permission: Error user not found : {e}')
        return False
