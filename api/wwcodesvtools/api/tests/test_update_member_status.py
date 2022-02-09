import json
from django.test import TransactionTestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import UserProfile
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AND
from api.permissions import CanEditMember
from ..views.UpdateMemberStatusView import UpdateMemberStatusView


class UpdateMemberStatusViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']

    USER_EDITED_SUCCESSFULLY = 'User edited successfully'
    INVALID_STATUS = {'error': {'status': ["Invalid Status: accepted values are 'ACTIVE','INACTIVE'"]}}

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

    def post_request(self, id, data, bearer):
        return self.client.post(f'/api/user/edit/{id}/status/', data, **bearer,
                                accept="application/json",
                                content_type="application/json",)

    # test if permission granted to change 'status' data
    def test_check_member_permissions(self):
        view_permissions = UpdateMemberStatusView().permission_classes
        # DRF Permissions OperandHolder Dictionary
        expected_permissions = {'operator_class': AND, 'op1_class': IsAuthenticated, 'op2_class': CanEditMember}
        self.assertEqual(len(view_permissions), 1)
        self.assertDictEqual(view_permissions[0].__dict__, expected_permissions)

    # test that user exists
    def test_member_not_found(self):
        data = {"status": UserProfile.INACTIVE}
        response = self.post_request(50000000, data, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {"detail": "Not found."})

    # test validity of status, return error if value is not one of ACTIVE, INACTIVE
    def test_update_member_forbidden_data(self):
        data = {"status": "PENDING"}
        response = self.post_request(4, data, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test request to change status from inactive to active
    def test_change_status_from_inactive_active(self):
        user_id = 5
        initial_status = User.objects.select_related('userprofile').get(id=user_id)
        initial_status.userprofile.status = 'INACTIVE'
        initial_status.userprofile.save()
        self.assertEqual(initial_status.userprofile.status, UserProfile.INACTIVE)

        # make the request
        new_status = {"status": UserProfile.ACTIVE}
        response = self.post_request(user_id, new_status, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 'User status edited successfully')
        initial_status.refresh_from_db()
        self.assertEqual(initial_status.userprofile.status, UserProfile.ACTIVE)

    # test request to change status from active to inactive
    def test_change_status_from_active_inactive(self):
        user_id = 6
        initial_status = User.objects.select_related('userprofile').get(id=user_id)
        initial_status.userprofile.status = 'ACTIVE'
        initial_status.userprofile.save()
        self.assertEqual(initial_status.userprofile.status, UserProfile.ACTIVE)

        # make the request
        new_status = {"status": UserProfile.INACTIVE}
        response = self.post_request(user_id, new_status, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 'User status edited successfully')
        initial_status.refresh_from_db()
        self.assertEqual(initial_status.userprofile.status, UserProfile.INACTIVE)
