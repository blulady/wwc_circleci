from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.models import RegistrationToken
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
    USER_TOKEN_EXPIRED_MESSAGE = 'Token has expired'
    USER_TOKEN_ALREADY_USED_MESSAGE = 'Token is already used'
    VALID_TOKEN_MESSAGE = 'Toke is valid'
    NOT_FOUND = 'Not found.'

    permission_classes = [AllowAny]

    post_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Response sent successfully",
            examples={
                "application/json": {
                    'success': {
                        "status": ["VALID", "EXPIRED", "USED", "INVALID"],
                        "message": [VALID_TOKEN_MESSAGE, USER_TOKEN_EXPIRED_MESSAGE, USER_TOKEN_ALREADY_USED_MESSAGE, USER_TOKEN_MISMATCH_MESSAGE]
                    }
                }
            }
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Error not found",
            examples={
                "application/json": {
                    'detail': NOT_FOUND,
                }
            }
        ),
    }
    email_param = openapi.Parameter('email', openapi.IN_QUERY, description="Email", type=openapi.TYPE_STRING)
    token_param = openapi.Parameter('token', openapi.IN_QUERY, description="Token", type=openapi.TYPE_STRING)

    @swagger_auto_schema(responses=post_response_schema, manual_parameters=[email_param, token_param])
    def get(self, request):
        logger.debug(f'ValidateRegLinkView: {request.data}')
        user = get_object_or_404(User, email=self.request.query_params.get('email'))
        registration_token = get_object_or_404(RegistrationToken.objects.select_related('user'), token=self.request.query_params.get('token'))
        if (self._is_token_expired(registration_token.token)):
            return Response(self._build_response_data('EXPIRED', self.USER_TOKEN_EXPIRED_MESSAGE), status=status.HTTP_200_OK)
        response_message = None
        result = None
        if registration_token.user.email != user.email:
            response_message = self.USER_TOKEN_MISMATCH_MESSAGE
            result = 'INVALID'
        elif registration_token.used:
            response_message = self.USER_TOKEN_ALREADY_USED_MESSAGE
            result = 'USED'
        else:
            response_message = self.VALID_TOKEN_MESSAGE
            result = 'VALID'
        return Response(self._build_response_data(result, response_message), status=status.HTTP_200_OK)

    def _is_token_expired(self, token):
        token_datetime = datetime.strptime(token[-14:], '%Y%m%d%H%M%S')
        now_datetime = datetime.now()
        return (now_datetime - timedelta(seconds=settings.REGISTRATION_LINK_EXPIRATION) > token_datetime)

    def _build_response_data(self, result, message):
        return {'success': {'status': result,  'message': message}}
