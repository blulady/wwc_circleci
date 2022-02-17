from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from api.models import UserProfile
from api.permissions import CanEditMember
from api.serializers.UserProfileSerializer import UserProfileSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import logging

logger = logging.getLogger('django')


class UpdateMemberStatusView(GenericAPIView):
    """
        Edits the Status in the UserProfile for the specified user's id
    """
    permission_classes = [IsAuthenticated & CanEditMember]
    serializer_class = UserProfileSerializer

    ERROR_EDITING_PENDING_USER = 'User can not be edited because her status is pending'
    ERROR_PAGE_NOT_FOUND = 'Specified value not found or invalid for this request'
    INTERNAL_SERVER_ERROR_EDITING_USER_PROFILE = 'Something went wrong while updating User Profile'
    USER_STATUS_EDITED_SUCCESSFULLY = 'User status edited successfully'

    post_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="User status edited successfully",
            examples={
                "application/json": {
                    'result': USER_STATUS_EDITED_SUCCESSFULLY
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
                    'error': INTERNAL_SERVER_ERROR_EDITING_USER_PROFILE
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
                        'status': ["This field may not be blank.",
                                   "Invalid Status: accepted values are 'ACTIVE','INACTIVE'"]
                    }
                }
            }
        ),
    }

    @swagger_auto_schema(responses=post_response_schema)
    def post(self, request, id):
        user_status = request.data.get('status')
        user_obj = get_object_or_404(User.objects.select_related('userprofile'), id=id)
        userprofile_obj = user_obj.userprofile
        try:
            if userprofile_obj.is_pending():
                logger.debug(f'UpdateMemberStatusView: userId:{id} ,status:{user_status}')
                return Response({'error': self.ERROR_EDITING_PENDING_USER}, status=status.HTTP_403_FORBIDDEN)
            if user_status in UserProfile.REGISTERED_USER_VALID_STATUSES:
                userprofile_serializer = UserProfileSerializer(userprofile_obj, data={'status': user_status})
                userprofile_serializer.is_valid()
                userprofile_serializer.save()
                return Response({'result': self.USER_STATUS_EDITED_SUCCESSFULLY}, status=status.HTTP_200_OK)
            else:
                logger.debug(f'userprofile_serializer in UpdateMemberStatusView returns invalid: userId:{id} ,status:{user_status}')
                return Response({'error': self.ERROR_PAGE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            error = f'{self.INTERNAL_SERVER_ERROR_EDITING_USER_PROFILE}: {e}'
            logger.error(f'UpdateMemberStatusView: {error}')
            return Response({'error': self.INTERNAL_SERVER_ERROR_EDITING_USER_PROFILE}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
