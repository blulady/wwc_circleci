from api.models import Invitee
from api.serializers.InviteeSerializer import InviteeSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.permissions import CanAccessInvitee
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from uuid import uuid4
from api.helper_functions import send_email_helper
from datetime import datetime
import logging
from django.utils.http import urlencode
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

logger = logging.getLogger('django')


class InviteeViewSet(viewsets.ModelViewSet):
    # Exclude the invitees that has been accepted
    queryset = Invitee.objects.exclude(accepted=True)
    permission_classes = [IsAuthenticated & CanAccessInvitee]

    def get_serializer_class(self):
        if self.action == 'create':
            return None
        return InviteeSerializer

    ERROR_CREATING_INVITEE = 'Error creating invitee'
    ERROR_SENDING_EMAIL_NOTIFICATION = 'Error sending email notification to the invitee'
    INVITEE_CREATED_SUCCESSFULLY = 'Invitee Created Succesfully'

    post_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Invitee created and email sent successfully",
            examples={
                "application/json": {
                    'result': INVITEE_CREATED_SUCCESSFULLY,
                    'token': "0148f55a1f404363bf27dd8ebc9443c920210210220436"
                }
            }
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            description="Internal Server Error",
            examples={
                "application/json": {
                     'error': ERROR_CREATING_INVITEE
                }
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    'error': {
                        "email": ["Enter a valid email address."],
                        "role": ["Invalid pk \"n\" - object does not exist."]
                    }
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

    @swagger_auto_schema(request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                'email': openapi.Parameter('email', openapi.IN_BODY, description="Email", type=openapi.TYPE_STRING),
                                'role': openapi.Parameter('role', openapi.IN_BODY, description="Role", type=openapi.TYPE_INTEGER),
                                'message': openapi.Parameter('message', openapi.IN_BODY, description="Message", type=openapi.TYPE_STRING)
                             },
                         ),
                         operation_description="POST /invitee/",
                         responses=post_response_schema)
    def create(self, request):
        res_status = None
        error = None
        req = request.data
        logger.debug(f'InviteeViewSet Create : query params: {req}')
        email = req.get('email')
        role = req.get('role')
        message = req.get('message')

        try:
            timenow = datetime.now().strftime('%Y%m%d%H%M%S')
            # generate random token as a 32-character hexadecimal string and timestamp
            registration_token = str(uuid4().hex) + timenow
            created_by = request.user.id
            logger.debug(f'InviteeViewSet Create: token ={registration_token} : created_by ={created_by}')

            invitee_data = {
                "email": email,
                "message": message,
                "role": role,
                "status": 'INVITED',
                "registration_token": registration_token,
                "resent_counter": 0,
                "accepted": False,
                'created_at': timenow,
                'updated_at': timenow,
                'created_by': created_by
            }

            # create invitee in the invitee table
            serializer_invitee = InviteeSerializer(data=invitee_data)
            if serializer_invitee.is_valid():
                serializer_invitee.save()
                logger.info('InviteeViewSet Create: Invitee data inserted successfully')
                res_status = status.HTTP_201_CREATED
            else:
                error = serializer_invitee.errors
                res_status = status.HTTP_400_BAD_REQUEST

            # If invitee created successfully with no errors, then send email notification to the new invitee
            if (error is None and res_status == status.HTTP_201_CREATED):
                message_sent = self.send_email_notification(email, registration_token, message)
                if message_sent:
                    logger.info('InviteeViewSet Create : Invitee created and email sent successfully')
                    res_status = status.HTTP_200_OK
                else:
                    res_status = status.HTTP_502_BAD_GATEWAY
                    error = self.ERROR_SENDING_EMAIL_NOTIFICATION
        except Exception as e:
            error = self.ERROR_CREATING_INVITEE
            logger.error(f'InviteeViewSet Create: {error}: {e}')
            res_status = status.HTTP_500_INTERNAL_SERVER_ERROR

        if (error is None and res_status == status.HTTP_200_OK):
            return Response({'result': self.INVITEE_CREATED_SUCCESSFULLY, 'token': registration_token}, status=res_status)
        return Response({'error': error}, status=res_status)

    def send_email_notification(self, email, token, message):
        registration_link = f'{settings.FRONTEND_APP_URL}/register?{urlencode({"email": email, "token": token})}'
        logger.debug(f'InviteeViewSet Create: registrationt link {registration_link}')
        context_data = {"user": email,
                        "registration_link": registration_link,
                        "optional_message": message
                        }
        return send_email_helper(
            email, 'Invitation to Join Chapter Portal, Action Required', 'new_member_email.html', context_data)
