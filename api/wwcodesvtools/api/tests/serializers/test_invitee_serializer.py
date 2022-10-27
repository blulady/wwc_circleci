from django.test import TransactionTestCase
from api.serializers.InviteeSerializer import InviteeSerializer
from api.models import Invitee


class InviteeModelTest(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json', 'invitee.json']

    def setUp(self):
        self.invitee = Invitee.objects.get(id=2)
        self.serializer = InviteeSerializer(self.invitee)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['email', 'role_name', 'status', 'created_at', 'updated_at']))

    def test_data_has_email_for_given_invitee(self):
        data = self.serializer.data
        self.assertEqual(data['email'], 'sophiefisher@example.com')

    def test_data_has_role_name_for_given_invitee(self):
        data = self.serializer.data
        self.assertEqual(data['role_name'], 'VOLUNTEER')

    def test_data_has_status_for_given_invitee(self):
        data = self.serializer.data
        self.assertEqual(data['status'], 'EXPIRED')
