# TODO delete this file after new resources api intergration is done.

# from rest_framework.response import Response
# from rest_framework import status
# from api.models import Resource
# from rest_framework.permissions import IsAuthenticated
# from api.permissions import CanEditResource
# from api.serializers.EditResourceSerializer import EditResourceSerializer
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from rest_framework.generics import GenericAPIView
# from django.shortcuts import get_object_or_404
# import logging


# logger = logging.getLogger('django')


# class EditResourceView(GenericAPIView):
#     """
#     Edits the edit_link,published_link for the resource
#     Takes the slug, edit_link and  published_link as parameters.
#     """
#     permission_classes = [IsAuthenticated & CanEditResource]
#     serializer_class = EditResourceSerializer

#     INTERNAL_SERVER_ERROR_EDITING_RESOURCE = 'Something went wrong while editing the Resource'
#     RESOURCE_EDITED_SUCCESSFULLY = 'Resource edited successfully'

#     post_response_schema = {
#         status.HTTP_200_OK: openapi.Response(
#             description="Resource edited successfully",
#             examples={
#                 "application/json": {
#                     'result': RESOURCE_EDITED_SUCCESSFULLY
#                 }
#             }
#         ),
#         status.HTTP_404_NOT_FOUND: openapi.Response(
#             description="Error not found",
#             examples={
#                 "application/json": {
#                     'detail': 'Not found.',
#                 }
#             }
#         ),
#         status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
#             description="Internal Server Error",
#             examples={
#                 "application/json": {
#                     'error': INTERNAL_SERVER_ERROR_EDITING_RESOURCE
#                 }
#             }
#         ),
#     }

#     @swagger_auto_schema(responses=post_response_schema)
#     def post(self, request, slug):
#         req = request.data
#         edit_link = req.get('edit_link')
#         published_link = req.get('published_link')
#         resource = get_object_or_404(Resource, slug=slug)
#         try:
#             logger.debug(f'edit_link={edit_link}  publishlink={published_link}')
#             serializer_resource = EditResourceSerializer(data={'edit_link': edit_link, 'published_link': published_link})
#             if serializer_resource.is_valid():
#                 setattr(resource, 'edit_link', edit_link)
#                 setattr(resource, 'published_link', published_link)
#                 resource.save()
#                 return Response({'result': self.RESOURCE_EDITED_SUCCESSFULLY}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': f'{serializer_resource.errors}'}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             logger.error(f'EditResourceView: Exception editing resource : {e}')
#             return Response({'error': f'{self.INTERNAL_SERVER_ERROR_EDITING_RESOURCE}: {e}',
#                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR})
