from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.models import Invitee
from datetime import datetime, timedelta
from rest_framework import status
from django.conf import settings
from drf_yasg import openapi
import logging


logger = logging.getLogger('django')


class ValidateRegLinkView(GenericAPIView):
    """
    Takes email, token and validate the registration link.

    """
    USER_TOKEN_MISMATCH_MESSAGE = 'Invalid token. Token in request does not match the token generated for this user.'
    USER_TOKEN_EXPIRED_MESSAGE = 'Token is expired'
    USER_TOKEN_ALREADY_USED_MESSAGE = 'Token is already used'
    USER_ALREADY_ACTIVE_MESSAGE = 'There is already an active user associated with this email'
    USER_TOKEN_NOT_FOUND_ERROR_MESSAGE = 'Email/Token does not exist in our invites system. You need to be invited to be able to register.'
    VALID_TOKEN_MESSAGE = 'Token is valid'
    INTERNAL_SERVER_ERROR_MESSAGE = 'Something went wrong : {0}'

    permission_classes = [AllowAny]

    post_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Response sent successfully",
            examples={
                "application/json": {
                    'detail': {
                        "status": ["VALID", "EXPIRED", "INVALID", "ACTIVE"],
                        "message": [VALID_TOKEN_MESSAGE, USER_TOKEN_EXPIRED_MESSAGE, USER_TOKEN_MISMATCH_MESSAGE, USER_ALREADY_ACTIVE_MESSAGE]
                    }
                }
            }
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Error not found",
            examples={
                "application/json": {
                    'detail': USER_TOKEN_NOT_FOUND_ERROR_MESSAGE,
                }
            }
        ),
    }
    email_param = openapi.Parameter('email', openapi.IN_QUERY, description="Email", type=openapi.TYPE_STRING)
    token_param = openapi.Parameter('token', openapi.IN_QUERY, description="Token", type=openapi.TYPE_STRING)

    @swagger_auto_schema(responses=post_response_schema, manual_parameters=[email_param, token_param])
    def get(self, request):
        response_status = status.HTTP_200_OK
        error = None
        response_message = None
        result = None
        try:
            request_email = self.request.query_params.get('email')
            request_token = self.request.query_params.get('token')

            if (self._is_user_active(request_email)):
                response_message = self.USER_ALREADY_ACTIVE_MESSAGE
                result = 'ACTIVE'
                return Response(self._build_response_data(result, response_message), status=status.HTTP_200_OK)
            else:
                invitee = Invitee.objects.get(email=request_email)
                if (invitee.registration_token == request_token):
                    # email and token matched, check token expiration
                    if (not self._is_token_expired(request_token)):
                        # if the token is not expired
                        response_message = self.VALID_TOKEN_MESSAGE
                        result = 'VALID'
                    else:
                        # token expired
                        response_message = self.USER_TOKEN_EXPIRED_MESSAGE
                        result = 'EXPIRED'
                else:
                    # email and token mismatch. Invalid token for given email.
                    response_message = self.USER_TOKEN_MISMATCH_MESSAGE
                    result = 'INVALID'
        except Invitee.DoesNotExist:
            response_message = self.USER_TOKEN_NOT_FOUND_ERROR_MESSAGE
            result = 'NONEXISTENT'
            return Response(self._build_response_data(result, response_message), status=status.HTTP_404_NOT_FOUND)

            # return Response({'detail': self.USER_TOKEN_NOT_FOUND_ERROR_MESSAGE}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            error = self.INTERNAL_SERVER_ERROR_MESSAGE.format(e)
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if (error is None and response_status == status.HTTP_200_OK):
            return Response(self._build_response_data(result, response_message), status=status.HTTP_200_OK)
        return Response({'error': str(error)}, status=response_status)

    def _is_token_expired(self, token):
        token_datetime = datetime.strptime(token[-14:], '%Y%m%d%H%M%S')
        now_datetime = datetime.now()
        return (now_datetime - timedelta(seconds=settings.REGISTRATION_LINK_EXPIRATION) > token_datetime)

    def _build_response_data(self, result, message):
        return {'detail': {'status': result,  'message': message}}

    def _is_user_active(self, request_email):
        if User.objects.filter(email=request_email).exists():
            return True
        return False
