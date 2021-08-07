from django.contrib.auth.models import User
from django.test import TransactionTestCase
from ..permissions import CanSendEmail, CanGetMemberInfo, CanAddMember, CanDeleteMember, CanEditMember
from django.http.request import HttpRequest


class PermissionsTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']
    _director = None
    _leader = None
    _volunteer = None
    _req = HttpRequest()

    def setUp(self):
        self._director = self._director or User.objects.get(email='director@example.com')
        self._leader = self._leader or User.objects.get(email='leader@example.com')
        self._volunteer = self._volunteer or User.objects.get(email='volunteer@example.com')

    # Can send email
    _can_send_email_permission = CanSendEmail()

    def test_can_send_email_permission_true_for_director(self):
        self._req.user = self._director
        permission = self._can_send_email_permission.has_permission(self._req, None)
        self.assertTrue(permission, 'Director should have permission to send email')

    def test_can_send_email_permission_false_for_leader(self):
        self._req.user = self._leader
        permission = self._can_send_email_permission.has_permission(self._req, None)
        self.assertFalse(permission, 'Leader should not have permission to send email')

    def test_can_send_email_permission_false_for_volunteer(self):
        self._req.user = self._volunteer
        permission = self._can_send_email_permission.has_permission(self._req, None)
        self.assertFalse(permission, 'Volunteer should not have permission to send email')

    # Can get member info
    _can_get_member_info_permission = CanGetMemberInfo()

    def test_can_get_member_info_permission_true_for_director(self):
        self._req.user = self._director
        permission = self._can_get_member_info_permission.has_permission(self._req, None)
        self.assertTrue(permission, 'Director should have permission to get member info')

    def test_can_get_member_info_permission_false_for_leader(self):
        self._req.user = self._leader
        permission = self._can_get_member_info_permission.has_permission(self._req, None)
        self.assertFalse(permission, 'Leader should not have permission to get member info')

    def test_can_get_member_info_permission_false_for_volunteer(self):
        self._req.user = self._volunteer
        permission = self._can_get_member_info_permission.has_permission(self._req, None)
        self.assertFalse(permission, 'Volunteer should not have permission to get member info')

    # Can add member
    _can_add_member_permission = CanAddMember()

    def test_can_add_member_permission_true_for_director(self):
        self._req.user = self._director
        permission = self._can_add_member_permission.has_permission(self._req, None)
        self.assertTrue(permission, 'Director should have permission to add member')

    def test_can_add_member_permission_false_for_leader(self):
        self._req.user = self._leader
        permission = self._can_add_member_permission.has_permission(self._req, None)
        self.assertFalse(permission, 'Leader should not have permission to add member')

    def test_can_add_member_permission_false_for_volunteer(self):
        self._req.user = self._volunteer
        permission = self._can_add_member_permission.has_permission(self._req, None)
        self.assertFalse(permission, 'Volunteer should not have permission to add member')

    # Can delete member
    _can_delete_member_permission = CanDeleteMember()

    def test_can_delete_member_permission_true_for_director(self):
        self._req.user = self._director
        permission = self._can_delete_member_permission.has_permission(self._req, None)
        self.assertTrue(permission, 'Director should have permission to delete member')

    def test_can_delete_member_permission_false_for_leader(self):
        self._req.user = self._leader
        permission = self._can_delete_member_permission.has_permission(self._req, None)
        self.assertFalse(permission, 'Leader should not have permission to delete member')

    def test_can_delete_member_permission_false_for_volunteer(self):
        self._req.user = self._volunteer
        permission = self._can_delete_member_permission.has_permission(self._req, None)
        self.assertFalse(permission, 'Volunteer should not have permission to delete member')

    # Can edit member
    _can_edit_member_permission = CanEditMember()

    def test_can_edit_member_permission_true_for_director(self):
        self._req.user = self._director
        permission = self._can_edit_member_permission.has_permission(self._req, None)
        self.assertTrue(permission, 'Director should have permission to edit member')

    def test_can_edit_member_permission_false_for_leader(self):
        self._req.user = self._leader
        permission = self._can_edit_member_permission.has_permission(self._req, None)
        self.assertFalse(permission, 'Leader should not have permission to edit member')

    def test_can_edit_member_permission_false_for_volunteer(self):
        self._req.user = self._volunteer
        permission = self._can_edit_member_permission.has_permission(self._req, None)
        self.assertFalse(permission, 'Volunteer should not have permission to edit member')
