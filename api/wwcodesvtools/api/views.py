from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile, RegistrationToken
from .serializers import UserRegistrationSerializer, MailSenderSerializer, UserSerializer, RegistrationTokenSerializer, AddMemberSerializer, UserProfileSerializer
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .helper_functions import send_email_helper, generate_random_password
from uuid import uuid4
import logging
from django.db import transaction

logger = logging.getLogger('django')


class UserRegistrationView(GenericAPIView):
    USER_NOT_FOUND_ERROR_MESSAGE = 'Email does not exist in our invites system. You need to be invited to be able to register.'
    USER_ALREADY_ACTIVE_ERROR_MESSAGE = 'User is already registered and Active'
    USER_TOKEN_MISMATCH_ERROR_MESSAGE = 'Invalid token. Token in request does not match the token generated for this user.'
    TOKE_NOT_FOUND_ERROR_MESSAGE = 'Invalid token. Token does not exist in our system.'
    INTERNAL_SERVER_ERROR_MESSAGE = 'Something went wrong : {0}'
    EXPECTED_KEY_NOT_PRESENT_IN_REQUEST = 'Invalid Request. Key not present in request : {0}'
    ERROR_STATUS = {
        USER_NOT_FOUND_ERROR_MESSAGE: status.HTTP_404_NOT_FOUND,
        USER_ALREADY_ACTIVE_ERROR_MESSAGE: status.HTTP_400_BAD_REQUEST,
        USER_TOKEN_MISMATCH_ERROR_MESSAGE: status.HTTP_400_BAD_REQUEST,
        TOKE_NOT_FOUND_ERROR_MESSAGE: status.HTTP_404_NOT_FOUND,
        INTERNAL_SERVER_ERROR_MESSAGE: status.HTTP_500_INTERNAL_SERVER_ERROR,
        EXPECTED_KEY_NOT_PRESENT_IN_REQUEST: status.HTTP_400_BAD_REQUEST
    }

    serializer_class = UserRegistrationSerializer

    post_response_schema = {
        status.HTTP_201_CREATED: openapi.Response(
            description="User successfully created",
            examples={
                "application/json": {}
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
            user_queryset = User.objects.filter(email=req['user']['email'])
            result = self.__validate_request(user_queryset, req['token'])
            if 'error' in result:
                return Response({'error': result['error']}, status=result['status'])
            user = result['user']
            serializer = UserRegistrationSerializer(user, data=req['user'])
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
        return Response({'error': error}, status=res_status)

    def __validate_request(self, user_queryset, request_token):
        if not user_queryset.exists():
            return self.__build_error_result(self.USER_NOT_FOUND_ERROR_MESSAGE)
        user = user_queryset.first()
        if not user.userprofile.is_pending():
            return self.__build_error_result(self.USER_ALREADY_ACTIVE_ERROR_MESSAGE)
        token_qs = RegistrationToken.objects.filter(token=request_token, used=False)
        if token_qs.exists():
            token = token_qs.first()
            if not (token and token.user.email == user.email):
                return self.__build_error_result(self.USER_TOKEN_MISMATCH_ERROR_MESSAGE)
        else:
            return self.__build_error_result(self.TOKE_NOT_FOUND_ERROR_MESSAGE)
        return {'user': user, 'token': token}

    def __build_error_result(self, error):
        return {'error': error, 'status': self.ERROR_STATUS[error]}

    def __activate_user(self, userprofile):
        userprofile.activate()
        userprofile.save()

    def __mark_token_used(self, token):
        token.mark_as_used()
        token.save()


class MailSender(GenericAPIView):
    """
    Takes an email and sends email using a sample html template.
    """
    serializer_class = MailSenderSerializer

    post_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Email sent",
            examples={
                "application/json": {}
            }
        ),
        status.HTTP_502_BAD_GATEWAY: openapi.Response(
            description="Bad Gateway",
            examples={
                "application/json": {}
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    'error': 'Make sure all fields are entered and valid.'
                }
            }
        ),
    }

    @swagger_auto_schema(responses=post_response_schema)
    def post(self, request):
        serializer = MailSenderSerializer(data=request.data)
        if serializer.is_valid():
            to_email = serializer.data['email']
            subject = 'Welcome to WWCode-SV'
            template_file = 'welcome_sample.html'
            context_data = {"user": "UserName",
                            "registration_link": "https://login.yahoo.com/account/create",
                            "social_media_link": "https://twitter.com/womenwhocode"
                            }
            logger.debug(f"post: to_email: {to_email}")
        else:
            return Response({'error': 'Make sure all fields are entered and valid.'},
                            status=status.HTTP_400_BAD_REQUEST)

        message_sent = send_email_helper(
            to_email, subject, template_file, context_data)
        if message_sent:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_502_BAD_GATEWAY)


