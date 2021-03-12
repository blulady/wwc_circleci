import json
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status


class GetMemberInfoViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['get_members_data.json']

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # Testing get member info with role = DIRECTOR
    def test_get_member_info_for_director(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/user/1", **bearer)
        self.assertEqual(json.loads(response.content)['id'], 1)
        self.assertEqual(json.loads(response.content)['email'], 'director@example.com')
        self.assertEqual(json.loads(response.content)['first_name'], 'John')
        self.assertEqual(json.loads(response.content)['last_name'], 'Smith')
        self.assertEqual(json.loads(response.content)['status'], 'ACTIVE')
        self.assertEqual(json.loads(response.content)['role'], 'DIRECTOR')
        self.assertEqual(json.loads(response.content)['date_joined'], '2021-02-19T01:55:01.810000Z')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing get member info with role = LEADER
    def test_get_member_info_for_leader(self):
        self.username = 'leader@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/user/1", **bearer)
        self.assertIn('You do not have permission to perform this action.', json.loads(response.content)['detail'])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Testing get member info with role = VOLUNTEER
    def test_get_member_info_for_volunteer(self):
        self.username = 'volunteer@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/user/2", **bearer)
        self.assertIn('You do not have permission to perform this action.', json.loads(response.content)['detail'])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
