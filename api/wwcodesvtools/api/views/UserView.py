from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from api.serializers.NameChangeSerializer import NameChangeSerializer
from api.helper_functions import send_email_helper
from drf_yasg import openapi


import logging


logger = logging.getLogger('django')


class UserView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NameChangeSerializer

    ERROR_SETTING_NEW_NAME = 'Either name was blank or name length not in range of 1-50 characters'
    NAME_CHANGE_SUCCESSFULLY = 'Name change was successful'
    CANNOT_UPDATE_PENDING_MEMBER = "Cannot update user with status Pending"

    post_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Set new password successfully",
            examples={
                "application/json": {
                    'success': NAME_CHANGE_SUCCESSFULLY
                }
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Name Change Error",
            examples={
                "application/json": {
                    'error': ERROR_SETTING_NEW_NAME
                }
            }
        ),
    }

    def patch(self, request):
        current_user = self.request.user
        curr_id = current_user.id
        user_obj = get_object_or_404(User, id=curr_id)
        userprofile_obj = user_obj.userprofile

        try:
            if userprofile_obj.is_pending():
                response_data = {'error': self.CANNOT_UPDATE_PENDING_MEMBER}
                res_status = status.HTTP_403_FORBIDDEN
                return Response(response_data, status=res_status)

# TODO Try to use UserSerializer and delete NameChangeSerializer
            name_serializer = NameChangeSerializer(user_obj, data=request.data)
            if name_serializer.is_valid():
                name_serializer.save()
                message_sent = self.send_email_notification(user_obj.email, user_obj.first_name, user_obj.last_name)
                if message_sent:
                    logger.info('UserView: Name change confirmation email sent successfully')
                response_data = {'success': self.NAME_CHANGE_SUCCESSFULLY}
                res_status = status.HTTP_200_OK
            else:
                response_data = {'error': self.ERROR_SETTING_NEW_NAME}
                res_status = status.HTTP_400_BAD_REQUEST
            return Response(response_data, res_status)
        except Exception as e:
            res_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response({'error': str(e)}, res_status)

    def send_email_notification(self, email, fn, ln):
        context_data = {"first_name": fn, "last_name": ln}
        return send_email_helper(email, 'Name Change Notification', 'request_name_change.html', context_data)
