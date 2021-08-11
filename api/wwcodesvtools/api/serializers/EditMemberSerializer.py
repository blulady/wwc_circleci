from rest_framework import serializers
from api.models import UserProfile, Role, Team


class EditMemberSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=20)
    role = serializers.CharField(max_length=20)
    teams = serializers.ListField(default=[], child=serializers.IntegerField(allow_null=True), allow_empty=True)

    def validate_role(self, value):
        if value not in Role.VALID_ROLES:
            raise serializers.ValidationError("Invalid Role: accepted values are 'VOLUNTEER','LEADER','DIRECTOR'")
        return value

    def validate_status(self, value):
        valid_status = [UserProfile.ACTIVE, UserProfile.INACTIVE]
        if value not in valid_status:
            raise serializers.ValidationError("Invalid Status: accepted values are 'ACTIVE','INACTIVE'")
        return value

    def validate_teams(self, value):
        if value:
            # check for duplicates, invalid team ids
            value_set = set(value)
            if len(value) != len(value_set):
                raise serializers.ValidationError("Invalid Teams: Duplicate values")
            teams = Team.objects.filter(id__in=value).values('id')
            teams_set = set(team['id'] for team in teams)
            invalid_teams = value_set.difference(teams_set)
            if invalid_teams:
                raise serializers.ValidationError(f'Invalid Teams: {invalid_teams} is not valid')
        return value
