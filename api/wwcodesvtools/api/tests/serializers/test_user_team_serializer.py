from django.test import TransactionTestCase
from api.serializers.UserTeamSerializer import UserTeamSerializer
from api.models import User_Team


class UserTeamSerializerTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']

    def test_serializer_data_has_role_name(self):
        user_role_team = User_Team.objects.get(user_id=1)
        serializer = UserTeamSerializer(user_role_team)
        self.assertEqual(serializer.data['role_name'], user_role_team.role.name)

    def test_serializer_data_has_team_name(self):
        user_role_team = User_Team.objects.get(user_id=1)
        serializer = UserTeamSerializer(user_role_team)
        self.assertEqual(serializer.data['team_name'], user_role_team.team.name)

    def test_serializer_data_has_team_id(self):
        user_role_team = User_Team.objects.get(user_id=1)
        serializer = UserTeamSerializer(user_role_team)
        self.assertEqual(serializer.data['team_id'], user_role_team.team.id)
