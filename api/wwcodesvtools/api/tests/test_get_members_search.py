import json
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class GetMembersSearchTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']
    DIRECTOR_EMAIL = 'director@example.com'
    DIRECTOR_PASSWORD = 'Password123'

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: username,
            'password': password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # Testing get members searching with role = DIRECTOR, first_name/last_name = bru
    def test_get_members_search_by_first_name_for_director_role(self):
        access_token = self.get_token(self.DIRECTOR_EMAIL, self.DIRECTOR_PASSWORD)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?search=bru", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 1)
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'Bruno')

    # Testing get members searching and sorting with role = DIRECTOR, first_name/last_name = br
    def test_get_members_search_and_sort_by_first_name_for_director_role(self):
        access_token = self.get_token(self.DIRECTOR_EMAIL, self.DIRECTOR_PASSWORD)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=first_name&search=br", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 3)
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'Alexander')
        self.assertEqual(json.loads(response.content)[1]['first_name'], 'Brenda')        
        self.assertEqual(json.loads(response.content)[2]['first_name'], 'Bruno')


    # Testing get members searching with role = DIRECTOR, first_name/last_name = mil
    def test_get_members_search_by_last_name_for_director_role(self):
        access_token = self.get_token(self.DIRECTOR_EMAIL, self.DIRECTOR_PASSWORD)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?search=mil", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 1)
        self.assertEqual(json.loads(response.content)[0]['last_name'], 'Miller')

    # Testing get members searching with role = DIRECTOR, first_name/last_name='not_matching_anything'
    def test_member_search_return_empty_for_no_match_for_director_role(self):
        access_token = self.get_token(self.DIRECTOR_EMAIL, self.DIRECTOR_PASSWORD)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?search=not_matching_anything", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 0)

    # Testing get members searching with role = LEADER, first_name/last_name = sop
    def test_member_search_returns_multiple_matches_for_firstname_for_leader_role(self):
        self.username = 'leader@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?search=sop", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 2)
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'Sophie')
        self.assertEqual(json.loads(response.content)[0]['id'], 9)
        self.assertEqual(json.loads(response.content)[1]['first_name'], 'Sophie')
        self.assertEqual(json.loads(response.content)[1]['id'], 6)

    # Testing get members searching with role = VOLUNTEER, first_name/last_name = br
    def test_member_search_returns_matches_for_firstname_and_lastname_for_volunteer_role(self):
        self.username = 'volunteer@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?search=br", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 3)
        self.assertEqual(json.loads(response.content)[0]['last_name'], 'Brown')
        self.assertEqual(json.loads(response.content)[1]['first_name'], 'Brenda')
        self.assertEqual(json.loads(response.content)[2]['first_name'], 'Bruno')
