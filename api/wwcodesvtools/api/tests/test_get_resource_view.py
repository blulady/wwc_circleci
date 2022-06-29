from api.models import Resource
from rest_framework import status
from django.test import TransactionTestCase
# from ..views.GetResourceView import GetResourceView
from api.views.resources_view import ResourceViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class GetResourceViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json', 'resources_data.json']
    DIRECTOR_EMAIL = 'director@example.com'
    LEADER_EMAIL = 'leader@example.com'
    PASSWORD = 'Password123'

    def get_token(self, username):
        self.username = username or self.DIRECTOR_EMAIL
        self.password = self.PASSWORD
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # Testing resources endpoint with valid slug with role = Director
    def test_resources_valid_slug_director(self):
        access_token = self.get_token(None)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/resources/volunteer_resource/", **bearer)
        expected_link = Resource.objects.get(slug='volunteer_resource')
        data_json = response.json()
        self.assertEqual(expected_link.edit_link, data_json['edit_link'])
        self.assertEqual(expected_link.published_link, data_json['published_link'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing resources endpoint with valid slug with role = Leader
    def test_resources_valid_slug_leader(self):
        access_token = self.get_token(self.LEADER_EMAIL)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/resources/volunteer_resource/", **bearer)
        expected_link = Resource.objects.get(slug='volunteer_resource')
        data_json = response.json()
        self.assertNotIn('edit_link', data_json)
        self.assertEqual(expected_link.published_link, data_json['published_link'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing resources endpoint with invalid slug
    def test_resources_invalid_slug(self):
        access_token = self.get_token(self.LEADER_EMAIL)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/resources/volunteer_onboarding/", **bearer)
        data_json = response.json()
        self.assertEqual(data_json['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_resources_view_permissions(self):
        view_permissions = ResourceViewSet().permission_classes
        self.assertEqual(len(view_permissions), 1)
        self.assertEqual(view_permissions[0], IsAuthenticated)
