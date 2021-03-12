from django.test import TestCase
from ..models import UserProfile


class UserProfileTestCase(TestCase):

    def test_userprofile_is_pending(self):
        user_profile = UserProfile(user=None, status=UserProfile.PENDING)
        self.assertIs(user_profile.is_pending(), True)
