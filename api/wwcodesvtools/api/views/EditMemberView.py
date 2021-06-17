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
from api.models import Role, User_Team, Team
from api.serializers.EditMemberSerializer import EditMemberSerializer
from api.serializers.UserProfileSerializer import UserProfileSerializer
from django.db import transaction


logger = logging.getLogger('django')


class EditMemberView(GenericAPIView):
    """
    Edits the Status, and Teams for the User's Role
    The input Teams is passed as list of team ids, for example [1,3,7]
    """
    permission_classes = [IsAuthenticated & CanEditMember]
    serializer_class = EditMemberSerializer

    INTERNAL_SERVER_ERROR_EDITING_USER_PROFILE = 'Something went wrong while updating User Profile'
    INTERNAL_SERVER_ERROR_EDITING_USER_ROLE_TEAM = 'Something went wrong while updating User Role Team'
    INTERNAL_SERVER_ERROR_EDITING_USER = 'Something went wrong while editing the User'
    ERROR_EDITING_PENDING_USER = 'User can not be edited because her status is pending'
    USER_EDITED_SUCCESSFULLY = 'User edited successfully'

    post_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="User edited successfully",
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
                        'status': ["This field may not be blank.",
                                   "Invalid Status: accepted values are 'ACTIVE','INACTIVE'"],
                        'teams':  ["Invalid Teams: {ids} is not valid",
                                   "Invalid Teams: Duplicate values"]
                    }
                }
            }
        ),
    }

    @swagger_auto_schema(responses=post_response_schema)
    @transaction.atomic
    def post(self, request, id):
        res_status = None
        error = None
        req = request.data
        user_status = req.get('status')
        role = req.get('role')
        teams = req.get('teams')
        user_obj = get_object_or_404(User.objects.select_related('userprofile'), id=id)
        userprofile_obj = user_obj.userprofile
        try:
            logger.debug(f'EditMemberView: userId:{id} ,status:{user_status}, role:{role}, teams:{teams}')
            if userprofile_obj.is_pending():
                return Response({'error': self.ERROR_EDITING_PENDING_USER}, status=status.HTTP_403_FORBIDDEN)
            serializer_edit_member = EditMemberSerializer(id, data={'role': role, 'status': user_status, 'teams': teams})
            if not serializer_edit_member.is_valid():
                return Response({'error': serializer_edit_member.errors}, status=status.HTTP_400_BAD_REQUEST)

            # edit member data in the db user_team table and the user profile table
            sid = transaction.savepoint()
            result_user_role_team = self.update_user_role_team(user_obj, role, teams)
            if 'success' in result_user_role_team:
                result_profile_status = self.edit_user_profile(userprofile_obj, user_status, role)
                if 'success' in result_profile_status:
                    # commit txn now, both tables are updated
                    transaction.savepoint_commit(sid)
                    logger.info('EditMemberView: save commit, User data edited successfully')
                    res_status = status.HTTP_200_OK
                else:
                    transaction.savepoint_rollback(sid)
                    logger.info('EditMemberView: user profile update unsuccessful, rollback')
                    return Response({'error': result_profile_status['error']}, status=result_profile_status['status'])
            else:
                transaction.savepoint_rollback(sid)
                logger.info('EditMemberView: user role team update unsuccessful,rollback')
                return Response({'error': result_user_role_team['error']}, status=result_user_role_team['status'])
        except Exception as e:
            error = f'{self.INTERNAL_SERVER_ERROR_EDITING_USER}: {e}'
            logger.error(f'EditMemberView: {error}: {e}')
            res_status = status.HTTP_500_INTERNAL_SERVER_ERROR

        if (error is None and res_status == status.HTTP_200_OK):
            return Response({'result': self.USER_EDITED_SUCCESSFULLY}, status=status.HTTP_200_OK)
        return Response({'error': error}, status=res_status)

    def edit_user_profile(self, userprofile_row, user_status, role):
        try:
            serializer_profile = UserProfileSerializer(userprofile_row, data={'status': user_status, 'role': role})
            if serializer_profile.is_valid():
                serializer_profile.save()
                return {'success': 'True'}
            else:
                logger.error(f'EditMemberView: Serializer errors: {serializer_profile.errors}')
                return {'error': f'serializer errors: {serializer_profile.errors}', 'status': status.HTTP_400_BAD_REQUEST}
        except Exception as e:
            logger.error(f'EditMemberView: Exception editing user profile : {e}')
            return {'error': f'{self.INTERNAL_SERVER_ERROR_EDITING_USER_PROFILE}: {e}',
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR}

    def update_user_role_team(self, user_obj, role, teams):
        try:
            role_obj = Role.objects.get(name=role)
            logger.debug(f'EditMemberView: add_remove_user_role_team for list of teams= {teams}, role={role}, userId= {user_obj.id}')
            if user_obj and role_obj:
                try:
                    # first,remove the existing user team rows for the role
                    User_Team.objects.filter(user_id=user_obj.id, role_id=role_obj.id).delete()
                except (User_Team.DoesNotExist) as e:
                    logger.error(f'EditMemberView:  No User role team rows found, none deleted {e}')
                if len(teams) > 0:
                    # add the team rows for the user role
                    team_objs = Team.objects.filter(id__in=teams)
                    user_team_objs = [User_Team(user=user_obj, role=role_obj, team=team_obj) for team_obj in team_objs]
                    User_Team.objects.bulk_create(user_team_objs)
                else:
                    # add a row with no team for the user role
                    user_team = User_Team(user=user_obj, role=role_obj, team=None)
                    user_team.save()
                return {'success': 'True'}
        except (Role.DoesNotExist, Team.DoesNotExist) as e:
            logger.error(f'EditMemberView: Role or Team not found : {e}')
            return {'error': f'Role or Team Does Not Exist : {e}', 'status': status.HTTP_404_NOT_FOUND}
        except Exception as e:
            logger.error(f'EditMemberView: Exception updating user role team : {e}')
            return {'error': f'{self.INTERNAL_SERVER_ERROR_UPDATING_USER_ROLE_TEAM}: {e}',
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR}
