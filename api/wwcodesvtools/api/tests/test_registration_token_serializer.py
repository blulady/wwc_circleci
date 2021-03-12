from django.test import TestCase
from ..models import User, RegistrationToken
from api.serializers.RegistrationTokenSerializer import RegistrationTokenSerializer


class RegistrationTokenSerializerTestCase(TestCase):
    def setUp(self):
        self.user_attributes = {
            "email": 'Martha@example.com',
            "username": 'Martha@example.com',
            "password": "passsword2"
        }
        self.new_user = User.objects.create_user(**self.user_attributes)
        self.registration_token = RegistrationToken.objects.get(user_id=self.new_user.id)

    def test_it_should_not_validate_if_token_is_blank(self):
        serializer = RegistrationTokenSerializer(instance=self.registration_token, data={
            "token": '',
            "used": False
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['token']))

    def test_it_should_not_validate_if_used_is_blank(self):
        serializer = RegistrationTokenSerializer(instance=self.registration_token, data={
            "token": "#%6token%#",
            "used": ''
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['used']))

    def test_it_should_not_validate_if_used_invalid(self):
        serializer = RegistrationTokenSerializer(instance=self.registration_token, data={
            "token": "#%6token%",
            "used": "Yesss"
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['used']))

    def test_it_should_not_validate_if_token_invalid(self):
        serializer = RegistrationTokenSerializer(instance=self.registration_token, data={
            "token": True,
            "used":  False
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['token']))

    def test_it_should_save_registration_token_when_valid(self):
        serializer = RegistrationTokenSerializer(instance=self.registration_token, data={
            "token": "#$%deftoken#",
            "used": False
        })
        self.assertTrue(serializer.is_valid())
        self.assertEquals(serializer.errors, {})
        serializer.save()

        self.registration_token.refresh_from_db()
        self.assertEqual(self.registration_token.token, "#$%deftoken#")
        self.assertEqual(self.registration_token.used, False)
