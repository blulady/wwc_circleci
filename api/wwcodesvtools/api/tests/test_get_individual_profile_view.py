import json
from rest_framework import status
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# Display the current user's profile, including sensitive data such as email address
class GetIndividualProfileViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # Testing get individual profile for a logged in member. Email displayed in results.
    def test_get_individual_profile(self):
        self.username = 'volunteer@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/user/profile/", **bearer)
        member_content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg='HTTP 200 failed')
        self.assertEqual(member_content.get('first_name'), 'Alice', msg='Invalid first name')
        self.assertEqual(member_content.get('email'), 'volunteer@example.com', msg='Invalid email')

    def test_get_individual_profile_director(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/user/profile/", **bearer)
        member_content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg='HTTP 200 failed')
        self.assertEqual(member_content.get('first_name'), 'John', msg='Invalid first name')
        self.assertEqual(member_content.get('email'), 'director@example.com', msg='Invalid email')

    def test_get_individual_profile_leader(self):
        self.username = 'leader@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/user/profile/", **bearer)
        member_content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg='HTTP 200 failed')
        self.assertEqual(member_content.get('first_name'), 'Bruno', msg='Invalid first name')
        self.assertEqual(member_content.get('email'), 'leader@example.com', msg='Invalid email')
