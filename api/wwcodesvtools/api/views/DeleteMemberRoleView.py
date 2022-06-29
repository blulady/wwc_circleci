from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from ..models import User_Team, Role
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permissions import CanDeleteMemberRole
from api.serializers.EditMemberRoleTeamsSerializer import EditMemberRoleTeamsSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

import logging

logger = logging.getLogger('django')


class DeleteMemberRoleView(GenericAPIView):
    """
    Delete member role. All the teams associated with the role should be removed from the table.
    """
    permission_classes = [IsAuthenticated & CanDeleteMemberRole]
    serializer_class = EditMemberRoleTeamsSerializer

    SUCCESSFULLY_REMOVED_ROLE = "The requested role has been removed along with the associated teams"
    ERROR_DOES_NOT_HAVE_ROLE = "The user does not have this role so it cannot be removed"
    ERROR_LAST_ROLE_FOR_USER = "Member has only one role so delete is not allowed"
    ERROR_REMOVING_ROLE_FROM_USER = "User cannot be edited because her status is pending"
    INTERNAL_SERVER_ERROR_REMOVING_USER_ROLE = "Something went wrong while editing the User"

    post_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Role removed successfully",
            examples={
                "application/json": {
                    'result': SUCCESSFULLY_REMOVED_ROLE
                }
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Bad Request.",
            examples={
                "application/json": {
                    'error': {
                        'role': ["Invalid Role: accepted values are 'VOLUNTEER','LEADER','DIRECTOR'"]
                    }
                }
            }
        ),
        status.HTTP_403_FORBIDDEN: openapi.Response(
            description="Forbidden.",
            examples={
                "application/json": {
                    'error': 'User cannot be edited because her status is pending',
                }
            }
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
           description="Error not found",
           examples={
               "application/json": {
                   'error': 'The user does not have this role so it cannot be removed',
               }
           }
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: openapi.Response(
            description="Unprocessed entity.",
            examples={
                "application/json": {
                    'result': 'Either Member status is "pending" or Member has only one role, so delete is not allowed'
                }
            }
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
           description="Internal Server Error",
           examples={
               "application/json": {
                   'error': INTERNAL_SERVER_ERROR_REMOVING_USER_ROLE
               }
           }
        ),

    }

    @swagger_auto_schema(responses=post_response_schema)
    def delete(self, request, id, role):
        remove_role_obj = get_object_or_404(Role, name=role)
        remove_role_id = remove_role_obj.id
        user_obj = get_object_or_404(User.objects.select_related('userprofile'), id=id)
        userprofile_obj = user_obj.userprofile

        try:
            logger.debug(f'DeleteMemberRoleView: userId:{user_obj.id} , role:{role}')

            if userprofile_obj.is_pending():
                return Response({'error': self.ERROR_REMOVING_ROLE_FROM_USER},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            role_cnt = User_Team.objects.filter(user_id=user_obj.id).values('role_id').distinct('role_id').count()
            if role_cnt < 2:
                return Response({'error': self.ERROR_LAST_ROLE_FOR_USER}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            user_role_deleted = User_Team.objects.filter(user_id=user_obj.id, role_id=remove_role_id).delete()
            if user_role_deleted[0] == 0:
                return Response({'error': self.ERROR_DOES_NOT_HAVE_ROLE}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'result': self.SUCCESSFULLY_REMOVED_ROLE}, status.HTTP_200_OK)

        except Exception as e:
            error = f'{self.INTERNAL_SERVER_ERROR_REMOVING_USER_ROLE}: {e}'
            logger.error(f'DeleteMemberRoleView: {error}')
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
