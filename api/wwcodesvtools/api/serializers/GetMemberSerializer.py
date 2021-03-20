from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import User_Team
from api.serializers.GetUserTeamSerializer import GetUserTeamSerializer


class GetMemberSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')
    role = serializers.SerializerMethodField('get_role')
    teams = serializers.SerializerMethodField('get_teams')

    class Meta(object):
        model = User
        fields = ['id', 'first_name', 'last_name', 'status', 'role', 'date_joined', 'teams']

    def get_status(self, obj):
        return obj.userprofile.status

    def get_role(self, obj):
        return obj.userprofile.role

    def get_teams(self, obj):
        userteam_qset = User_Team.objects.filter(user=obj)
        return GetUserTeamSerializer(userteam_qset, many=True).data
