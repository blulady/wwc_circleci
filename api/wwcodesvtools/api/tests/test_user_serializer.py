from django.test import TestCase
from api.serializers.UserSerializer import UserSerializer


class UserSerializerTestCase(TestCase):

    def test_it_should_not_validate_if_username_missing(self):
        serializer = UserSerializer(data={
            'password': 'mypassword',
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['username']))

    def test_it_should_not_validate_if_password_missing(self):
        serializer = UserSerializer(data={
            'username': 'Jane@example.com',
        })

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['password']))

    def test_it_should_not_validate_if_user_email_is_invalid(self):
        serializer = UserSerializer(data={
            'email': 'Jan+e@Doe@Jane.com',
            'username': 'Jan+e@Doe@Jane.com',
            'password': 'password'
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['email']))

    def test_it_should_not_validate_if_email_and_username_not_same(self):
        serializer = UserSerializer(data={
            'email': 'JaneDoe@example.com',
            'username': 'JaneDoe',
            'password': 'password'
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['email_username']))

    def test_it_should_save_user_when_valid(self):
        serializer = UserSerializer(data={
            'email': 'JaneDoe@example.com',
            'username': 'JaneDoe@example.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'password': 'mypassword'
        })
        self.assertTrue(serializer.is_valid())
        self.assertEquals(serializer.errors, {})
        self.new_user = serializer.save()

        self.new_user.refresh_from_db()
        self.assertEquals(self.new_user.email, 'JaneDoe@example.com')
        self.assertEquals(self.new_user.username, 'JaneDoe@example.com')
        self.assertEquals(self.new_user.first_name, 'Jane')
        self.assertEquals(self.new_user.last_name, 'Doe')
        self.assertEqual(self.new_user.check_password('mypassword'), True)
