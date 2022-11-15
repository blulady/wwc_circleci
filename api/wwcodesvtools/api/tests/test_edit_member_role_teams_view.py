import json
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import Role, User_Team
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AND
from api.permissions import CanEditMember
from ..views.EditMemberRoleTeamsView import EditMemberRoleTeamsView


class EditMemberRoleTeamsViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']
    ERROR_EDITING_USER = 'Error editing user'
    USER_EDITED_SUCCESSFULLY = 'Member role-teams edited successfully'

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
        return self.client.put(f'/api/user/edit/{id}/role_teams/', data, **bearer,
                               accept="application/json",
                               content_type="application/json",)

    def validate_teams(self, user_id, team_ids):
        user_teams = [entity.team_id for entity in User_Team.objects.filter(user_id=user_id).order_by('team_id')]
        self.assertEquals(user_teams, team_ids)

    # test cannot edit an invalid userid
    def test_edit_member_invalid_user_id(self):
        data = {"role": Role.VOLUNTEER, "teams": []}
        response = self.post_request(9999, data, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {"detail": "Not found."})

    # test cannot edit member who has 'PENDING' status
    def test_cannot_edit_member_in_pending_status(self):
        data = {"role": Role.VOLUNTEER, "teams": []}
        response = self.post_request(4, data, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {
                         'error': 'User can not be edited because her status is pending'})

    # test edit member fails for invalid input Role
    def test_edit_member_for_invalid_role(self):
        data = {"role": "SUPERVISOR", "teams": []}
        response = self.post_request(3, data, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid Role: SUPERVISOR', json.loads(response.content)['error']['role'])

    # test edit member fails for blank input Role
    def test_edit_member_empty_input_role(self):
        data = {"role": '', "teams": []}
        response = self.post_request(3, data, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field may not be blank.",
                      json.loads(response.content)['error']['role'])

    # test edit member fails for no input Teams
    def test_edit_member_teams_key_not_present_in_input(self):
        data = {"role": Role.VOLUNTEER}
        response = self.post_request(3, data, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field may not be null.",
                      json.loads(response.content)['error']['teams'])

    # test edit member fails for invalid team ids
    def test_edit_member_invalid_team_ids(self):
        data = {"role": Role.DIRECTOR, "teams": [2, 0, 100]}
        response = self.post_request(3, data, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid Teams: {0, 100} is not valid",
                      json.loads(response.content)['error']['teams'])

    # test edit member fails for duplicate team ids
    def test_edit_member_duplicate_team_ids(self):
        data = {"role": Role.DIRECTOR, "teams": [2, 2, 5]}
        response = self.post_request(3, data, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid Teams: Duplicate values",
                      json.loads(response.content)['error']['teams'])

    # test edit member is successfull with valid input data
    def test_edit_member_with_valid_data(self):
        data = {"role": Role.VOLUNTEER, "teams": [1, 6, 7]}
        response = self.post_request(2, data, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {
                         'result': self.USER_EDITED_SUCCESSFULLY})

    # test edit member removes and adds the list of teams for the user role
    def test_edit_member_update_teams(self):
        # first, edit list of teams ids for user role Leader
        data = {"role": Role.LEADER, "teams": [1, 7]}
        response = self.post_request(3, data, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {
                        'result': self.USER_EDITED_SUCCESSFULLY})

        # validate the team rows added for user
        self.validate_teams(user_id=3, team_ids=[1, 7])

        # next, edit member with another list of teams for the user role Leader
        data = {"role": Role.LEADER, "teams": [4, 7, 5]}
        response = self.post_request(3, data, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {
                        'result': self.USER_EDITED_SUCCESSFULLY})

        # validate the team rows are updated successfully to the new list of teams
        self.validate_teams(user_id=3, team_ids=[4, 5, 7])

    # test edit member for user role with no team
    def test_edit_member_user_role_with_no_team(self):
        # first, edit list of team id for user role Leader
        data = {"role": Role.LEADER, "teams": [1]}
        response = self.post_request(3, data, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {
                         'result': self.USER_EDITED_SUCCESSFULLY})

        # validate the team row added for user role Leader
        self.validate_teams(user_id=3, team_ids=[1])

        # next, edit member with no team for the user role
        data = {"role": Role.LEADER, "teams": []}
        response = self.post_request(3, data, self.bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {
                         'result': self.USER_EDITED_SUCCESSFULLY})

        # validate user role row has no team
        self.validate_teams(user_id=3, team_ids=[None])

    def test_edit_member_view_permissions(self):
        view_permissions = EditMemberRoleTeamsView().permission_classes
        # DRF Permissions OperandHolder Dictionary
        expected_permissions = {'operator_class': AND, 'op1_class': IsAuthenticated, 'op2_class': CanEditMember}
        self.assertEqual(len(view_permissions), 1)
        self.assertDictEqual(view_permissions[0].__dict__, expected_permissions)
