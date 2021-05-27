from api.serializers.RequestPasswordResetSerializer import RequestPasswordResetSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from api.helper_functions import send_email_helper
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework import status
from django.conf import settings
from drf_yasg import openapi
import logging
from django.utils.http import urlencode


logger = logging.getLogger('django')


class RequestPasswordResetView(GenericAPIView):
    """
    Takes email and sends an email notification with the password reset link.

    """

    ERROR_SENDING_EMAIL_NOTIFICATION = 'Error sending reset email notification to the user'
    ERROR_REQUEST_RESET = 'Error in request for password reset'
    ERROR_MAKING_RESET_TOKEN = 'Error generating the reset token'
    RESET_LINK_SENT_SUCCESSFULLY = 'We have sent you a link to reset your password'

    permission_classes = [AllowAny]
    serializer_class = RequestPasswordResetSerializer

    post_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Reset email sent successfully",
            examples={
                "application/json": {
                    'success': RESET_LINK_SENT_SUCCESSFULLY
                }
            }
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            description="Internal Server Error",
            examples={
                "application/json": {
                     'error': ERROR_REQUEST_RESET
                }
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    'error': "Email does not exist"
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
    def post(self, request):
        res_status = None
        error = None
        logger.debug(f'RequestPasswordResetView: {request.data}')
        email = request.data.get('email')

        try:
            serializer = RequestPasswordResetSerializer(data={'email': email})
            if serializer.is_valid():
                user = User.objects.get(email=email)
                token = PasswordResetTokenGenerator().make_token(user)
                if not token:
                    error = self.ERROR_MAKING_RESET_TOKEN
                res_status = status.HTTP_201_CREATED
            else:
                error = serializer.errors
                res_status = status.HTTP_400_BAD_REQUEST

            if (error is None and res_status == status.HTTP_201_CREATED):
                message_sent = self.send_email_notification(email, user.first_name, user.last_name, token)
                if message_sent:
                    logger.info('RequestPasswordResetView: Reset email sent successfully')
                    res_status = status.HTTP_200_OK
                else:
                    res_status = status.HTTP_502_BAD_GATEWAY
                    error = self.ERROR_SENDING_EMAIL_NOTIFICATION
        except Exception as e:
            error = self.ERROR_REQUEST_RESET
            logger.error(f'RequestPasswordResetView: {error}: {e}')
            res_status = status.HTTP_500_INTERNAL_SERVER_ERROR

        if (error is None and res_status == status.HTTP_200_OK):
            return Response({'success': self.RESET_LINK_SENT_SUCCESSFULLY}, status=res_status)
        return Response({'error': error}, status=res_status)

    def send_email_notification(self, email, first_name, last_name, token):
        # password_reset_confirm = settings.FRONTEND_APP_URL + "/password/reset?" + urlencode({'email': email, 'token': token})

        password_reset_confirm = f'{settings.FRONTEND_APP_URL}/password/reset?{urlencode({"email": email, "token": token})}'
        logger.debug(f'RequestPasswordResetView: password_reset_confirm: {password_reset_confirm}')
        context_data = {"user": f'{first_name} {last_name}',
                        "password_reset_confirm": password_reset_confirm
                        }
        return send_email_helper(email, 'Password Reset Requested', 'request_reset_password.html', context_data)
