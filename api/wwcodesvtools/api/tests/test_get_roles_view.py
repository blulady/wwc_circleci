import json
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from ..views.RolesView import RolesView


class RolesViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    def test_get_roles(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/roles/", **bearer)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(json.loads(response.content)[0]['name'], 'VOLUNTEER')
        self.assertEqual(json.loads(response.content)[1]['name'], 'LEADER')
        self.assertEqual(json.loads(response.content)[2]['name'], 'DIRECTOR')

    def test_get_roles_view_permissions(self):
        view_permissions = RolesView().permission_classes
        self.assertEqual(len(view_permissions), 1)
        self.assertEqual(view_permissions[0], IsAuthenticated)
