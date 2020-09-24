from django.test import TestCase
from .models import UserProfile
# Create your tests here.


class UserProfileTests(TestCase):

    def test_userprofile_is_new(self):
        us = UserProfile(user=None, status=UserProfile.NEW)
        self.assertIs(us.is_new(), True)

