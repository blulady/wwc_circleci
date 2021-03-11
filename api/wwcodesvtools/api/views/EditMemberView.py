from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
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
from django.db import transaction

logger = logging.getLogger('django')


class EditMemberView(GenericAPIView):
    """
    Edits the User and its related information from the database

    """
    permission_classes = [IsAuthenticated & CanEditMember]

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
        user = get_object_or_404(User, id=id)
        try:
            user_row = UserProfile.objects.get(user_id=id)
            if user_row.status == UserProfile.PENDING:
                return Response({'error': 'User can not be edited because her status is pending.'}, status=status.HTTP_403_FORBIDDEN)

            data = {}
            updatable_fields = ['role', 'status']
            for field in updatable_fields:
                if field in request.data:
                    data[field] = request.data[field]
            if self.edit_user_profile(id, data):
                return Response({'result': 'User edited successfully'}, status=status.HTTP_200_OK)
            else:
                error = "User's role or status entered is empty or incorrect."
                res_status = status.HTTP_403_FORBIDDEN
                return Response({'error': error}, status=res_status)

        except Exception as e:
            logger.error(f'EditMemberView:Error editing the User: {e}')
            return Response({'error': 'Error Editing the User'}, status=status.HTTP_403_FORBIDDEN)

    def edit_user_profile(self, user_id, data):
        try:
            user_row = UserProfile.objects.get(user_id=user_id)
            logger.debug(
                f'row {user_row.user_id} : {user_row.role}  : {user_row.status}')
            if user_row:
                serializer_profile = EditMemberSerializer(user_row, data=data)
                if serializer_profile.is_valid():
                    serializer_profile.save()
                    return True
                else:
                    logger.error(
                        f'EditMemberView:Error updating user profile : {serializer_profile.errors}')
                    return False
        except UserProfile.DoesNotExist as e:
            logger.error(f'EditMemberView:Error updating user profile : {e}')
            return False
