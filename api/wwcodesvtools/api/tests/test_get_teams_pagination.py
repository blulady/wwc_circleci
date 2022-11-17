from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class GetTeamsPaginationTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # Testing limit-offset pagination with a limit of 2, it should return the firts two values
    def test_get_teams_pagination_with_limit(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/teams/?limit=2", **bearer)
        self.assertEqual(response.data['count'], 8)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['id'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Event Volunteers')
        self.assertEqual(response.data['results'][1]['id'], 2)
        self.assertEqual(response.data['results'][1]['name'], 'Hackathon Volunteers')

    # Testing limit-offset pagination with a limit of 2 and an offset of 6
    # Since there are 8 values, it should return two values (the last two)
    def test_get_teams_pagination_with_limit_and_offset(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/teams/?limit=2&offset=6", **bearer)
        self.assertEqual(response.data['next'], None)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['id'], 7)
        self.assertEqual(response.data['results'][0]['name'], 'Volunteer Management')
        self.assertEqual(response.data['results'][1]['id'], 8)
        self.assertEqual(response.data['results'][1]['name'], 'Tech Bloggers')
