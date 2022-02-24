from django.test import TransactionTestCase
from api.serializers.EditMemberRoleTeamsSerializer import EditMemberRoleTeamsSerializer
from api.models import Role
from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import User_Team, Team


class EditMemberRoleTeamsSerializerTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['roles_data.json', 'teams_data.json', 'users_data.json']
    serializer = EditMemberRoleTeamsSerializer()
    role = None
    user = None
    old_teams = None

    def test_validate_role_returns_role_object_for_valid_role_in_data(self):
        serializer = EditMemberRoleTeamsSerializer()
        value = serializer.validate_role(Role.VOLUNTEER)
        self.assertEqual(value, Role.VOLUNTEER)

    def test_validate_role_raise_serializer_error_for_invalid_role(self):
        serializer = EditMemberRoleTeamsSerializer()

        with self.assertRaises(serializers.ValidationError) as error:
            serializer.validate_role('SupervisorRole')
        self.assertEqual(error.exception.detail[0], 'Invalid Role: SupervisorRole')
        self.assertEqual(error.exception.detail[0].code, "invalid")

    def test_validate_teams_returns_team_id_for_valid_teams_in_data(self):
        serializer = EditMemberRoleTeamsSerializer()
        valid_teams = [1, 2, 4]
        value = serializer.validate_teams(valid_teams)
        self.assertListEqual(value, valid_teams)

    def test_validate_teams_raise_serializer_error_for_duplicate_team_ids(self):
        serializer = EditMemberRoleTeamsSerializer()
        duplicate_teams = [1, 2, 4, 2]
        with self.assertRaises(serializers.ValidationError) as error:
            serializer.validate_teams(duplicate_teams)
        self.assertEqual(error.exception.detail[0], 'Invalid Teams: Duplicate values')
        self.assertEqual(error.exception.detail[0].code, 'invalid')

    def test_validate_teams_raise_serializer_error_for_invalid_team_ids(self):
        serializer = EditMemberRoleTeamsSerializer()
        duplicate_teams = [10000, 50000]
        with self.assertRaises(serializers.ValidationError) as error:
            serializer.validate_teams(duplicate_teams)
        self.assertEqual(error.exception.detail[0], 'Invalid Teams: {10000, 50000} is not valid')
        self.assertEqual(error.exception.detail[0].code, 'invalid')

    def test_update_replaces_old_role_teams_with_new_ones_from_data(self):
        self.user = User.objects.get(id=1)
        user_role_teams = User_Team.objects.filter(user=self.user)
        self.role = user_role_teams[0].role
        role_name = self.role.name
        self.old_teams = [user_role_team.team_id for user_role_team in user_role_teams if user_role_team.role.name == role_name]
        all_teams = Team.objects.only('id')
        new_teams = [team.id for team in all_teams if team not in self.old_teams]
        # Call serializer update method
        serializer = EditMemberRoleTeamsSerializer(self.user, data={'role': role_name, 'teams': new_teams})
        serializer.is_valid()
        serializer_user_role_teams = serializer.save()

        updated_teams = [role_team.team.id for role_team in serializer_user_role_teams if role_team.role.name == role_name]
        self.assertListEqual(updated_teams, new_teams)
        # Fetch teams from db and to assert data was saved in db
        user_role_teams_from_db = User_Team.objects.filter(user=self.user)
        teams_from_db = [user_role_team.team_id for user_role_team in user_role_teams_from_db if user_role_team.role.name == role_name]
        self.assertListEqual(teams_from_db, new_teams)

        # Verify the serializer returns all user role team records for that user
        self.assertEqual(list(serializer_user_role_teams), list(user_role_teams_from_db))

    def test_update_removes_all_teams_when_empty_team_list_in_data(self):
        self.user = User.objects.get(id=1)
        user_role_teams = User_Team.objects.filter(user=self.user)
        self.role = user_role_teams[0].role
        role_name = self.role.name
        self.old_teams = [user_role_team.team_id for user_role_team in user_role_teams if user_role_team.role.name == role_name]
        # Call serializer update method
        serializer = EditMemberRoleTeamsSerializer(self.user, data={'role': role_name, 'teams': []})
        serializer.is_valid()
        serializer_user_role_teams = serializer.save()

        self.assertEqual(len(serializer_user_role_teams), 1)
        self.assertEqual(serializer_user_role_teams.first().role.name, role_name)
        self.assertEqual(serializer_user_role_teams.first().team, None)
        # Fetch teams from db and to assert data was saved in db
        user_role_teams_from_db = User_Team.objects.filter(user=self.user)
        self.assertEqual(len(user_role_teams_from_db), 1)
        self.assertEqual(user_role_teams_from_db.first().role.name, role_name)
        self.assertEqual(user_role_teams_from_db.first().team, None)

        # Verify the serializer returns all user role team records for that user
        self.assertEqual(list(serializer_user_role_teams), list(user_role_teams_from_db))

    def test_update_fails_for_new_role_with_existing_team(self):
        self.user = User.objects.get(id=1)
        user_role_teams = User_Team.objects.filter(user=self.user)
        self.role = user_role_teams[0].role
        role_name = self.role.name
        self.old_teams = [user_role_team.team_id for user_role_team in user_role_teams if user_role_team.role.name == role_name]
        new_role = [role for role in Role.VALID_ROLES if role != role_name]
        first_new_role = new_role[0]
        serializer = EditMemberRoleTeamsSerializer(self.user, data={'role': first_new_role, 'teams': [self.old_teams[0]]})

        with self.assertRaises(serializers.ValidationError) as error:
            serializer.validate({'role': first_new_role, 'teams': [self.old_teams[0]]})

        self.assertEqual(error.exception.detail[0], f'Role other than {first_new_role} exists for one or more teams in request')

    def tearDown(self) -> None:
        # Revert changes made by the test
        if self.user:
            User_Team.objects.filter(user=self.user, role=self.role).delete()
            user_team_objs = [User_Team(user=self.user, role=self.role, team_id=team) for team in self.old_teams]
            User_Team.objects.bulk_create(user_team_objs)
            self.user = self.role = self.old_teams = None
