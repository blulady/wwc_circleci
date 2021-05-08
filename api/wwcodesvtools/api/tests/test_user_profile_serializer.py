from django.test import TestCase
from ..models import UserProfile, User
from api.serializers.UserProfileSerializer import UserProfileSerializer


class UserProfileSerializerTestCase(TestCase):

    def setUp(self):
        self.user_attributes = {
            "email": 'JohnDoe@example.com',
            "username": 'JohnDoe@example.com',
            "password": "passsword1"
        }
        self.new_user = User.objects.create_user(**self.user_attributes)
        self.user_profile = UserProfile.objects.get(user_id=self.new_user.id)

    def test_it_should_not_validate_if_status_is_blank(self):
        serializer = UserProfileSerializer(instance=self.user_profile, data={
            "status": ''
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['status']))

    def test_it_should_not_validate_if_status_invalid(self):
        serializer = UserProfileSerializer(instance=self.user_profile, data={
            "status": 'OBSOLETE'
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['status']))

    def test_it_should_save_userprofile_when_valid(self):
        serializer = UserProfileSerializer(instance=self.user_profile, data={
            "status": UserProfile.PENDING
        })
        self.assertTrue(serializer.is_valid())
        self.assertEquals(serializer.errors, {})
        serializer.save()

        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.status, UserProfile.PENDING)
