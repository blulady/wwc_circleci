from rest_framework import permissions
from .models import UserProfile
import logging


logger = logging.getLogger('django')


class CanSendEmail(permissions.BasePermission):
    """
    Check if logged in user has DIRECTOR role or IsSuperUser
    """
    def has_permission(self, request, view):
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id)
            if request.user.is_superuser or user_profile.role == UserProfile.DIRECTOR:
                return True
            return False
        except UserProfile.DoesNotExist as e:
            logger.error(f'CanSendEmail: Error user not found : {e}')
            return False
