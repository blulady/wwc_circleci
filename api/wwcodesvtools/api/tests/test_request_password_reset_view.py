import json
from django.test import TransactionTestCase, override_settings
from rest_framework import status
from django.conf import settings
from django.core import mail
from django.utils.http import urlencode
from django.utils.html import escape
from ..helper_functions import send_email_helper


class RequestPasswordResetViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json']
    EXPECTED_MESSAGE = "We have sent you a link to reset your password"

    # test request reset password fails with blank email
    def test_request_reset_password_fails_with_blank_email(self):
        data = {"email": ''}
        response = self.client.post("/api/user/reset_password/request/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(json.loads(response.content)['error'].keys()), set(['email']))

    # test request reset password fails with invalid email
    def test_request_reset_password_fails_with_invalid_email(self):
        data = {"email": "hello@123"}
        response = self.client.post("/api/user/reset_password/request/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', json.loads(response.content)['error'])

    # test request reset password fails if email does not exist
    def test_request_reset_password_fails_email_doesnot_exist(self):
        data = {"email": "leaderrrr@example.com"}
        response = self.client.post("/api/user/reset_password/request/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', json.loads(response.content)['error'])

    # test request reset password email sent with valid data
    def test_request_reset_password_sent_with_valid_data(self):
        data = {"email": "volunteer@example.com"}
        response = self.client.post("/api/user/reset_password/request/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'success': self.EXPECTED_MESSAGE})

    # Test the reset_password link in the password reset notification email message
    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_reset_password_notification_link(self):
        email = "++Mary--Shaw@example.com"
        first_name = 'Mary'
        last_name = 'Shaw'
        token = "alzzo5-3e9de98f260e4abb8177846acb569305"
        password_reset_confirm = f'{settings.FRONTEND_APP_URL}/password/reset?{urlencode({"email": email, "token": token})}'
        context_data = {"user": f'{first_name} {last_name}',
                        "password_reset_confirm": password_reset_confirm
                        }
        send_email_helper(email, 'Password Reset Requested', 'request_reset_password.html', context_data)

        expected_encoded_email_param = "email=%2B%2BMary--Shaw%40example.com"
        expected_encoded_token_param = "token=alzzo5-3e9de98f260e4abb8177846acb569305"
        expected_host_api_endpoint = "https://wwcode-chtools-fe.herokuapp.com/password/reset?"

        # Verify that one email message has been sent.
        self.assertEquals(len(mail.outbox), 1)
        # Verify that the "subject" of the message is correct.
        self.assertEquals(mail.outbox[0].subject, 'Password Reset Requested')
        # Verify that the "to" of the message is correct.
        self.assertEquals(mail.outbox[0].to, ['++Mary--Shaw@example.com'])
        # Verify the request reset password link url in the email html message body
        self.assertIn(escape(password_reset_confirm), mail.outbox[0].body)
        # verify the encoded email param
        self.assertIn(expected_encoded_email_param, mail.outbox[0].body)
        # verify the encoded token param
        self.assertIn(expected_encoded_token_param, mail.outbox[0].body)
        # verify the host api_endpoint
        self.assertIn(expected_host_api_endpoint, mail.outbox[0].body)
