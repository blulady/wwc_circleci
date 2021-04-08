from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from api.serializers.TeamSerializer import TeamSerializer
from api.models import Team


class GetTeamsView(ListAPIView):
    """
    Returns a list of all teams.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Team.objects.all()
        return queryset

    def get_serializer_class(self):
        return TeamSerializer
