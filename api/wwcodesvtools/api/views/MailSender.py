from rest_framework.response import Response
from rest_framework import status
from api.serializers.MailSenderSerializer import MailSenderSerializer
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.helper_functions import send_email_helper
from rest_framework.permissions import IsAuthenticated
from api.permissions import CanSendEmail
import logging


logger = logging.getLogger('django')


class MailSender(GenericAPIView):
    """
    Takes an email and sends email using a sample html template.
    """
    permission_classes = [IsAuthenticated & CanSendEmail]
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
