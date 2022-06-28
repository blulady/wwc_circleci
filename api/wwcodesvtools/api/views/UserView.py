from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from api.serializers.NameChangeSerializer import NameChangeSerializer


import logging


logger = logging.getLogger('django')


class UserView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NameChangeSerializer

    ERROR_SETTING_NEW_NAME = 'Error: either name was blank or name length not in range of 1-50 characters'
    NAME_CHANGE_SUCCESSFULLY = 'Name change was successful'

# TODO Add the swagger_auto_schema
    def patch(self, request):
        res_status = "res status not set"
        current_user = self.request.user
        curr_id = current_user.id
        user_obj = get_object_or_404(User, id=curr_id)
        userprofile_obj = user_obj.userprofile

        try:
            if userprofile_obj.is_pending():
                response_data = {'error': "User status is Pending. Name cannot be changed"}
                res_status = status.HTTP_403_FORBIDDEN
                return Response({response_data, res_status})

# TODO Try to use UserSerializer and delete NameChangeSerializer
            name_serializer = NameChangeSerializer(user_obj, data=request.data)
            if name_serializer.is_valid():
                name_serializer.save()
                # TODO commnet this after fixing it
                # self.notify_user(user_obj)
                response_data = self.NAME_CHANGE_SUCCESSFULLY
                res_status = status.HTTP_200_OK
            else:
                response_data = self.ERROR_SETTING_NEW_NAME
                res_status = status.HTTP_400_BAD_REQUEST

            return Response(response_data, res_status)
        except Exception as e:
            res_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(e, res_status)

    def notify_user(self, user_info):
        subj = "Requested Name Change"
        msg = "The request to change your name was successful"
        from_whom = "wwcode.sv.noreply@gmail.com"
        to_user = [user_info.email]
        # TODO Use # send_email_helper function from helper_functions
        send_result = send_mail(subj, msg, from_whom, to_user, fail_silently=False)
        if not send_result:
            raise Warning("email notification failed")
