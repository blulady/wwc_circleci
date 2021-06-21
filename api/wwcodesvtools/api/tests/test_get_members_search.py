import json
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class GetMembersSearchTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # Testing get members searching with role = DIRECTOR, first_name/last_name = bru
    def test_get_members_search_by_first_name_for_director_role(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?search=bru", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 1)
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'Bruno')

    # Testing get members searching with role = DIRECTOR, first_name/last_name = mil
    def test_get_members_search_by_last_name_for_director_role(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?search=mil", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 1)
        self.assertEqual(json.loads(response.content)[0]['last_name'], 'Miller')

    # Testing get members searching with role = DIRECTOR, first_name/last_name = whi
    def test_get_members_search_by_name_for_director_role(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?search=whi", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 0)

    # Testing get members searching with role = LEADER, first_name/last_name = sop
    def test_get_members_search_by_multiple_names_for_leader_role(self):
        self.username = 'leader@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?search=sop", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 2)
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'Sophie')
        self.assertEqual(json.loads(response.content)[1]['first_name'], 'Sophie')

    # Testing get members searching with role = VOLUNTEER, first_name/last_name = br
    def test_get_members_search_by_multiple_names_for_volunteer_role(self):
        self.username = 'volunteer@example.com'
        self.password = 'Password123'

        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?search=br", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 3)
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'Alexander')
        self.assertEqual(json.loads(response.content)[1]['first_name'], 'Brenda')
        self.assertEqual(json.loads(response.content)[2]['first_name'], 'Bruno')
