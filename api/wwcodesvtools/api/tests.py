from django.core import mail
from django.test import TestCase, override_settings
from .helper_functions import sendmail_helper
from .models import UserProfile

# Create your tests here.
class UserProfileTests(TestCase):

    def test_userprofile_is_new(self):
        us = UserProfile(user=None, status=UserProfile.NEW)
        self.assertIs(us.is_new(), True)
        
class helperFunctionsTest(TestCase):

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_sendmail_helper(self):
        toEmail = 'WWCodeSV@gmail.com'
        subject = 'Welcome to WWCode-SV'
        templateFile = 'welcome_sample.html'
        contextData = {"user": "UserName",
                       "registrationLink": "https://login.yahoo.com/account/create",
                       "socialMediaLink": "https://www.linkedin.com/company/women-who-code/"
                       }
        sendmail_helper(toEmail, subject, templateFile, contextData)

        # Test that one message has been sent.
        self.assertEquals(len(mail.outbox), 1)

        # Verify that the "subject" of the first message is correct.
        self.assertEquals(mail.outbox[0].subject, 'Welcome to WWCode-SV')

        # Verify that the "to" of the first message is correct.
        self.assertEquals(mail.outbox[0].to, ['WWCodeSV@gmail.com'])