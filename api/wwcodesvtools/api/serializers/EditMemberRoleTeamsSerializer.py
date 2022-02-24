from rest_framework import serializers
from api.models import Role, Team, User_Team
import logging

logger = logging.getLogger('django')


class EditMemberRoleTeamsSerializer(serializers.Serializer):
    role = serializers.CharField(max_length=20)
    teams = serializers.ListField(default=[], child=serializers.IntegerField(allow_null=True), allow_empty=True)

    def validate_role(self, value):
        if value not in Role.VALID_ROLES:
            raise serializers.ValidationError(f'Invalid Role: {value}')
        return value

    def validate_teams(self, value):
        if value:
            # check for duplicates, invalid team ids
            value_set = set(value)
            if len(value) != len(value_set):
                raise serializers.ValidationError('Invalid Teams: Duplicate values')
            teams = Team.objects.filter(id__in=value).values('id')
            teams_set = set(team['id'] for team in teams)
            invalid_teams = value_set.difference(teams_set)
            if invalid_teams:
                raise serializers.ValidationError(f'Invalid Teams: {invalid_teams} is not valid')
        return value

    def validate(self, data):
        teams = data.get('teams')
        role = data.get('role')
        role_obj = Role.objects.get(name=role)
        user_teams_roles = User_Team.objects.filter(user=self.instance, team_id__in=teams).values('role_id')
        roles_for_teams = [team_role['role_id'] for team_role in user_teams_roles]
        if len(roles_for_teams) >= 1 and roles_for_teams[0] != role_obj.id:
            raise serializers.ValidationError(f'Role other than {role} exists for one or more teams in request')
        return data

    def update(self, user_obj, validated_data):
        # edit member data in the db user_team table and the user profile table
        teams = validated_data.get('teams')
        role = validated_data.get('role')
        role_obj = Role.objects.get(name=role)
        logger.debug(f'EditMemberRoleTeamsSerializer: add_remove_user_role_team for list of teams= {teams}, role={role}, userId= {user_obj.id}')
        try:
            # first,remove the existing user team rows for the role
            User_Team.objects.filter(user=user_obj, role=role_obj).delete()
        except (User_Team.DoesNotExist) as e:
            logger.error(f'EditMemberRoleTeamsSerializer: No User role team rows found, none deleted {e}')
        if len(teams) > 0:
            # add the team rows for the user role
            user_team_objs = [User_Team(user=user_obj, role=role_obj, team_id=team) for team in teams]
            User_Team.objects.bulk_create(user_team_objs)
        else:
            # add a row with no team for the user role
            user_team = User_Team(user=user_obj, role=role_obj, team=None)
            user_team.save()
        return User_Team.objects.filter(user=user_obj)