class AddMemberView(GenericAPIView):
    """
    Takes email, role and creates a new user in  pending status.

    """

    ERROR_UPDATING_REGISTRATION_TOKEN = 'Error updating registration token'
    ERROR_CREATING_MEMBER_USER = 'Error creating member user'
    ERROR_UPDATING_USER_PROFILE = 'Error updating user profile'
    NO_ERRORS = 'No Errors'

    serializer_class = AddMemberSerializer

    post_response_schema = {
        status.HTTP_201_CREATED: openapi.Response(
            description="Member user successfully created",
            examples={
                "application/json": {
                    'error': NO_ERRORS
                }
            }
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            description="Internal Server Error",
            examples={
                "application/json": {
                     'error': ERROR_CREATING_MEMBER_USER
                }
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    'error': "Invalid Role: accepted values are 'VOLUNTEER','LEADER','DIRECTOR"
                }
            }
        ),
    }

    @swagger_auto_schema(responses=post_response_schema)
    @transaction.atomic
    def post(self, request, format=None):
        res_status = None
        error = None
        logger.debug(f'AddMemberView: {request.data}')
        email = request.data.get('email')
        role = request.data.get('role')
        try:
            serializer_member = AddMemberSerializer(data={'email': email, 'role': role})
            if not serializer_member.is_valid():
                return Response({'error': serializer_member.errors}, status=status.HTTP_400_BAD_REQUEST)

            member_user = {
                "email": email,
                "username": email,
                "first_name": "new",
                "last_name": "user",
                "password": generate_random_password(8)
            }
            # generate random token as a 32-character hexadecimal string.
            rand_token = uuid4().hex
            logger.debug(f'AddMemberView: token : {rand_token}')
            registration_token = {
                "token": rand_token,
            }
            # create member user in the db
            # this will create rows in the user,userprofile and registrationToken tables
            # and update the role,status and role
            serializer_user = UserSerializer(data=member_user)
            if serializer_user.is_valid():
                # creating txn savepoint
                sid = transaction.savepoint()
                user_obj = serializer_user.save()
                res_profile_status = self.update_user_profile(user_obj.id, role)
                res_token_status = self.update_registration_token(user_obj.id, registration_token)
                if res_profile_status and res_token_status:
                    # all well,commit data to the db
                    transaction.savepoint_commit(sid)
                    error = self.NO_ERRORS
                    logger.info('AddMemberView: User data inserted successfully')
                    res_status = status.HTTP_201_CREATED
                else:
                    if not res_profile_status:
                        error = self.ERROR_UPDATING_USER_PROFILE
                    if not res_token_status:
                        error = self.ERROR_UPDATING_REGISTRATION_TOKEN
                    # something went wrong, don't commit data to db,rollback txn
                    transaction.savepoint_rollback(sid)
                    res_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                error = serializer_user.errors
                res_status = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            error = self.ERROR_CREATING_MEMBER_USER
            logger.error(f'AddMemberView: {error}: {e}')
            res_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response({'error': error}, status=res_status)

    def update_registration_token(self, user_id, registration_token):
        try:
            reg_token_row = RegistrationToken.objects.get(user_id=user_id)
            if reg_token_row:
                serializer_token = RegistrationTokenSerializer(reg_token_row, data=registration_token)
                if serializer_token.is_valid():
                    serializer_token.save()
                    return True
                else:
                    logger.error(f'AddMemberView:Error updating registration_token :{serializer_token.errors}')
                    return False
        except RegistrationToken.DoesNotExist as e:
            logger.error(f'AddMemberMember:Error updating registration_token : {e}')
            return False

    def update_user_profile(self, user_id, role):
        try:
            user_row = UserProfile.objects.get(user_id=user_id)
            data = {
                "status": UserProfile.PENDING,
                "role": role}
            logger.error(f'row {user_row.user_id} : {user_row.role}  : {user_row.status}')
            if user_row:
                serializer_profile = UserProfileSerializer(user_row, data=data)
                if serializer_profile.is_valid():
                    serializer_profile.save()
                    return True
                else:
                    logger.error(f'AddMemberView:Error updating user profile : {serializer_profile.errors}')
                    return False
        except UserProfile.DoesNotExist as e:
            logger.error(f'AddMemberView:Error updating user profile : {e}')
            return False
