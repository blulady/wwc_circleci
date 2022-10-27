from rest_framework import permissions
from .helper_functions import is_director_or_superuser


class CanSendEmail(permissions.BasePermission):
    """
    Check if user can send email.
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


class CanEditResource(permissions.BasePermission):
    """
    Check if user can edit member.
    """

    def has_permission(self, request, view):
        return is_director_or_superuser(request.user.id, request.user.is_superuser)


class CanDeleteMemberRole(permissions.BasePermission):
    """
    Check if user can delete member role.
    """

    def has_permission(self, request, view):
        user_to_be_edited_id = view.kwargs['id']
        logged_in_user_id = request.user.id
        return (user_to_be_edited_id != logged_in_user_id) and (is_director_or_superuser(logged_in_user_id, request.user.is_superuser))


class CanAccessInvitee(permissions.BasePermission):
    """
    Check if user can access invitees.
    """

    def has_permission(self, request, view):
        return is_director_or_superuser(request.user.id, request.user.is_superuser)
