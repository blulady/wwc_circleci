from api.serializers.ChangePasswordSerializer import ChangePasswordSerializer
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from api.helper_functions import send_email_helper

import logging

logger = logging.getLogger('django')


class ChangePasswordView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    ERROR_PASSWORD_PENDING_USER = "User can not be edited because her status is pending"
    ERROR_CHANGING_PASSWORD = "Error changing password"
    ERROR_PASSWORDS_SAME = "New password cannot be the same as the old password"
    ERROR_EXCEPTION = "Exception {e}"
    SUCCESS_PASSWORD_CHANGED = "Success, password changed"

    post_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Set new password successfully",
            examples={
                "application/json": {
                    'success': SUCCESS_PASSWORD_CHANGED
                }
            }
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            description="Internal Server Error",
            examples={
                "application/json": {
                    'error': ERROR_EXCEPTION
                }
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    'error': ERROR_CHANGING_PASSWORD
                }
            }
        ),
    }

    @swagger_auto_schema(responses=post_response_schema)
    def patch(self, request):
        user_obj = get_object_or_404(User, id=self.request.user.id)
        userprofile_obj = user_obj.userprofile
        try:
            serializer = ChangePasswordSerializer(user_obj, data=request.data)
            if userprofile_obj.is_pending():
                response_data = {'error': self.ERROR_PASSWORD_PENDING_USER}
                return Response({response_data, status.HTTP_403_FORBIDDEN})
# TODO Remove this code after confirming with Product team.
# This condition is not present in the Product story. Jai had put this condition in the BE story.
# If this check is required, it should be added to the serializer.
# Commenting it our for now. - Jai
            # new_password = request.data.get('password')
            # old_password = user_obj.password
            # if check_password(new_password, old_password):
            #     response_data = {'error': self.ERROR_PASSWORDS_SAME}
            #     return Response(response_data, status.HTTP_406_NOT_ACCEPTABLE)

            if serializer.is_valid():
                serializer.save()
                email_subject = 'Password Changed Notification'
                email_template = 'password_change_notification.html'
                context_data = {'email': user_obj.email}
                message_sent = send_email_helper(user_obj.email, email_subject, email_template, context_data)
                if not message_sent:
                    logger.info(f'ChangePasswordView: Change Password email not sent- {user_obj.email}')
                response_data = {'result': self.SUCCESS_PASSWORD_CHANGED}
                return Response(response_data, status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors['password']}, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error = self.ERROR_EXCEPTION
            logger.error(f'ChangePasswordView: {error}: {e}')
            response_data = {'error': e}
            return Response(response_data, status.HTTP_500_INTERNAL_SERVER_ERROR)
