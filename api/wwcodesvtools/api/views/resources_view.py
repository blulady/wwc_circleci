
from api.models import Resource
from rest_framework import viewsets
from api.serializers.GetResourceSerializer import CompleteResourceSerializer, NonSensitiveResourceSerializer
from api.helper_functions import is_director_or_superuser
from rest_framework.permissions import IsAuthenticated
from api.permissions import CanEditResource
from api.serializers.EditResourceSerializer import EditResourceSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_serializer_class(self):
        try:
            is_user_director = is_director_or_superuser(self.request.user.id, self.request.user.is_superuser)
            if self.action == 'create':
                return CompleteResourceSerializer
            elif self.action in ['update', 'partial_update']:
                return EditResourceSerializer
            elif is_user_director:
                return CompleteResourceSerializer
            else:
                return NonSensitiveResourceSerializer
        except AttributeError:
            return "Attribute Exception: user id not found"

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action not in ['list', 'retrieve']:
            permission_classes.append(CanEditResource)
        return [permission() for permission in permission_classes]
