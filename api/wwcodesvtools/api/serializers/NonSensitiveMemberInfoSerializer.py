from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import User_Team
from api.serializers.UserTeamSerializer import UserTeamSerializer


class NonSensitiveMemberInfoSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='userprofile.status')
    highest_role = serializers.SerializerMethodField('get_highest_role')
    role_teams = serializers.SerializerMethodField('get_role_teams')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'status', 'highest_role', 'date_joined', 'role_teams']

    def get_highest_role(self, user):
        return User_Team.highest_role(user.id)

    def get_role_teams(self, user):
        userteam_qset = User_Team.objects.filter(user=user).order_by('-role_id')
        return UserTeamSerializer(userteam_qset, many=True).data
