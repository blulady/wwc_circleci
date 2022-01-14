import json
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from ..views.GetMembersView import GetMembersView


class GetMembersViewTestCase(TransactionTestCase):
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

    # Testing get members with role = DIRECTOR
    # 'PENDING' status members and 'email' field are in the response
    def test_get_members_role_director(self):
        access_token = self.get_token(None)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/", **bearer)
        members = json.loads(response.content)
        for member in members:
            self.assertIsNotNone(member['email'])
            self.assertIn(member['status'], ('PENDING', 'ACTIVE'))

    # Testing get members with role = VOLUNTEER
    # 'PENDING' status members and 'email' field not in the response
    def test_get_members_role_volunteer(self):
        self.username = self.VOLUNTEER_EMAIL
        access_token = self.get_token(self.username)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/", **bearer)
        members = json.loads(response.content)
        for member in members:
            self.assertRaises(KeyError, lambda: member['email'])
            self.assertIn(member['status'], 'ACTIVE')

    # Testing get members with role = LEADER
    # 'PENDING' status members and 'email' field not in the response
    def test_get_members_role_leader(self):
        self.username = self.LEADER_EMAIL
        access_token = self.get_token(self.username)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/", **bearer)
        members = json.loads(response.content)
        for member in members:
            self.assertRaises(KeyError, lambda: member['email'])
            self.assertIn(member['status'], 'ACTIVE')

    def test_get_members_view_permissions(self):
        view_permissions = GetMembersView().permission_classes
        self.assertEqual(len(view_permissions), 1)
        self.assertEqual(view_permissions[0], IsAuthenticated)
