from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import User
from datetime import datetime


class GetMembersOrderingTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']
    DIRECTOR_EMAIL = 'director@example.com'
    LEADER_EMAIL = 'leader@example.com'
    VOLUNTEER_EMAIL = 'volunteer@example.com'
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

    # Testing get members ordering with role = DIRECTOR
    # first_name field ordered by "Ascending" order
    def test_get_members_ordering_by_first_name_asc(self):
        access_token = self.get_token(None)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=first_name", **bearer)

        # validate the ordering
        members = response.json()
        api_resp_data = [member['first_name'] for member in members]
        db_user_data = [entity for entity in User.objects.values_list('first_name', flat=True).order_by('first_name')]
        self.assertEqual(db_user_data, api_resp_data)

    # Testing get members ordering with role = DIRECTOR
    # first_name field ordered by "Descending" order
    def test_get_members_ordering_by_first_name_desc(self):
        access_token = self.get_token(None)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=-first_name", **bearer)

        # validate the ordering
        members = response.json()
        api_resp_data = [member['first_name'] for member in members]
        db_user_data = [entity for entity in User.objects.values_list('first_name', flat=True).order_by('-first_name')]
        self.assertEqual(db_user_data, api_resp_data)

    # Testing get members ordering with role = LEADER
    # last_name field ordered by "Ascending" order
    def test_get_members_ordering_by_last_name_asc(self):
        access_token = self.get_token(self.LEADER_EMAIL)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=last_name", **bearer)

        # validate the ordering
        members = response.json()
        api_resp_data = [member['last_name'] for member in members]
        db_user_data = [entity for entity in User.objects.values_list('last_name', flat=True).order_by('last_name').exclude(userprofile__status='PENDING')]
        self.assertEqual(db_user_data, api_resp_data)

    # Testing get members ordering with role = LEADER
    # last_name field ordered by "Descending" order
    def test_get_members_ordering_by_last_name_desc(self):
        access_token = self.get_token(self.LEADER_EMAIL)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=-last_name", **bearer)

        # validate the ordering
        members = response.json()
        api_resp_data = [member['last_name'] for member in members]
        db_user_data = [entity for entity in User.objects.values_list('last_name', flat=True).order_by('-last_name').exclude(userprofile__status='PENDING')]
        self.assertEqual(db_user_data, api_resp_data)

    # Testing get members ordering with role = VOLUNTEER
    # date_joined field ordered by "Ascending" order
    def test_get_members_ordering_by_date_joined_asc(self):
        access_token = self.get_token(self.VOLUNTEER_EMAIL)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=date_joined", **bearer)

        # validate the ordering
        members = response.json()
        api_resp_data = [member['date_joined'] for member in members]
        db_user_data = [datetime.strftime(entity, "%Y-%m-%dT%H:%M:%S.%fZ") for entity in User.objects.values_list('date_joined', flat=True).order_by('date_joined').exclude(userprofile__status='PENDING')]
        self.assertEqual(db_user_data, api_resp_data)

    # Testing get members ordering with role = VOLUNTEER
    # date_joined field ordered by "Descending" order
    def test_get_members_ordering_by_date_joined_desc(self):
        access_token = self.get_token(self.VOLUNTEER_EMAIL)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=-date_joined", **bearer)

        # validate the ordering
        members = response.json()
        api_resp_data = [member['date_joined'] for member in members]
        db_user_data = [datetime.strftime(entity, "%Y-%m-%dT%H:%M:%S.%fZ") for entity in User.objects.values_list('date_joined', flat=True).order_by('-date_joined').exclude(userprofile__status='PENDING')]
        self.assertEqual(db_user_data, api_resp_data)
