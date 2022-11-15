from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import Role, User_Team
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AND
from api.permissions import CanEditMember
from ..views.EditMemberRoleTeamsView import EditMemberRoleTeamsView


class DeleteMemberRoleViewTestCase(TransactionTestCase):
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

    def delete_request(self, id, role, bearer):
        return self.client.delete(f'/api/user/edit/{id}/role/{role}/', **bearer,
                                  accept="application/json",
                                  content_type="application/json", )

    def test_edit_permissions(self):
        view_permissions = EditMemberRoleTeamsView.permission_classes
        # DRF Permissions OperandHolder Dictionary
        expected_permissions = {'operator_class': AND, 'op1_class': IsAuthenticated, 'op2_class': CanEditMember}
        self.assertEqual(len(view_permissions), 1)
        self.assertDictEqual(view_permissions[0].__dict__, expected_permissions)

    def test_user_pending(self):
        target_userid = 8
        response = self.delete_request(target_userid, Role.LEADER, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_invalid_user_id(self):
        target_userid = 9999
        response = self.delete_request(target_userid, Role.VOLUNTEER, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_role_not_found(self):
        target_userid = 6
        response = self.delete_request(target_userid, Role.DIRECTOR, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_last_role_cannot_be_removed(self):
        target_userid = 5
        response = self.delete_request(target_userid, Role.DIRECTOR, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_role_removed_successfully(self):
        target_userid = 6
        response = self.delete_request(target_userid, Role.VOLUNTEER, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        target_role = Role.objects.get(name=Role.VOLUNTEER)
        confirm_role_deleted = User_Team.objects.filter(user_id=target_userid, role_id=target_role)
        self.assertEqual(len(confirm_role_deleted), 0)
