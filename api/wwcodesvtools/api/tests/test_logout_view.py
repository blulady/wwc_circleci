import json
from django.test import TransactionTestCase
from rest_framework import status
from api.serializers.CustomTokenObtainPairSerializer import CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from ..views.LogoutView import LogoutView


class LogoutViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']

    def get_token(self, username, password):
        s = CustomTokenObtainPairSerializer(data={
            CustomTokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data

    def test_refresh_token_is_blacklisted_after_logout(self):
        self.username = 'volunteer@example.com'
        self.password = 'Password123'
        token_data = self.get_token(self.username, self.password)
        access_token = token_data['access']
        refresh_token = token_data['refresh']
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}

        logout_response = self.client.post("/api/logout/", **bearer)
        self.assertEqual(logout_response.status_code, status.HTTP_205_RESET_CONTENT)

        data = {"refresh": refresh_token}
        refresh_response = self.client.post("/api/login/refresh/", data, **bearer)
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(refresh_response.content)['detail'], "Token is blacklisted")
        self.assertEqual(json.loads(refresh_response.content)['code'], "token_not_valid")

    def test_logout_view_permissions(self):
        view_permissions = LogoutView().permission_classes
        self.assertEqual(len(view_permissions), 1)
        self.assertEqual(view_permissions[0], IsAuthenticated)
