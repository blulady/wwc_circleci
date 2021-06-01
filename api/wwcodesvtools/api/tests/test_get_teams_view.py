import json
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class GetTeamsViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    def test_get_teams(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/teams/", **bearer)
        self.assertEqual(len(response.data), 7)
        self.assertEqual(json.loads(response.content)[0]['id'], 1)
        self.assertEqual(json.loads(response.content)[0]['name'], 'Event Volunteers')
        self.assertEqual(json.loads(response.content)[1]['id'], 2)
        self.assertEqual(json.loads(response.content)[1]['name'], 'Hackathon Volunteers')
        self.assertEqual(json.loads(response.content)[2]['id'], 3)
        self.assertEqual(json.loads(response.content)[2]['name'], 'Host Management')
        self.assertEqual(json.loads(response.content)[3]['id'], 4)
        self.assertEqual(json.loads(response.content)[3]['name'], 'Partnership Management')
        self.assertEqual(json.loads(response.content)[4]['id'], 5)
        self.assertEqual(json.loads(response.content)[4]['name'], 'Social Media')
        self.assertEqual(json.loads(response.content)[5]['id'], 6)
        self.assertEqual(json.loads(response.content)[5]['name'], 'Tech Event Volunteers')
        self.assertEqual(json.loads(response.content)[6]['id'], 7)
        self.assertEqual(json.loads(response.content)[6]['name'], 'Volunteer Management')
