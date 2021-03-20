from rest_framework import serializers
from api.models import User_Team


class GetUserTeamSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='team.id')
    name = serializers.ReadOnlyField(source='team.name')

    class Meta:
        model = User_Team
        fields = ('id', 'name')
