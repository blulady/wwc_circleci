from rest_framework.response import Response
from rest_framework import status
from api.models import UserProfile, RegistrationToken
from api.serializers import UserSerializer, RegistrationTokenSerializer, AddMemberSerializer, UserProfileSerializer
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.helper_functions import generate_random_password
from uuid import uuid4
from django.db import transaction
from rest_framework.permissions import AllowAny
from django.conf import settings
from api.helper_functions import send_email_helper
import logging


logger = logging.getLogger('django')


class AddMemberView(GenericAPIView):
    """
    Takes email,role,message and creates a new user in pending status.
    Sends email notification with the registration link to the new user.

    """

    ERROR_UPDATING_REGISTRATION_TOKEN = 'Error updating registration token'
    ERROR_CREATING_MEMBER_USER = 'Error creating member user'
    ERROR_UPDATING_USER_PROFILE = 'Error updating user profile'
    ERROR_SENDING_EMAIL_NOTIFICATION = 'Error sending email notification to the member user'
    NO_ERRORS = 'No Errors'

    permission_classes = [AllowAny]
    serializer_class = AddMemberSerializer

    post_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Member User created and email sent successfully",
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
    @transaction.atomic
    def post(self, request, format=None):
        res_status = None
        error = None
        logger.debug(f'AddMemberView: {request.data}')
        email = request.data.get('email')
        role = request.data.get('role')
        message = request.data.get('message')

        try:
            serializer_member = AddMemberSerializer(data={'email': email, 'role': role, 'message': message})
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

            # If user created successfully with no errors, then send email notification to the new member user
            if (error == self.NO_ERRORS and res_status == status.HTTP_201_CREATED):
                message_sent = self.send_email_notification(email, rand_token, message)
                if message_sent:
                    logger.info('AddMemberView: Member User created and email sent successfully')
                    res_status = status.HTTP_200_OK
                    error = self.NO_ERRORS
                else:
                    res_status = status.HTTP_502_BAD_GATEWAY
                    error = self.ERROR_SENDING_EMAIL_NOTIFICATION

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

    def send_email_notification(self, email, token, message):
        context_data = {"user": email,
                        "registration_link": settings.FRONTEND_APP_URL+"/register?email="+email+"&token="+token,
                        "optional_message": message
                        }
        return send_email_helper(
            email, 'Invitation to Join Chapter Portal, Action Required', 'new_member_email.html', context_data)
