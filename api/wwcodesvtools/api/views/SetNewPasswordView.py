from api.serializers.SetNewPasswordSerializer import SetNewPasswordSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from api.helper_functions import send_email_helper
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from rest_framework import status
import logging

logger = logging.getLogger('django')


class SetNewPasswordView(GenericAPIView):
    """
    Set new password and sends an email notifying the user's password change.

    """

    ERROR_SENDING_EMAIL_NOTIFICATION = 'Error sending password change notification'
    ERROR_SETTING_NEW_PASSWORD = 'Error setting new password'
    INVALID_LINK = 'The reset link is invalid'
    PASSWORD_RESET_SUCCESSFULLY = 'Password reset successfully'

    permission_classes = [AllowAny]
    serializer_class = SetNewPasswordSerializer

    post_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Set new password successfully",
            examples={
                "application/json": {
                    'success': PASSWORD_RESET_SUCCESSFULLY
                }
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    "error": {
                        'password': ["This field is required.",
                                     "This field may not be blank.",
                                     "Ensure this field has at least 8 characters.",
                                     "Password should have at least one upper case letter",
                                     "Password should have at least one lower case letter",
                                     "Password should have at least one number"
                                     ],
                        'token': ["This field is required.",
                                  "This field may not be blank."]
                    }
                }
            }
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            description="Unauthorized",
            examples={
                "application/json": {
                     'error': INVALID_LINK
                }
            }
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Not Found",
            examples={
                "application/json": {
                     'detail': "Not found."
                }
            }
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            description="Internal Server Error",
            examples={
                "application/json": {
                    'error': ERROR_SETTING_NEW_PASSWORD
                }
            }
        ),
        status.HTTP_502_BAD_GATEWAY: openapi.Response(
            description="Bad Gateway",
            examples={
                "application/json": {
                    'error': ERROR_SENDING_EMAIL_NOTIFICATION
                }
            }
        ),
    }

    @swagger_auto_schema(responses=post_response_schema)
    def patch(self, request):
        res_status = None
        error = None
        logger.debug(f'SetNewPasswordView: {request.data}')
        password = request.data.get('password')
        email = request.data.get('email')
        token = request.data.get('token')
        user = get_object_or_404(User, email=email)

        try:
            serializer = SetNewPasswordSerializer(data=request.data)
            if serializer.is_valid():
                if not PasswordResetTokenGenerator().check_token(user, token):
                    error = self.INVALID_LINK
                    res_status = status.HTTP_401_UNAUTHORIZED
                else:
                    user.set_password(password)
                    user.save()
                    res_status = status.HTTP_200_OK
            else:
                error = serializer.errors
                res_status = status.HTTP_400_BAD_REQUEST

            if (error is None and res_status == status.HTTP_200_OK):
                message_sent = self.send_email_notification(user.email)
                if message_sent:
                    logger.info('SetNewPasswordView: Reset password confirmation email sent successfully')
                    res_status = status.HTTP_200_OK
                else:
                    res_status = status.HTTP_502_BAD_GATEWAY
                    error = self.ERROR_SENDING_EMAIL_NOTIFICATION
        except Exception as e:
            error = self.ERROR_SETTING_NEW_PASSWORD
            logger.error(f'SetNewPasswordView: {error}: {e}')
            res_status = status.HTTP_500_INTERNAL_SERVER_ERROR

        if (error is None and res_status == status.HTTP_200_OK):
            return Response({'success': self.PASSWORD_RESET_SUCCESSFULLY}, status=res_status)
        return Response({'error': error}, status=res_status)

    def send_email_notification(self, email):
        context_data = {"email": email}
        return send_email_helper(email, 'Password Change Notification', 'password_change_notification.html', context_data)
