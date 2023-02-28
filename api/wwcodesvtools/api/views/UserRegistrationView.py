from rest_framework.response import Response
from rest_framework import status
from api.models import Invitee, User_Team, Role
from api.serializers.UserActivationSerializer import UserActivationSerializer
from api.serializers.UserSerializer import UserSerializer
from api.helper_functions import is_token_expired
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.db import transaction
import logging
logger = logging.getLogger('django')


class UserRegistrationView(GenericAPIView):
    """
    Takes email, first_name, last_name, password, token and registers the user.
    A new User is created and its associated(used) invitee is deleted.

    """
    USER_NOT_FOUND_ERROR_MESSAGE = 'Email does not exist in our invites system. You need to be invited to be able to register.'
    USER_TOKEN_MISMATCH_ERROR_MESSAGE = 'Invalid token. Token in request does not match the token generated for this user.'
    INTERNAL_SERVER_ERROR_MESSAGE = 'Something went wrong : {0}'
    EXPECTED_KEY_NOT_PRESENT_IN_REQUEST = 'Invalid Request. Key not present in request : {0}'
    USER_TOKEN_EXPIRED_ERROR_MESSAGE = 'Expired token. Unable to register the user'
    USER_REGISTERED_SUCCESSFULLY = 'User Registered Successfully'
    ERROR_CREATING_USERTEAM_ROLE = 'Error creating user team role'
    ERROR_DELETING_USED_INVITEE = 'Error deleting used invitee'

    ERROR_STATUS = {
        USER_NOT_FOUND_ERROR_MESSAGE: status.HTTP_404_NOT_FOUND,
        USER_TOKEN_MISMATCH_ERROR_MESSAGE: status.HTTP_400_BAD_REQUEST,
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
                    "result": USER_REGISTERED_SUCCESSFULLY
                }
            }
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            description="Internal Server Error",
            examples={
                "application/json": {
                     'error': INTERNAL_SERVER_ERROR_MESSAGE
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
        response_status = None
        error = None
        request_data = request.data

        try:
            invitee = Invitee.objects.get(email=request_data['email'])
            request_token = request_data['token']
            if (invitee.registration_token == request_token):
                # email and token matched, check token expiration
                if (not is_token_expired(self, request_token)):
                    user_serializer = UserSerializer(data={'email': request_data['email'], 'username': request_data['email'], 'first_name': request_data['first_name'],
                                                           'last_name': request_data['last_name'], 'password': request_data['password']})
                    # if the token is not expired and all the fields are valid,
                    # create a new user, a new user-team-role and delete the invitee
                    if user_serializer.is_valid():
                        # creating txn savepoint
                        sid = transaction.savepoint()
                        user_obj = user_serializer.save()
                        res_role_status = self.create_user_team_role(user_obj, invitee.role)
                        res_delete_invitee = self.delete_invitee(invitee)

                        if res_role_status and res_delete_invitee:
                            # all well,commit data to the db
                            transaction.savepoint_commit(sid)
                            logger.info('UserRegistrationView: User data inserted successfully')
                            response_status = status.HTTP_201_CREATED
                        else:
                            if not res_role_status:
                                error = self.ERROR_CREATING_USERTEAM_ROLE
                            if not res_delete_invitee:
                                error = self.ERROR_DELETING_USED_INVITEE
                            # something went wrong, don't commit data to db, rollback txn
                            transaction.savepoint_rollback(sid)
                            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
                    else:
                        # invalid data
                        error = user_serializer.errors
                        response_status = status.HTTP_400_BAD_REQUEST
                else:
                    # token expired
                    error = self.USER_TOKEN_EXPIRED_ERROR_MESSAGE
                    response_status = self.ERROR_STATUS[error]
            else:
                # email and token mismatch. Invalid token for given email.
                error = self.USER_TOKEN_MISMATCH_ERROR_MESSAGE
                response_status = self.ERROR_STATUS[error]

        except Invitee.DoesNotExist:
            error = self.USER_NOT_FOUND_ERROR_MESSAGE
            response_status = self.ERROR_STATUS[error]
        except KeyError as key_error:
            error = self.EXPECTED_KEY_NOT_PRESENT_IN_REQUEST.format(key_error)
            response_status = self.ERROR_STATUS[self.EXPECTED_KEY_NOT_PRESENT_IN_REQUEST]
        except Exception as e:
            error = self.INTERNAL_SERVER_ERROR_MESSAGE.format(e)
            response_status = self.ERROR_STATUS[self.INTERNAL_SERVER_ERROR_MESSAGE]

        if (error is None and response_status == status.HTTP_201_CREATED):
            return Response({'result': self.USER_REGISTERED_SUCCESSFULLY}, status=response_status)
        return Response({'error': str(error)}, status=response_status)

    def create_user_team_role(self, user_obj, role):
        try:
            role_row = Role.objects.get(name=role)
            userteam_row = User_Team(user=user_obj, role=role_row)
            userteam_row.save()
            return True
        except Exception as e:
            logger.error(f'AddMemberView:Error creating user team role : {e}')
            return False

    def delete_invitee(self, invitee):
        try:
            invitee.delete()
            return True
        except Exception as e:
            logger.error(f'UserRegistrationView:Error deleting used invitee : {e}')
            return False
