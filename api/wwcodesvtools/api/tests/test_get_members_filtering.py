import json
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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

    # Testing get members filtering with role = DIRECTOR
    # status = ACTIVE
    def test_get_members_filtering_with_role_and_status(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?userprofile__role=DIRECTOR&userprofile__status=ACTIVE", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 1)
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'John')
        self.assertEqual(json.loads(response.content)[0]['role'], 'DIRECTOR')
        self.assertEqual(json.loads(response.content)[0]['status'], 'ACTIVE')

    # Testing get members filtering with role = LEADER
    # status = PENDING for a non-director user
    # Users with PENDING status should not be shown for a non-director
    def test_get_members_filtering_with_non_director_role_and_status(self):
        self.username = 'volunteer@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?userprofile__role=LEADER&userprofile__status=PENDING", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 0)

    # Testing get members filtering with role = LEADER
    def test_get_members_filtering_with_role(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?userprofile__role=LEADER", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 2)
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'Caroline')
        self.assertEqual(json.loads(response.content)[0]['role'], 'LEADER')
        self.assertEqual(json.loads(response.content)[0]['status'], 'PENDING')
        self.assertEqual(json.loads(response.content)[1]['first_name'], 'Bruno')
        self.assertEqual(json.loads(response.content)[1]['role'], 'LEADER')
        self.assertEqual(json.loads(response.content)[1]['status'], 'ACTIVE')
