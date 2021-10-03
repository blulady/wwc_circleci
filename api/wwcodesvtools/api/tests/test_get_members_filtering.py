import json
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import date


class GetMembersFilteringTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # Testing get members filtering with status=ACTIVE
    def test_get_members_filtering_with_status(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?status=ACTIVE", **bearer)
        members = json.loads(response.content)
        for member in members:
            self.assertEqual(member['status'], 'ACTIVE')

    # Testing get members filtering with date joined = current_year
    def test_get_members_filtering_with_date_joined(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?created_at=current_year", **bearer)
        current_year = date.today().year
        members = json.loads(response.content)
        for member in members:
            self.assertEqual(member['date_joined'][:4], str(current_year))

    # Testing get members filtering with role = LEADER
    def test_get_members_filtering_with_role(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?role=LEADER", **bearer)
        members = json.loads(response.content)
        for member in members:
            if member['role']:
                self.assertEqual(member['role'], 'LEADER')

    # Test get members filtering with role = LEADER and status = ACTIVE
    def test_get_members_filtering_with_role_and_status(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?role=LEADER&status=ACTIVE", **bearer)
        members = json.loads(response.content)
        for member in members:
            self.assertEqual(member['status'], 'ACTIVE')
            if member['role']:
                self.assertEqual(member['role'], 'LEADER')