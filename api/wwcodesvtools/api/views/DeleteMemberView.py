from rest_framework.response import Response
from rest_framework import status
from api.permissions import CanDeleteMember
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

logger = logging.getLogger('django')


class DeleteMemberView(GenericAPIView):
    """
    Deletes the User and its related information from the database

    """
    permission_classes = [IsAuthenticated & CanDeleteMember]

    post_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="User deleted successfully",
            examples={
                "application/json": {
                    'result': 'User deleted successfully',
                }
            }
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Error not found",
            examples={
                "application/json": {
                    'detail': 'Not found.',
                }
            }
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            description="Internal Server Error",
            examples={
                "application/json": {
                     'error': 'Error deleting the User'
                }
            }
        ),
    }

    @swagger_auto_schema(responses=post_response_schema)
    def delete(self, request, id):
        user = get_object_or_404(User, id=id)
        try:
            # this deletes the User and all other objects having User as foreign key with 'ON DELETE CASCADE'
            user.delete()
            return Response({'result': 'User deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'DeleteMemberView:Error deleting the User: {e}')
            return Response({'error': 'Error deleting the User'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
