from django.test import TransactionTestCase
from rest_framework import status
from rest_framework.permissions import AllowAny
from ...views.ValidateRegLinkView import ValidateRegLinkView
from ...models import Invitee, Role
from django.contrib.auth.models import User
from datetime import datetime


class ValidateRegLinkViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json', 'invitee.json']

    DIRECTOR_EMAIL = 'director@example.com'
    PASSWORD = 'Password123'
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    token = f"abcdefa0342a4330bc790f23ac70a7b6{now}"

    USER_TOKEN_MISMATCH_MESSAGE = 'Invalid token. Token in request does not match the token generated for this user.'
    USER_TOKEN_EXPIRED_MESSAGE = 'Token is expired'
    USER_TOKEN_ALREADY_USED_MESSAGE = 'Token is already used'
    USER_ALREADY_ACTIVE_MESSAGE = 'There is already an active user associated with this email'
    USER_TOKEN_NOT_FOUND_ERROR_MESSAGE = 'Email/Token does not exist in our invites system. You need to be invited to be able to register.'
    VALID_TOKEN_MESSAGE = 'Token is valid'

    def create_invitee(self):
        invitee = Invitee(email="volunteer1@example.com",
                          message="Invitee testing",
                          role=Role.objects.get(name='VOLUNTEER'),
                          registration_token=self.token,
                          resent_counter=0,
                          accepted=False,
                          created_by=User.objects.get(email=self.DIRECTOR_EMAIL)
                          )
        invitee.save()

    def test_validate_active_user(self):
        data = {"email": "vincenttaylor@example.com",
                "token": "62080e2bb45e4b8588a83f4582acc8f420500119173010"}
        response = self.client.get("/api/validate/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'detail': {'message': self.USER_ALREADY_ACTIVE_MESSAGE, 'status': 'ACTIVE'}})

    def test_validate_token_mismatch(self):
        data = {"email": "volunteer_3@example.com",
                "token": "8b7bd00fffa742ed836539f0acce6ce920230525000234"}
        response = self.client.get("/api/validate/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'detail': {'message': self.USER_TOKEN_MISMATCH_MESSAGE, 'status': 'INVALID'}})

    def test_validate_token_expired(self):
        data = {"email": "volunteer_3@example.com",
                "token": "93f9f678565b4f1783dba9028801c1de20210624235504"}
        response = self.client.get("/api/validate/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'detail': {'message': self.USER_TOKEN_EXPIRED_MESSAGE, 'status': 'EXPIRED'}})

    def test_validate_token_valid(self):
        self.create_invitee()
        data = {"email": "volunteer1@example.com",
                "token": self.token}
        response = self.client.get("/api/validate/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'detail': {'message': self.VALID_TOKEN_MESSAGE, 'status': 'VALID'}})

    def test_validate_email_token_not_found(self):
        data = {"email": "example@example.com",
                "token": "938d60469dc74cceae396f2c963f105520500219015651"}
        response = self.client.get("/api/validate/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'detail': {'message': self.USER_TOKEN_NOT_FOUND_ERROR_MESSAGE, 'status': 'NONEXISTENT'}})

    def test_validate_reg_link_view_permissions(self):
        view_permissions = ValidateRegLinkView().permission_classes
        self.assertEqual(len(view_permissions), 1)
        self.assertEqual(view_permissions[0], AllowAny)
