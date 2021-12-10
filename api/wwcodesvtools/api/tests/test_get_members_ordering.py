import json
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class GetMembersOrderingTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # Testing get members ordering with role = DIRECTOR
    # first_name field ordered by "Ascending" order
    def test_get_members_ordering_by_first_name_asc(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=first_name", **bearer)
        responseLength = len(response.data)
        members = json.loads(response.content)
        for ix in range(1, responseLength):
            self.assertLessEqual(members[ix-1]['first_name'], members[ix]['first_name'])

    # Testing get members ordering with role = DIRECTOR
    # first_name field ordered by "Descending" order
    def test_get_members_ordering_by_first_name_desc(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=-first_name", **bearer)
        responseLength = len(response.data)
        members = json.loads(response.content)
        for ix in range(1, responseLength):
            self.assertLessEqual(members[ix]['first_name'], members[ix-1]['first_name'])

    # Testing get members ordering with role = LEADER
    # last_name field ordered by "Ascending" order
    def test_get_members_ordering_by_last_name_asc(self):
        self.username = 'leader@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=last_name", **bearer)
        responseLength = len(response.data)
        members = json.loads(response.content)
        for ix in range(1, responseLength):
            self.assertLessEqual(members[ix-1]['last_name'], members[ix]['last_name'])

    # Testing get members ordering with role = LEADER
    # last_name field ordered by "Descending" order
    def test_get_members_ordering_by_last_name_desc(self):
        self.username = 'leader@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=-last_name", **bearer)
        responseLength = len(response.data)
        members = json.loads(response.content)
        for ix in range(1, responseLength):
            self.assertLessEqual(members[ix]['last_name'], members[ix-1]['last_name'])
    
    # Testing get members ordering with role = VOLUNTEER
    # date_joined field ordered by "Ascending" order
    def test_get_members_ordering_by_date_joined_asc(self):
        self.username = 'volunteer@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=date_joined", **bearer)
        responseLength = len(response.data)
        members = json.loads(response.content)
        for ix in range(1, responseLength):
            self.assertLess(members[ix - 1]['date_joined'], members[ix]['date_joined'])

    # Testing get members ordering with role = VOLUNTEER
    # date_joined field ordered by "Descending" order
    def test_get_members_ordering_by_date_joined_desc(self):
        self.username = 'volunteer@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=-date_joined", **bearer)
        responseLength = len(response.data)
        members = json.loads(response.content)
        for ix in range(1, responseLength):
            self.assertGreater(members[ix-1]['date_joined'], members[ix]['date_joined'])
