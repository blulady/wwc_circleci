from django.test import TransactionTestCase
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
import json


class ChangePasswordViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']

    def setUp(self):
        self.access_token = self.get_token('volunteer@example.com', 'Password123')
        self.bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.access_token)}

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: username,
            'password': password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    def patch_request(self, data, bearer):
        change_password_url = "/api/user/password/"
        return self.client.patch(f'{change_password_url}', data, **bearer,
                                 accept="application/json",
                                 content_type="application/json",)

    def test_change_password_success(self):
        user = User.objects.get(email='volunteer@example.com')
        new_password = "Password456"
        self.assertFalse(check_password(new_password, user.password))
        result = self.patch_request({"password": new_password}, self.bearer)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(check_password(new_password, user.password))

    def test_missing_uppercase(self):
        data = {"password": "password1"}
        result = self.patch_request(data, self.bearer)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(result.content), {'error': ['Password should have at least one uppercase letter']})
# TODO wirte tests for 500 Internal error  and serializer error scenario
