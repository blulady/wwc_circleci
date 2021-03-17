import json
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import UserProfile
from rest_framework import status


class EditMemberViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['get_members_data.json']
    EXPECTED_MESSAGE = 'User edited successfully'

    def setUp(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        self.access_token = self.get_token(self.username, self.password)
        self.bearer = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.access_token)}

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: username,
            'password': password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    def check_member_before_after_change(self, data):
        # Before change
        endpoint = "/api/user/" + str(data['user_id'])
        response = self.client.get(endpoint, **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['id'], data['user_id'])
        self.assertEqual(json.loads(response.content)[
                         'email'], data['email'])
        self.assertEqual(json.loads(response.content)[
                         'first_name'], data['first_name'])
        self.assertEqual(json.loads(response.content)[
                         'last_name'], data['last_name'])
        self.assertEqual(json.loads(response.content)[
                         'status'], data['user_status'])
        self.assertEqual(json.loads(response.content)['role'], data['role'])

    def test_edit_member_nonexistant_id(self):
        user_data = {
            'user_id': 404,
            'email':  'leaderPendingStatus@example.com',
            'first_name': 'Caroline',
            'last_name': 'Miller',
            'user_status': UserProfile.PENDING,
            'role': UserProfile.LEADER
        }

        # making change
        data = {"role": UserProfile.VOLUNTEER, "status": UserProfile.INACTIVE}
        endpoint = "/api/user/edit/" + str(user_data["user_id"])
        response = self.client.post(endpoint, data, **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {"detail": "Not found."})

    def test_edit_member_pending_status(self):
        # before change
        user_data = {
            'user_id': 4,
            'email':  'leaderPendingStatus@example.com',
            'first_name': 'Caroline',
            'last_name': 'Miller',
            'user_status': UserProfile.PENDING,
            'role': UserProfile.LEADER
        }

        self.check_member_before_after_change(data=user_data)

        # making change
        data = {"role": UserProfile.VOLUNTEER, "status": UserProfile.INACTIVE}
        endpoint = "/api/user/edit/" + str(user_data["user_id"])
        response = self.client.post(endpoint, data, **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {
                         'error': 'User can not be edited because her status is pending.'})
        # after change
        self.check_member_before_after_change(user_data)

    def test_edit_member_by_nondirector(self):
        username = 'leader@example.com'
        password = 'Password123'
        access_token = self.get_token(username, password)
        bearer = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        # before change
        user_data = {
            'user_id': 4,
            'email':  'leaderPendingStatus@example.com',
            'first_name': 'Caroline',
            'last_name': 'Miller',
            'user_status': UserProfile.PENDING,
            'role': UserProfile.LEADER
        }

        self.check_member_before_after_change(data=user_data)

        # making change
        data = {"role": UserProfile.VOLUNTEER, "status": UserProfile.INACTIVE}
        endpoint = "/api/user/edit/" + str(user_data["user_id"])
        response = self.client.post(endpoint, data, **bearer)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {
                         'detail': 'You do not have permission to perform this action.'})
        # after change
        self.check_member_before_after_change(user_data)

    def test_edit_role_member_notallowed_role(self):
        user_data = {
            'user_id': 3,
            'email':  'leader@example.com',
            'first_name': 'Bruno',
            'last_name': 'Clark',
            'user_status': UserProfile.ACTIVE,
            'role': UserProfile.LEADER
        }
        # before change
        self.check_member_before_after_change(data=user_data)

        # making change
        data = {"role": "SOMEROLE", "status": UserProfile.INACTIVE}
        response = self.client.post("/api/user/edit/3", data, **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {
            'error': "User's role or status entered is empty or incorrect."})

        # after change
        self.check_member_before_after_change(user_data)

    def test_edit_status_member_notallowed_status(self):
        user_data = {
            'user_id': 3,
            'email':  'leader@example.com',
            'first_name': 'Bruno',
            'last_name': 'Clark',
            'user_status': UserProfile.ACTIVE,
            'role': UserProfile.LEADER
        }
        # before change
        self.check_member_before_after_change(data=user_data)

        # making change
        data = {"role": UserProfile.VOLUNTEER, "status": "SOMESTATUS"}
        response = self.client.post("/api/user/edit/3", data, **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {
            'error': "User's role or status entered is empty or incorrect."})

        # after change
        self.check_member_before_after_change(user_data)

    def test_empty_input(self):
        user_data = {
            'user_id': 3,
            'email':  'leader@example.com',
            'first_name': 'Bruno',
            'last_name': 'Clark',
            'user_status': UserProfile.ACTIVE,
            'role': UserProfile.LEADER
        }
        # before change
        self.check_member_before_after_change(data=user_data)

        # making change
        data = {"role": "", "status": ""}
        response = self.client.post("/api/user/edit/3", data, **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {
            'error': "User's role or status entered is empty or incorrect."})

        # after change
        self.check_member_before_after_change(user_data)

    def test_edit_member(self):
        user_data = {
            'user_id': 3,
            'email':  'leader@example.com',
            'first_name': 'Bruno',
            'last_name': 'Clark',
            'user_status': UserProfile.ACTIVE,
            'role': UserProfile.LEADER
        }
        # before change
        self.check_member_before_after_change(data=user_data)

        # making change
        data = {"role": UserProfile.VOLUNTEER, "status": UserProfile.INACTIVE}
        response = self.client.post("/api/user/edit/3", data, **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {
                         'result': self.EXPECTED_MESSAGE})

        # after change
        user_data['role'] = UserProfile.VOLUNTEER
        user_data['user_status'] = UserProfile.INACTIVE
        self.check_member_before_after_change(user_data)
