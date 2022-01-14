from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import User_Team
from api.serializers.GetUserTeamSerializer import GetUserTeamSerializer


class NonSensitiveMemberInfoSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')
    role = serializers.SerializerMethodField('get_role')
    teams = serializers.SerializerMethodField('get_teams')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'status', 'role', 'date_joined', 'teams']

    def get_status(self, user):
        return user.userprofile.status

    def get_role(self, user):
        role = User_Team.highest_role(user.id)
        return role

    def get_teams(self, user):
        userteam_qset = User_Team.objects.filter(user=user)
        return GetUserTeamSerializer(userteam_qset, many=True).data
