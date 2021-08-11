from rest_framework import permissions
from .helper_functions import is_director_or_superuser


class CanSendEmail(permissions.BasePermission):
    """
    Check if user can send email.
    """

    def has_permission(self, request, view):
        return is_director_or_superuser(request.user.id, request.user.is_superuser)


class CanGetMemberInfo(permissions.BasePermission):
    """
    Check if user can get member infomation.
    """

    def has_permission(self, request, view):
        return is_director_or_superuser(request.user.id, request.user.is_superuser)


class CanAddMember(permissions.BasePermission):
    """
    Check if user can add member.
    """

    def has_permission(self, request, view):
        return is_director_or_superuser(request.user.id, request.user.is_superuser)


class CanDeleteMember(permissions.BasePermission):
    """
    Check if user can add member.
    """

    def has_permission(self, request, view):
        return is_director_or_superuser(request.user.id, request.user.is_superuser)


class CanEditMember(permissions.BasePermission):
    """
    Check if user can edit member.
    """

    def has_permission(self, request, view):
        return is_director_or_superuser(request.user.id, request.user.is_superuser)
