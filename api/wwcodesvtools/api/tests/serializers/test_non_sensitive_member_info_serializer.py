from django.test import TransactionTestCase
from api.serializers.NonSensitiveMemberInfoSerializer import NonSensitiveMemberInfoSerializer
from api.serializers.UserTeamSerializer import UserTeamSerializer
from django.contrib.auth.models import User

from api.models import Role, User_Team, UserProfile


class NonSensitiveMemberInfoSerializerTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']

    def test_data_has_highest_role_for_given_user(self):
        user_with_multiple_roles = User.objects.get(id=9)
        serializer = NonSensitiveMemberInfoSerializer(user_with_multiple_roles)
        self.assertEqual(serializer.data['highest_role'], Role.DIRECTOR)

    def test_data_has_user_attributes_for_given_user(self):
        user = User.objects.get(id=2)
        serializer = NonSensitiveMemberInfoSerializer(user)
        self.assertEqual(serializer.data['first_name'], user.first_name)
        self.assertEqual(serializer.data['last_name'], user.last_name)
        self.assertEqual(serializer.data['id'], user.id)
        self.assertEqual(serializer.data['date_joined'], user.date_joined.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

    def test_data_has_status_for_given_user(self):
        user = User.objects.get(id=2)
        serializer = NonSensitiveMemberInfoSerializer(user)
        self.assertEqual(serializer.data['status'], UserProfile.ACTIVE)

    def test_data_has_role_teams_details_for_given_user(self):
        user_with_multiple_teams = User.objects.get(id=2)
        userteam_qset = User_Team.objects.filter(user=user_with_multiple_teams)
        expected_user_role_teams = UserTeamSerializer(userteam_qset, many=True)
        serializer = NonSensitiveMemberInfoSerializer(user_with_multiple_teams)
        self.assertListEqual(serializer.data['role_teams'], expected_user_role_teams.data)

    def test_data_has_first_role_teams_correspond_to_highest_role(self):
        user_with_multiple_roles = 9
        highest_role = User_Team.highest_role(user_with_multiple_roles)
        serializer = NonSensitiveMemberInfoSerializer(User.objects.get(id=user_with_multiple_roles))
        first_role_team = serializer.data['role_teams'][0]
        self.assertEqual(first_role_team['role_name'], highest_role)
