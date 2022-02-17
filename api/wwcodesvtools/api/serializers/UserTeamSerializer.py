from rest_framework import serializers
from api.models import User_Team


class UserTeamSerializer(serializers.ModelSerializer):

    team_id = serializers.ReadOnlyField(source='team.id')
    team_name = serializers.ReadOnlyField(source='team.name')
    role_name = serializers.ReadOnlyField(source='role.name')

    class Meta:
        model = User_Team
        fields = ('team_id', 'team_name', 'role_name')
