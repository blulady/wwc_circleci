import json
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AND
from api.permissions import CanDeleteMember
from ..views.DeleteMemberView import DeleteMemberView


class DeleteMembersTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']

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

    def test_delete_member_view_permissions(self):
        view_permissions = DeleteMemberView().permission_classes
        # DRF Permissions OperandHolder Dictionary
        expected_permissions = {'operator_class': AND, 'op1_class': IsAuthenticated, 'op2_class': CanDeleteMember}
        self.assertEqual(len(view_permissions), 1)
        self.assertDictEqual(view_permissions[0].__dict__, expected_permissions)
