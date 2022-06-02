from django.test import TransactionTestCase
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..views.ValidateRegLinkView import ValidateRegLinkView


class ValidateRegLinkViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']
    USER_TOKEN_MISMATCH_MESSAGE = 'Invalid token. Token in request does not match the token generated for this user.'
    USER_TOKEN_EXPIRED_MESSAGE = 'Token has expired'
    USER_TOKEN_ALREADY_USED_MESSAGE = 'Token is already used'
    VALID_TOKEN_MESSAGE = 'Toke is valid'
    NOT_FOUND = 'Not found.'

    def test_validate_token_used(self):
        data = {"email": "vincenttaylor@example.com",
                "token": "62080e2bb45e4b8588a83f4582acc8f420500119173010"}
        response = self.client.get("/api/validate/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'success': {'message': self.USER_TOKEN_ALREADY_USED_MESSAGE, 'status': 'USED'}})

    def test_validate_token_mismatch(self):
        data = {"email": "volunteer@example.com",
                "token": "8b7bd00fffa742ed836539f0acce6ce920230525000234"}
        response = self.client.get("/api/validate/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'success': {'message': self.USER_TOKEN_MISMATCH_MESSAGE, 'status': 'INVALID'}})

    def test_validate_token_expired(self):
        data = {"email": "thomasparker@example.com",
                "token": "5f6a1048ef694b1692f3b7766caa56b920200527213401"}
        response = self.client.get("/api/validate/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'success': {'message': self.USER_TOKEN_EXPIRED_MESSAGE, 'status': 'EXPIRED'}})

    def test_validate_token_valid(self):
        data = {"email": "leaderPendingStatus@example.com",
                "token": "938d60469dc74cceae396f2c963f105520500219015651"}
        response = self.client.get("/api/validate/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'success': {'message': self.VALID_TOKEN_MESSAGE, 'status': 'VALID'}})

    def test_validate_email_not_found(self):
        data = {"email": "example@example.com",
                "token": "938d60469dc74cceae396f2c963f105520500219015651"}
        response = self.client.get("/api/validate/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'detail': self.NOT_FOUND})

    def test_validate_token_not_found(self):
        data = {"email": "leader@example.com",
                "token": "938d60469dc74cceae396f2c963f1055205002190156519"}
        response = self.client.get("/api/validate/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'detail': self.NOT_FOUND})

    def test_validate_reg_link_view_permissions(self):
        view_permissions = ValidateRegLinkView().permission_classes
        self.assertEqual(len(view_permissions), 1)
        self.assertEqual(view_permissions[0], AllowAny)
