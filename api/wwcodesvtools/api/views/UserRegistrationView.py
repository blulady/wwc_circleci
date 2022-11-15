from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from api.models import RegistrationToken
from api.serializers.UserRegistrationSerializer import UserRegistrationSerializer
from api.serializers.UserActivationSerializer import UserActivationSerializer
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta
from django.conf import settings
import logging


logger = logging.getLogger('django')


class UserRegistrationView(GenericAPIView):
    """
    Takes email, first_name, last_name, password, token and activates the user.
    User status is changed from Pending to Active.

    """
    USER_NOT_FOUND_ERROR_MESSAGE = 'Email does not exist in our invites system. You need to be invited to be able to register.'
    USER_ALREADY_ACTIVE_ERROR_MESSAGE = 'User is already registered and Active'
    USER_TOKEN_MISMATCH_ERROR_MESSAGE = 'Invalid token. Token in request does not match the token generated for this user.'
    TOKEN_NOT_FOUND_ERROR_MESSAGE = 'Invalid token. Token does not exist in our system.'
    INTERNAL_SERVER_ERROR_MESSAGE = 'Something went wrong : {0}'
    EXPECTED_KEY_NOT_PRESENT_IN_REQUEST = 'Invalid Request. Key not present in request : {0}'
    USER_TOKEN_EXPIRED_ERROR_MESSAGE = 'Expired token. Unable to register the user'
    USER_ACTIVATED_SUCCESSFULLY = 'User Activated Succesfully'
    ERROR_STATUS = {
        USER_NOT_FOUND_ERROR_MESSAGE: status.HTTP_404_NOT_FOUND,
        USER_ALREADY_ACTIVE_ERROR_MESSAGE: status.HTTP_400_BAD_REQUEST,
        USER_TOKEN_MISMATCH_ERROR_MESSAGE: status.HTTP_400_BAD_REQUEST,
        TOKEN_NOT_FOUND_ERROR_MESSAGE: status.HTTP_404_NOT_FOUND,
        INTERNAL_SERVER_ERROR_MESSAGE: status.HTTP_500_INTERNAL_SERVER_ERROR,
        EXPECTED_KEY_NOT_PRESENT_IN_REQUEST: status.HTTP_400_BAD_REQUEST,
        USER_TOKEN_EXPIRED_ERROR_MESSAGE: status.HTTP_400_BAD_REQUEST
    }

    permission_classes = [AllowAny]
    serializer_class = UserActivationSerializer

    post_response_schema = {
        status.HTTP_201_CREATED: openapi.Response(
            description="User Activated Successfully",
            examples={
                "application/json": {
                    "result": USER_ACTIVATED_SUCCESSFULLY
                }
            }
        ),
        ERROR_STATUS[EXPECTED_KEY_NOT_PRESENT_IN_REQUEST]: openapi.Response(
            description="Key error: Key not present",
            examples={
                "application/json": {
                    "error": EXPECTED_KEY_NOT_PRESENT_IN_REQUEST.format("email not present")
                }
            }
        ),
    }

    @swagger_auto_schema(responses=post_response_schema)
    def post(self, request):
        res_status = None
        error = None
        req = request.data
        try:
            user_queryset = User.objects.filter(email=req['email'])
            result = self.__validate_request(user_queryset, req['token'])
            if 'error' in result:
                return Response({'error': result['error']}, status=result['status'])
            user = result['user']
            serializer = UserRegistrationSerializer(user, data={'email': req['email'], 'first_name': req['first_name'],
                                                                'last_name': req['last_name'], 'password': req['password']})
            if serializer.is_valid():
                serializer.save()
                self.__activate_user(user.userprofile)
                self.__mark_token_used(result['token'])
                res_status = status.HTTP_201_CREATED
            else:
                error = serializer.errors
                res_status = status.HTTP_400_BAD_REQUEST
        except KeyError as key_error:
            error = self.EXPECTED_KEY_NOT_PRESENT_IN_REQUEST.format(key_error)
            res_status = self.ERROR_STATUS[self.EXPECTED_KEY_NOT_PRESENT_IN_REQUEST]
        except Exception as e:
            error = self.INTERNAL_SERVER_ERROR_MESSAGE.format(e)
            res_status = self.ERROR_STATUS[self.INTERNAL_SERVER_ERROR_MESSAGE]
        if (error is None and res_status == status.HTTP_201_CREATED):
            return Response({'result': self.USER_ACTIVATED_SUCCESSFULLY}, status=res_status)
        return Response({'error': str(error)}, status=res_status)

    def __validate_request(self, user_queryset, request_token):
        if not user_queryset.exists():
            return self.__build_error_result(self.USER_NOT_FOUND_ERROR_MESSAGE)
        user = user_queryset.first()
        if not user.userprofile.is_pending():
            return self.__build_error_result(self.USER_ALREADY_ACTIVE_ERROR_MESSAGE)
        # check for valid unexpired registration token
        token_datetime = datetime.strptime(request_token[-14:], '%Y%m%d%H%M%S')
        now_datetime = datetime.now()
        if not (now_datetime - timedelta(seconds=settings.REGISTRATION_LINK_EXPIRATION) <= token_datetime):
            return self.__build_error_result(self.USER_TOKEN_EXPIRED_ERROR_MESSAGE)
        token_qs = RegistrationToken.objects.filter(token=request_token, used=False)
        if token_qs.exists():
            token = token_qs.first()
            if not (token and token.user.email == user.email):
                return self.__build_error_result(self.USER_TOKEN_MISMATCH_ERROR_MESSAGE)
        else:
            return self.__build_error_result(self.TOKEN_NOT_FOUND_ERROR_MESSAGE)
        return {'user': user, 'token': token}

    def __build_error_result(self, error):
        return {'error': error, 'status': self.ERROR_STATUS[error]}

    def __activate_user(self, userprofile):
        userprofile.activate()
        userprofile.save()

    def __mark_token_used(self, token):
        token.mark_as_used()
        token.save()
