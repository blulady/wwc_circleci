from django.test import TestCase
from ..models import UserProfile
from api.serializers.AddMemberSerializer import AddMemberSerializer


class AddMemberSerializerTestCase(TestCase):

    def test_it_should_not_validate_if_email_is_blank(self):
        serializer = AddMemberSerializer(data={
            "email": '',
            "role": 'LEADER',
            "message": 'test message'
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['email']))

    def test_it_should_not_validate_if_role_is_blank(self):
        serializer = AddMemberSerializer(data={
            "email": 'jane@jane.com',
            "role": '',
            "message": 'test message'
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['role']))

    def test_it_should_not_validate_if_email_is_invalid(self):
        serializer = AddMemberSerializer(data={
            "email": "newUser'semail@$@example.com",
            "role": UserProfile.DIRECTOR,
            "message": ""
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['email']))

    def test_it_should_not_validate_if_role_invalid(self):
        serializer = AddMemberSerializer(data={
            'email': 'newUser@example.com',
            "role": 'PRESIDENT',
            "message": "test message"
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['role']))

    def test_it_should_validate_if_message_is_blank(self):
        serializer = AddMemberSerializer(data={
            "email": 'newMember@example.com',
            "role": UserProfile.LEADER,
            "message": ""
        })
        self.assertTrue(serializer.is_valid())
        self.assertEquals(serializer.errors, {})

    def test_it_should_validate_when_valid_data(self):
        serializer = AddMemberSerializer(data={
            "email": 'newUser@example.com',
            "role": UserProfile.VOLUNTEER,
            "message": "optional message"
        })
        self.assertTrue(serializer.is_valid())
        self.assertEquals(serializer.errors, {})
