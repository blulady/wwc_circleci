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

    def setUp(self):
        self.access_token = self.get_token('director@example.com', 'Password123')
        self.bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.access_token)}

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: username,
            'password': password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    def delete_request(self, id, bearer):
        return self.client.delete(f'/api/user/delete/{id}/', **bearer, accept="application/json", content_type="application/json",)

    # test can delete member with role = DIRECTOR
    def test_can_delete_member(self):
        response = self.delete_request(3, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {"result": "User deleted successfully"})

    def test_delete_member_view_permissions(self):
        view_permissions = DeleteMemberView().permission_classes
        # DRF Permissions OperandHolder Dictionary
        expected_permissions = {'operator_class': AND, 'op1_class': IsAuthenticated, 'op2_class': CanDeleteMember}
        self.assertEqual(len(view_permissions), 1)
        self.assertDictEqual(view_permissions[0].__dict__, expected_permissions)

    def test_user_not_found(self):
        response = self.delete_request(50, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {"detail": "Not found."})
