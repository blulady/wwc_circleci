import json
import re
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
        members = json.loads(response.content)
        name_of_members = set()
        expected_members = set(['Brown', 'Brenda', 'Bruno'])
        for member in members:
            member_start_with_first_name_check = re.search('^Br', member['first_name'])
            member_start_with_last_name_check = re.search('^Br', member['last_name'])
            if(member_start_with_first_name_check is not None):
                name_of_members.add(member['first_name'])
            elif(member_start_with_last_name_check is not None):
                name_of_members.add(member['last_name'])
        self.assertSetEqual(expected_members, name_of_members)

    # Testing get members searching with role = DIRECTOR, first_name/last_name = mil
    def test_get_members_search_by_last_name_for_director_role(self):
        access_token = self.get_token(self.DIRECTOR_EMAIL, self.DIRECTOR_PASSWORD)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?search=cla", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 1)
        self.assertEqual(json.loads(response.content)[0]['last_name'], 'Clark')

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
        members = json.loads(response.content)
        unique_members = set()
        self.assertEqual(responseLength, 2)
        for member in members:
            self.assertEqual(member['first_name'], 'Sophie')
            unique_members.add(member['id'])
        self.assertEqual(len(unique_members), len(members))

    # Testing get members searching with role = VOLUNTEER, first_name/last_name = br
    def test_member_search_returns_matches_for_firstname_and_lastname_for_volunteer_role(self):
        self.username = 'volunteer@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?search=br", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 3)
        members = json.loads(response.content)
        name_of_members = set()
        expected_members = set(['Brown', 'Brenda', 'Bruno'])
        for member in members:
            member_start_with_first_name_check = re.search('^Br', member['first_name'])
            member_start_with_last_name_check = re.search('^Br', member['last_name'])
            if(member_start_with_first_name_check is not None):
                name_of_members.add(member['first_name'])
            elif(member_start_with_last_name_check is not None):
                name_of_members.add(member['last_name'])
        self.assertSetEqual(expected_members, name_of_members)
