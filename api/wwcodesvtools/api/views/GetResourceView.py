# TODO delete this file after new resources api intergration is done.

# from api.models import Resource
# from rest_framework.generics import RetrieveAPIView
# from rest_framework.permissions import IsAuthenticated
# from api.helper_functions import is_director_or_superuser
# from api.serializers.GetResourceSerializer import CompleteResourceSerializer, NonSensitiveResourceSerializer

# import logging


# logger = logging.getLogger('django')


# class GetResourceView(RetrieveAPIView):
#     """
#     Takes the slug as a parameter and gives back the document link.
#     """
#     permission_classes = [IsAuthenticated]
#     queryset = Resource.objects.all()
#     lookup_field = 'slug'

#     def get_serializer_class(self):
#         if is_director_or_superuser(self.request.user.id, self.request.user.is_superuser):
#             return CompleteResourceSerializer
#         return NonSensitiveResourceSerializer
