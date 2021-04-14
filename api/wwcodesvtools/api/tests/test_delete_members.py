import json
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status


class DeleteMembersTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['get_members_data.json', 'roles_data.json']
    EXPECTED_MESSAGE = 'You do not have permission to perform this action.'

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # test  can delete member with role =DIRECTOR
    def test_can_delete_member(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/user/3", **bearer)
        self.assertEqual(json.loads(response.content)['id'], 3)
        self.assertEqual(json.loads(response.content)['email'], 'leader@example.com')
        self.assertEqual(json.loads(response.content)['first_name'], 'Bruno')
        self.assertEqual(json.loads(response.content)['last_name'], 'Clark')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete("/api/user/delete/3", **bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {"result": "User deleted successfully"})
        response = self.client.get("/api/user/3", **bearer)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {"detail": "Not found."})

    # test cannot delete member permission with role = LEADER
    def test_can_delete_member_with_no_permission_for_leader(self):
        self.username = 'leader@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.delete("/api/user/delete/3", **bearer)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail': self.EXPECTED_MESSAGE})

    # test cannot delete member permission with role = VOLUNTEER
    def test_can_delete_member_with_no_permission_for_volunteer(self):
        self.username = 'volunteer@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.delete("/api/user/delete/3", **bearer)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail': self.EXPECTED_MESSAGE})
