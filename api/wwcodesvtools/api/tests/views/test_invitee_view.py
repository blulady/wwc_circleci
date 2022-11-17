from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from datetime import datetime
import json


class InviteeModelTest(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json', 'invitee.json']
    DIRECTOR_EMAIL = 'director@example.com'
    LEADER_EMAIL = 'leader@example.com'
    PASSWORD = 'Password123'

    def setUp(self):
        self.access_token = self.get_token(self.DIRECTOR_EMAIL, self.PASSWORD)
        self.bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.access_token)}

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: username,
            'password': password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # Testing GET invitee list endpoint with role = Director
    def test_invitee_list_for_director(self):
        response = self.client.get("/api/invitee/", **self.bearer)
        data_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data_json), 6)

    # Testing GET invitee list endpoint with role = Leader
    def test_invalid_access_to_invitee_list(self):
        access_token = self.get_token(self.LEADER_EMAIL, self.PASSWORD)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/invitee/", **bearer)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Testing CREATE invitee endpoint
    def test_invitee_create(self):
        json_type = "application/json"
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        token = f"abcdefa0342a4330bc790f23ac70a7b6{now}"
        data = json.dumps({"email": "user@example.com",
                           "message": "string",
                           "role": 1,
                           "registration_token": token,
                           "resent_counter": 0,
                           "accepted": False,
                           "created_by": 1
                           })
        response = self.client.post("/api/invitee/", data, **self.bearer, accept=json_type, content_type=json_type)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', json.loads(response.content))

    # Testing GET invitee by id endpoint
    def test_invitee_read_for_director(self):
        response = self.client.get("/api/invitee/1/", **self.bearer)
        self.assertEqual(response.data['email'], 'volunteer@example.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing PATCH invitee endpoint
    def test_invitee_patch(self):
        json_type = "application/json"
        data = json.dumps({"email": "volunteer2@example.com"})
        response = self.client.patch("/api/invitee/1/", data, **self.bearer, accept=json_type, content_type=json_type)
        self.assertEqual(response.status_code,  status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'volunteer2@example.com')

    # Testing DELETE invitee endpoint
    def test_delete_invitee_by_id_for_director(self):
        response = self.client.delete("/api/invitee/2/", **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
