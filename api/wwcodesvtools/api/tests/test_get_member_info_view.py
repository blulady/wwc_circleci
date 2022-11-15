import json
from rest_framework import status
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.models import Role

# Alternate the endpoint id to test whether sensitive information is displayed or not
# In this case, the email should only be shown to the Director.


class GetMemberInfoViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']
    DIRECTOR_EMAIL = 'director@example.com'
    LEADER_EMAIL = 'leader@example.com'
    VOLUNTEER_EMAIL = 'volunteer@example.com'
    PASSWORD = 'Password123'

    def get_token(self, username):
        self.username = username or self.DIRECTOR_EMAIL
        self.password = self.PASSWORD
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # Testing get member info for a logged in member. Email not displayed in results.
    def test_get_member_info(self):
        self.username = 'alexanderbrown@example.com'
        access_token = self.get_token(self.username)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/user/7/", **bearer)
        member_content = json.loads(response.content)
        self.assertEqual(member_content.get('id'), 7)
        self.assertEqual(member_content.get('first_name'), "Alexander")
        self.assertEqual(member_content.get('last_name'), "Brown")
        self.assertEqual(member_content.get('status'), "ACTIVE")
        self.assertEqual(member_content.get('highest_role'), Role.LEADER)
        self.assertEqual(member_content.get('date_joined'), "2021-05-25T00:00:52.353000Z")
        self.assertEqual(member_content.get('role_teams'), [{'role_name': Role.LEADER}])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing get member info with role = DIRECTOR. Email displayed for any endpoint id
    def test_get_member_info_for_director(self):
        access_token = self.get_token(None)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/user/1/", **bearer)
        member_content = json.loads(response.content)
        self.assertEqual(member_content.get('id'), 1)
        self.assertEqual(member_content.get('first_name'), "John")
        self.assertEqual(member_content.get('last_name'), "Smith")
        self.assertEqual(member_content.get('status'), "ACTIVE")
        self.assertEqual(member_content.get('highest_role'), Role.DIRECTOR)
        self.assertEqual(member_content.get('date_joined'), "2021-02-19T01:55:01.810000Z")
        self.assertEqual(member_content.get('role_teams'), [{'team_id': 5, 'team_name': 'Social Media', 'role_name': Role.DIRECTOR}])
        self.assertEqual(member_content.get('email'), 'director@example.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing get member info with role = LEADER. Email not displayed for any endpoint id
    def test_get_member_info_for_leader(self):
        access_token = self.get_token(self.LEADER_EMAIL)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/user/3/", **bearer)
        member_content = json.loads(response.content)
        self.assertEqual(member_content.get('id'), 3)
        self.assertEqual(member_content.get('first_name'), "Bruno")
        self.assertEqual(member_content.get('last_name'), "Clark")
        self.assertEqual(member_content.get('status'), "ACTIVE")
        self.assertEqual(member_content.get('highest_role'), Role.LEADER)
        self.assertEqual(member_content.get('date_joined'), "2021-02-19T01:56:29.756000Z")
        self.assertEqual(member_content.get('role_teams'),
                         [{'role_name': Role.LEADER, 'team_id': 1, 'team_name': 'Event Volunteers'},
                         {'role_name': Role.LEADER, 'team_id': 7, 'team_name': 'Volunteer Management'}])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing get member info with role = VOLUNTEER. Email not displayed for any endpoint id
    def test_get_member_info_for_volunteer(self):
        access_token = self.get_token(self.VOLUNTEER_EMAIL)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/user/2/", **bearer)
        member_content = json.loads(response.content)
        self.assertEqual(member_content.get('id'), 2)
        self.assertEqual(member_content.get('first_name'), "Alice")
        self.assertEqual(member_content.get('last_name'), "Robinson")
        self.assertEqual(member_content.get('status'), "ACTIVE")
        self.assertEqual(member_content.get('highest_role'), Role.VOLUNTEER)
        self.assertEqual(member_content.get('date_joined'), "2021-02-19T01:56:06.115000Z")
        self.assertEqual(member_content.get('role_teams'),
                         [{'role_name': Role.VOLUNTEER, 'team_id': 4, 'team_name': 'Partnership Management'},
                         {'role_name': Role.VOLUNTEER, 'team_id': 5, 'team_name': 'Social Media'},
                         {'role_name': Role.VOLUNTEER, 'team_id': 3, 'team_name': 'Host Management'}])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
