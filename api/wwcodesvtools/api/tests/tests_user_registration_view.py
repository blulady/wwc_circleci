from django.test import TransactionTestCase
from django.contrib.auth.models import User
from rest_framework import status
from ..models import RegistrationToken, UserProfile


class UserRegistrationViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']
    CONTENT_TYPE_APPLICATION_JSON = "application/json"

    def setUp(self):
        self.registration_request_data = {
            "email": "leaderPendingStatus@example.com",
            "first_name": "Caroline",
            "last_name": "Miller",
            "password": "Password123",
            "token": "938d60469dc74cceae396f2c963f105520500219015651",
        }

    def __send_request(self, data):
        registration_api_url = "/api/user/activate/"
        return self.client.post(
            registration_api_url,
            data,
            accept=self.CONTENT_TYPE_APPLICATION_JSON,
            content_type=self.CONTENT_TYPE_APPLICATION_JSON,
        )

    def __perform_response_assertions(self, resp, expected_status, expected_error):
        self.assertEqual(resp.status_code, expected_status)
        self.assertEqual(resp["content-type"], self.CONTENT_TYPE_APPLICATION_JSON)
        self.assertEqual(resp.data["error"], expected_error)

    # Test new user can complete registration
    def test_successful_user_registration(self):
        """
        Test to verify that on a POST call with a new user having valid token, registration is successful

        """
        resp = self.__send_request(self.registration_request_data)
        successfully_updated_status_code = 201
        self.assertIs(resp.status_code, successfully_updated_status_code)
        self.assertEqual(resp["content-type"], self.CONTENT_TYPE_APPLICATION_JSON)
        self.assertEqual(resp.data["result"], "User Activated Succesfully")
        # Check user status is now ACTIVE
        user_email = self.registration_request_data["email"]
        registered_user = User.objects.get(email=user_email)
        self.assertEqual(registered_user.userprofile.status, UserProfile.ACTIVE)
        # Check token is marked as used
        token = RegistrationToken.objects.get(token=self.registration_request_data["token"])
        self.assertTrue(token.used)

    # Test with password field missing in request data
    def test_password_required_fail(self):
        """
        Test to verify that a POST call with no password data returns bad request error response.
        Error message specifies password field is required.
        """
        self.registration_request_data.pop("password")
        expected_error = "Invalid Request. Key not present in request : 'password'"
        resp = self.__send_request(self.registration_request_data)
        self.__perform_response_assertions(resp, status.HTTP_400_BAD_REQUEST, expected_error)

    # Test new user with token missing in request data
    def test_token_required_fail(self):
        """
        Test to verify that a POST call with no token data returns bad request error response
        """
        self.registration_request_data.pop("token")
        expected_error = "Invalid Request. Key not present in request : 'token'"
        resp = self.__send_request(self.registration_request_data)
        self.__perform_response_assertions(resp, status.HTTP_400_BAD_REQUEST, expected_error)

    # Test new user with email missing in request data
    def test_email_required_fail(self):
        """
        Test to verify that a POST call with no token data returns bad request error response
        """
        self.registration_request_data.pop("email")
        expected_error = "Invalid Request. Key not present in request : 'email'"
        resp = self.__send_request(self.registration_request_data)
        self.__perform_response_assertions(resp, status.HTTP_400_BAD_REQUEST, expected_error)

    # Test new user with first name missing in request data
    def test_first_name_required_fail(self):
        """
        Test to verify that a POST call with no token data returns bad request error response
        """
        self.registration_request_data.pop("first_name")
        expected_error = "Invalid Request. Key not present in request : 'first_name'"
        resp = self.__send_request(self.registration_request_data)
        self.__perform_response_assertions(resp, status.HTTP_400_BAD_REQUEST, expected_error)

    # Test new user with last name missing in request data
    def test_last_name_required_fail(self):
        """
        Test to verify that a POST call with no token data returns bad request error response
        """
        self.registration_request_data.pop("last_name")
        expected_error = "Invalid Request. Key not present in request : 'last_name'"
        resp = self.__send_request(self.registration_request_data)
        self.__perform_response_assertions(resp, status.HTTP_400_BAD_REQUEST, expected_error)

    # Test new valid user with non-existing token
    def test_invalid_token_fail(self):
        """
        Test to verify that a POST call with valid user but non-existing token return invalid token
        response.
        """
        self.registration_request_data["token"] = "abcdefa0342a4330bc790f23ac70a7b620220214015340"
        expected_error = "Invalid token. Token does not exist in our system."
        resp = self.__send_request(self.registration_request_data)
        self.__perform_response_assertions(resp, status.HTTP_404_NOT_FOUND, expected_error)

    # Test invited email with mismatched token
    def test_newuser_mismatched_token(self):
        """
        Test to verify that a POST request with valid new user and mismatched valid token
        returns error response
        """
        self.registration_request_data["token"] = "8b7bd00fffa742ed836539f0acce6ce920220525000234"
        expected_error = "Invalid token. Token in request does not match the token generated for this user."
        resp = self.__send_request(self.registration_request_data)
        self.__perform_response_assertions(resp, status.HTTP_400_BAD_REQUEST, expected_error)

    # Test Active User trying to register
    def test_ActiveUser_Register_fail(self):
        """
        Test to verify that a POST call with Active User returns error response
        """
        self.registration_request_data["email"] = "volunteer@example.com"
        expected_error = "User is already registered and Active"
        resp = self.__send_request(self.registration_request_data)
        self.__perform_response_assertions(resp, status.HTTP_400_BAD_REQUEST, expected_error)

    # Test user with Invalid email sent to register
    def test_invalid_not_present_in_db_email_fail(self):
        """
        Test to verify that a post call with the User with Invalid email registration fails.
        Returns error response.
        """
        self.registration_request_data["email"] = "test_invalidemail@domain.com"
        expected_error = "Email does not exist in our invites system. You need to be invited to be able to register."
        resp = self.__send_request(self.registration_request_data)
        self.__perform_response_assertions(resp, status.HTTP_404_NOT_FOUND, expected_error)
