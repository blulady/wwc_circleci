import json
from django.test import TransactionTestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions as drf_exceptions
from rest_framework.permissions import AllowAny
from ..views.SetNewPasswordView import SetNewPasswordView


class SetNewPasswordViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']
    CONTENT_TYPE_APPLICATION_JSON = "application/json"

    def setUp(self):
        self.email = 'volunteer@example.com'
        self.old_password = 'Password123'
        self.user = User.objects.get(email=self.email)
        self.set_new_password_request_data = {
            "password": "Password1234",
            "email": self.email,
            "token": PasswordResetTokenGenerator().make_token(self.user)
        }

    def __send_request(self, data):
        set_new_password_api_url = "/api/user/reset_password/confirm/"
        return self.client.patch(
            set_new_password_api_url,
            data,
            accept=self.CONTENT_TYPE_APPLICATION_JSON,
            content_type=self.CONTENT_TYPE_APPLICATION_JSON,
        )

    # Test set new password api
    def test_set_new_password_successful(self):
        resp = self.__send_request(self.set_new_password_request_data)
        self.assertIs(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["success"], "Password reset successfully")
        # Check if you are able to login with the OLD password = False
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.email,
            'password': self.old_password,
        })
        with self.assertRaises(drf_exceptions.AuthenticationFailed):
            s.is_valid()
        # Check if you are able to login with the NEW password = True
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.email,
            'password': self.set_new_password_request_data["password"],
        })
        self.assertTrue(s.is_valid())
        self.assertIn('access', s.validated_data)
        self.assertIn('refresh', s.validated_data)
        # Check if you are able to reset again the password using the same token = False
        resp = self.__send_request(self.set_new_password_request_data)
        self.assertIs(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(resp.data["error"], "The reset link is invalid")

    # Test with password field missing in request data
    def test_password_required_fail(self):
        self.set_new_password_request_data.pop("password")
        expected_error = "This field is required."
        resp = self.__send_request(self.set_new_password_request_data)
        self.assertIs(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(resp.content), {'error': {'password': [expected_error]}})

    # Test password should not be blank
    def test_password_not_blank(self):
        self.set_new_password_request_data["password"] = ""
        expected_error = "This field may not be blank."
        resp = self.__send_request(self.set_new_password_request_data)
        self.assertIs(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(resp.content), {'error': {'password': [expected_error]}})

    # Test password should have at least 8 characters
    def test_password_field_length(self):
        self.set_new_password_request_data["password"] = "Pa5"
        expected_error = "Password should be a minimum of 8 and maximum of 50 characters long"
        resp = self.__send_request(self.set_new_password_request_data)
        self.assertIs(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(resp.content), {'error': {'password': [expected_error]}})

    # Test password should have at least one upper case letter
    def test_password_one_upper_case(self):
        self.set_new_password_request_data["password"] = "password123"
        expected_error = "Password should have at least one uppercase letter"
        resp = self.__send_request(self.set_new_password_request_data)
        self.assertIs(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(resp.content), {'error': {'password': [expected_error]}})

    # Test password should have at least one lower case letter
    def test_password_one_lower_case(self):
        self.set_new_password_request_data["password"] = "PASSWORD"
        expected_error = "Password should have at least one lowercase letter"
        resp = self.__send_request(self.set_new_password_request_data)
        self.assertIs(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(resp.content), {'error': {'password': [expected_error]}})

    # Test password should have at least one number
    def test_password_one_number(self):
        self.set_new_password_request_data["password"] = "Password"
        expected_error = "Password should have at least one number"
        resp = self.__send_request(self.set_new_password_request_data)
        self.assertIs(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(resp.content), {'error': {'password': [expected_error]}})

    # Test with email field missing in request data
    def test_email_required_fail(self):
        self.set_new_password_request_data.pop("email")
        expected_error = "Not found."
        resp = self.__send_request(self.set_new_password_request_data)
        self.assertIs(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(resp.content), {'detail': expected_error})

    # Test email should not be blank
    def test_email_not_blank(self):
        self.set_new_password_request_data["email"] = ""
        expected_error = "Not found."
        resp = self.__send_request(self.set_new_password_request_data)
        self.assertIs(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(resp.content), {'detail': expected_error})

    # Test with invalid email
    def test_invalid_email(self):
        self.set_new_password_request_data["email"] = "director@"
        expected_error = "Not found."
        resp = self.__send_request(self.set_new_password_request_data)
        self.assertIs(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(resp.content), {'detail': expected_error})

    # Test with email that doesn't exist in db
    def test_email_doesnt_exist(self):
        self.set_new_password_request_data["email"] = "director1@example.com"
        expected_error = "Not found."
        resp = self.__send_request(self.set_new_password_request_data)
        self.assertIs(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(resp.content), {'detail': expected_error})

    # Test with token field missing in request data
    def test_token_required_fail(self):
        self.set_new_password_request_data.pop("token")
        expected_error = "This field is required."
        resp = self.__send_request(self.set_new_password_request_data)
        self.assertIs(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(resp.content), {'error': {'token': [expected_error]}})

    # Test token should not be blank
    def test_token_not_blank(self):
        self.set_new_password_request_data["token"] = ""
        expected_error = "This field may not be blank."
        resp = self.__send_request(self.set_new_password_request_data)
        self.assertIs(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(resp.content), {'error': {'token': [expected_error]}})

    # Test with invalid token
    def test_invalid_token(self):
        self.set_new_password_request_data["token"] = "ajmexd-54417cf8a815baeb341418a33852ad0e"
        expected_error = "The reset link is invalid"
        resp = self.__send_request(self.set_new_password_request_data)
        self.assertIs(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(resp.content), {'error': expected_error})

    def test_set_new_password_view_permissions(self):
        view_permissions = SetNewPasswordView().permission_classes
        self.assertEqual(len(view_permissions), 1)
        self.assertEqual(view_permissions[0], AllowAny)
