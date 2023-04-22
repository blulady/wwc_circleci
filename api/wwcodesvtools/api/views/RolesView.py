from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from api.serializers.RoleSerializer import RoleSerializer
from api.models import Role


class RolesView(ListAPIView):
    """
    Returns a list of all roles.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Role.objects.all()
        return queryset

    def get_serializer_class(self):
        return RoleSerializer
