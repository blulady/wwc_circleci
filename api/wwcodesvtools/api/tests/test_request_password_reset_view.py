import json
from django.test import TransactionTestCase
from rest_framework import status


class RequestPasswordResetViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json']

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
        self.assertIn('token', json.loads(response.content))
