import json
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.models import Role


class TestGetMembersTeams(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']

    def setUp(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        self.access_token = self.get_token(self.username, self.password)
        self.bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.access_token)}

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # Testing get members with user teams
    def test_get_members_teams(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=first_name", **bearer)
        members = json.loads(response.content)

        self.assertEqual(members[0]['first_name'], 'Alexander')
        self.assertListEqual(members[0]['role_teams'], [{'role_name': Role.LEADER}])

        alice_expected_role_teams = [{'role_name': Role.VOLUNTEER, 'team_id': 4, 'team_name': 'Partnership Management'},
                                     {'role_name': Role.VOLUNTEER, 'team_id': 5, 'team_name': 'Social Media'},
                                     {'role_name': Role.VOLUNTEER, 'team_id': 3, 'team_name': 'Host Management'}]
        self.assertEqual(members[1]['first_name'], 'Alice')
        self.assertListEqual(members[1]['role_teams'], alice_expected_role_teams)

        self.assertEqual(members[2]['first_name'], 'Brenda')
        self.assertListEqual(members[2]['role_teams'], [{'role_name': Role.DIRECTOR}])

        self.assertEqual(members[3]['first_name'], 'Bruno')
        bruno_expected_role_teams = [{'role_name': Role.LEADER, 'team_id': 1, 'team_name': 'Event Volunteers'},
                                     {'role_name': Role.LEADER, 'team_id': 7, 'team_name': 'Volunteer Management'}]
        self.assertListEqual(members[3]['role_teams'], bruno_expected_role_teams)

        self.assertEqual(members[4]['first_name'], 'John')
        john_expected_role_teams = [{'role_name': Role.DIRECTOR, 'team_id': 5, 'team_name': 'Social Media'}]
        self.assertListEqual(members[4]['role_teams'], john_expected_role_teams)

        self.assertEqual(members[5]['first_name'], 'Sophie')
        sophie_expected_role_teams = [{'role_name': Role.LEADER, 'team_id': 6, 'team_name': 'Tech Event Volunteers'},
                                      {'role_name': Role.VOLUNTEER, 'team_id': 2, 'team_name': 'Hackathon Volunteers'}]
        self.assertListEqual(members[5]['role_teams'], sophie_expected_role_teams)

        self.assertEqual(members[6]['first_name'], 'Sophie')
        sophie_butler_expected_role_teams = [{'role_name': Role.DIRECTOR, 'team_id': 4, 'team_name': 'Partnership Management'},
                                             {'role_name': Role.LEADER, 'team_id': 1, 'team_name': 'Event Volunteers'}]
        self.assertListEqual(members[6]['role_teams'], sophie_butler_expected_role_teams)

        self.assertEqual(members[7]['first_name'], 'Vincent')
        self.assertListEqual(members[7]['role_teams'], [{'role_name': Role.LEADER}])
