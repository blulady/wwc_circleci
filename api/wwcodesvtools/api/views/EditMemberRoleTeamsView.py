from rest_framework.response import Response
from rest_framework import status
from api.permissions import CanEditMember
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging
from api.models import Role, Team
from api.serializers.EditMemberRoleTeamsSerializer import EditMemberRoleTeamsSerializer


logger = logging.getLogger('django')


class EditMemberRoleTeamsView(GenericAPIView):
    """
    Add Role if role not yet assigned to User. Edits Teams for the User's Role.
    The input Teams is passed as list of team ids, for example [1,3,7]
    """
    permission_classes = [IsAuthenticated & CanEditMember]
    serializer_class = EditMemberRoleTeamsSerializer

    INTERNAL_SERVER_ERROR_EDITING_USER = 'Something went wrong while editing the User'
    ERROR_EDITING_PENDING_USER = 'User can not be edited because her status is pending'
    USER_EDITED_SUCCESSFULLY = 'Member role-teams edited successfully'
    ROLE_OR_TEAM_DOES_NOT_EXIST = 'Role or Team Does Not Exist'

    post_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Member role-teams edited successfully",
            examples={
                "application/json": {
                    'result': USER_EDITED_SUCCESSFULLY
                }
            }
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Error not found",
            examples={
                "application/json": {
                    'detail': 'Not found.',
                }
            }
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            description="Internal Server Error",
            examples={
                "application/json": {
                    'error': INTERNAL_SERVER_ERROR_EDITING_USER
                }
            }
        ),
        status.HTTP_403_FORBIDDEN: openapi.Response(
            description="Forbidden.",
            examples={
                "application/json": {
                    'error': ERROR_EDITING_PENDING_USER
                }
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Bad Request.",
            examples={
                "application/json": {
                    'error': {
                        'role': ["This field may not be blank.",
                                 "Invalid Role: accepted values are 'VOLUNTEER','LEADER','DIRECTOR'"],
                        'teams':  ["Invalid Teams: {ids} is not valid",
                                   "Invalid Teams: Duplicate values"],
                        'non_field_errors': ["Role other than {role} exists for one or more teams in request"]
                    }
                }
            }
        ),
    }

    @swagger_auto_schema(responses=post_response_schema)
    def put(self, request, id):
        res_status = None
        response_data = None
        user_obj = get_object_or_404(User.objects.select_related('userprofile'), id=id)
        req = request.data
        role = req.get('role')
        teams = req.get('teams')
        userprofile_obj = user_obj.userprofile
        try:
            logger.debug(f'MemberRoleTeamsView: userId:{id}, role:{role}, teams:{teams}')
            if userprofile_obj.is_pending():
                return Response({'error': self.ERROR_EDITING_PENDING_USER}, status=status.HTTP_403_FORBIDDEN)
            serializer_edit_member = EditMemberRoleTeamsSerializer(user_obj, data={'role': role, 'teams': teams})
            if serializer_edit_member.is_valid():
                serializer_edit_member.save()
                res_status = status.HTTP_200_OK
                response_data = {'result': self.USER_EDITED_SUCCESSFULLY}
            else:
                response_data = {'error': serializer_edit_member.errors}
                res_status = status.HTTP_400_BAD_REQUEST
        except (Role.DoesNotExist, Team.DoesNotExist) as e:
            logger.error(f'EditMemberRoleTeamsView: Role or Team not found : {e}')
            error = f'{self.ROLE_OR_TEAM_DOES_NOT_EXIST}: {e}'
            response_data = {'error': error}
            res_status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            error = f'{self.INTERNAL_SERVER_ERROR_EDITING_USER}: {e}'
            logger.error(f'EditMemberView: {error}')
            response_data = {'error': error}
            res_status = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response_data, status=res_status)
