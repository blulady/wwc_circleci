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
from api.models import UserProfile
from api.serializers.EditMemberSerializer import EditMemberSerializer
from api.serializers.UserProfileSerializer import UserProfileSerializer
from django.db import transaction

logger = logging.getLogger('django')


class EditMemberView(GenericAPIView):
    """
    Edits the User Role and Status
    """
    permission_classes = [IsAuthenticated & CanEditMember]
    serializer_class = EditMemberSerializer

    ERROR_UPDATING_USER_PROFILE = 'Error updating user profile'
    ERROR_INVALID_INPUT_ROLE_STATUS = "User's role or status entered is empty or incorrect."

    post_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="User edited successfully",
            examples={
                "application/json": {
                    'result': 'User edited successfully',
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
                    'error': 'Error editing the User'
                }
            }
        ),
        status.HTTP_403_FORBIDDEN: openapi.Response(
            description="User's role or status entered is empty or incorrect.",
            examples={
                "application/json": {
                    'error': "User's role or status entered is empty or incorrect."
                }
            }
        ),
    }

    @swagger_auto_schema(responses=post_response_schema)
    @transaction.atomic
    def post(self, request, id):
        get_object_or_404(User, id=id)
        try:
            user_row = UserProfile.objects.get(id=id)
            if user_row.status == UserProfile.PENDING:
                return Response({'error': 'User can not be edited because her status is pending.'}, status=status.HTTP_403_FORBIDDEN)

            data = {}
            updatable_fields = ['role', 'status']
            for field in updatable_fields:
                if field in request.data:
                    data[field] = request.data[field]

            serializer_role_status = EditMemberSerializer(id, data=data)
            if serializer_role_status.is_valid():
                # creating txn savepoint
                sid = transaction.savepoint()
                res_profile_status_role = self.edit_user_profile(id, data)
                if res_profile_status_role:
                    # all well,commit data to the db
                    transaction.savepoint_commit(sid)
                    logger.info(
                        'EditMemberView: User data edited successfully')
                    res_status = status.HTTP_200_OK
                    error = None
                else:
                    if not res_profile_status_role:
                        error = self.ERROR_UPDATING_USER_PROFILE
                    # something went wrong, don't commit data to db,rollback txn
                    transaction.savepoint_rollback(sid)
                    res_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                error = self.ERROR_INVALID_INPUT_ROLE_STATUS
                res_status = status.HTTP_400_BAD_REQUEST

        except Exception as e:
            error = self.ERROR_UPDATING_USER_PROFILE
            logger.error(f'EditMemberView: {error}: {e}')
            res_status = status.HTTP_400_BAD_REQUEST

        if (error is None and res_status == status.HTTP_200_OK):
            return Response({'result': 'User edited successfully'}, status=status.HTTP_200_OK)
        return Response({'error': error}, status=res_status)

    def edit_user_profile(self, user_id, data):
        try:
            user_row = UserProfile.objects.get(user_id=user_id)
            logger.debug(
                f'row {user_row.user_id} : {user_row.role}  : {user_row.status}')
            if user_row:
                serializer_profile = UserProfileSerializer(user_row, data=data)
                if serializer_profile.is_valid():
                    serializer_profile.save()
                    return True
                else:
                    logger.error(
                        f'AddMemberView:Error updating user profile : {serializer_profile.errors}')
                    return False
        except UserProfile.DoesNotExist as e:
            logger.error(f'AddMemberView:Error updating user profile : {e}')
            return False
