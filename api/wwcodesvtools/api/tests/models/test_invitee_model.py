from django.test import TransactionTestCase
from django.db import IntegrityError
from datetime import datetime
from ...models import Invitee, User


class InviteeModelTest(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json', 'invitee.json']
    _director = None

    def setUp(self):
        self._director = self._director or User.objects.get(email='director@example.com')

    # Testing not-null constraint for email
    def test_email_not_null_constraint(self):
        invitee = Invitee(email=None, message="Invitee to new user", created_by=self._director, registration_token="123456")
        self.assertRaises(IntegrityError, lambda: invitee.save())

    # Testing max_lenght for email
    def test_email_max_length(self):
        invitee = Invitee.objects.get(id=1)
        max_length = invitee._meta.get_field('email').max_length
        self.assertEqual(max_length, 254)

    # Testing unique constraint for email
    def test_unique_constraint(self):
        invitee1 = Invitee(email="volunteer1@example.com", message="Invitee to new user", created_by=self._director)
        invitee1.save()
        invitee2 = Invitee(email="volunteer1@example.com", message="Invitee to new user", created_by=self._director)
        self.assertRaises(IntegrityError, lambda: invitee2.save())

    # Testing not-null constraint for registration token
    def test_registration_token_not_null_constraint(self):
        invitee = Invitee(email="volunteer1@example.com", message="Invitee to new user", created_by=self._director, registration_token=None)
        self.assertRaises(IntegrityError, lambda: invitee.save())

    # Testing max_lenght for token
    def test_token_max_length(self):
        invitee = Invitee.objects.get(id=1)
        max_length = invitee._meta.get_field('registration_token').max_length
        self.assertEqual(max_length, 150)

    # Testing default value for accepted
    def test_default_values(self):
        invitee = Invitee(email="volunteer3@example.com", message="Invitee to new user", created_by=self._director)
        invitee.save()
        self.assertEquals(invitee.resent_counter, 0)
        self.assertEquals(invitee.accepted, False)

    # Testing timestamps
    def test_it_has_timestamps(self):
        invitee = Invitee.objects.get(pk=1)
        self.assertIsInstance(invitee.created_at, datetime)
        self.assertIsInstance(invitee.updated_at, datetime)
