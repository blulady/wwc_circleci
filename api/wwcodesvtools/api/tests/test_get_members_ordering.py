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
        self.assertEqual(responseLength, 9)
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'Alexander')
        self.assertEqual(json.loads(response.content)[1]['first_name'], 'Alice')
        self.assertEqual(json.loads(response.content)[2]['first_name'], 'Brenda')
        self.assertEqual(json.loads(response.content)[3]['first_name'], 'Bruno')
        self.assertEqual(json.loads(response.content)[4]['first_name'], 'Caroline')
        self.assertEqual(json.loads(response.content)[5]['first_name'], 'Jack')
        self.assertEqual(json.loads(response.content)[6]['first_name'], 'John')
        self.assertEqual(json.loads(response.content)[7]['first_name'], 'Sophie')
        self.assertEqual(json.loads(response.content)[8]['first_name'], 'Sophie')

    # Testing get members ordering with role = DIRECTOR
    # first_name field ordered by "Descending" order
    def test_get_members_ordering_by_first_name_desc(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=-first_name", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 9)
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'Sophie')
        self.assertEqual(json.loads(response.content)[1]['first_name'], 'Sophie')
        self.assertEqual(json.loads(response.content)[2]['first_name'], 'John')
        self.assertEqual(json.loads(response.content)[3]['first_name'], 'Jack')
        self.assertEqual(json.loads(response.content)[4]['first_name'], 'Caroline')
        self.assertEqual(json.loads(response.content)[5]['first_name'], 'Bruno')
        self.assertEqual(json.loads(response.content)[6]['first_name'], 'Brenda')
        self.assertEqual(json.loads(response.content)[7]['first_name'], 'Alice')
        self.assertEqual(json.loads(response.content)[8]['first_name'], 'Alexander')

    # Testing get members ordering with role = LEADER
    # last_name field ordered by "Ascending" order
    def test_get_members_ordering_by_last_name_asc(self):
        self.username = 'leader@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=last_name", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 7)
        self.assertEqual(json.loads(response.content)[0]['last_name'], 'Brown')
        self.assertEqual(json.loads(response.content)[1]['last_name'], 'Butler')
        self.assertEqual(json.loads(response.content)[2]['last_name'], 'Clark')
        self.assertEqual(json.loads(response.content)[3]['last_name'], 'Fisher')
        self.assertEqual(json.loads(response.content)[4]['last_name'], 'Jackson')
        self.assertEqual(json.loads(response.content)[5]['last_name'], 'Robinson')
        self.assertEqual(json.loads(response.content)[6]['last_name'], 'Smith')

    # Testing get members ordering with role = LEADER
    # last_name field ordered by "Descending" order
    def test_get_members_ordering_by_last_name_desc(self):
        self.username = 'leader@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=-last_name", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 7)
        self.assertEqual(json.loads(response.content)[0]['last_name'], 'Smith')
        self.assertEqual(json.loads(response.content)[1]['last_name'], 'Robinson')
        self.assertEqual(json.loads(response.content)[2]['last_name'], 'Jackson')
        self.assertEqual(json.loads(response.content)[3]['last_name'], 'Fisher')
        self.assertEqual(json.loads(response.content)[4]['last_name'], 'Clark')
        self.assertEqual(json.loads(response.content)[5]['last_name'], 'Butler')
        self.assertEqual(json.loads(response.content)[6]['last_name'], 'Brown')

    # Testing get members ordering with role = VOLUNTEER
    # date_joined field ordered by "Ascending" order
    def test_get_members_ordering_by_date_joined_asc(self):
        self.username = 'volunteer@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=date_joined", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 7)
        self.assertEqual(json.loads(response.content)[0]['date_joined'], '2021-02-19T01:55:01.810000Z')
        self.assertEqual(json.loads(response.content)[1]['date_joined'], '2021-02-19T01:56:06.115000Z')
        self.assertEqual(json.loads(response.content)[2]['date_joined'], '2021-02-19T01:56:29.756000Z')
        self.assertEqual(json.loads(response.content)[3]['date_joined'], '2021-05-24T23:50:53.484000Z')
        self.assertEqual(json.loads(response.content)[4]['date_joined'], '2021-05-24T23:55:04.556000Z')
        self.assertEqual(json.loads(response.content)[5]['date_joined'], '2021-05-25T00:00:52.353000Z')
        self.assertEqual(json.loads(response.content)[6]['date_joined'], '2021-05-27T21:34:01.149000Z')

    # Testing get members ordering with role = VOLUNTEER
    # date_joined field ordered by "Descending" order
    def test_get_members_ordering_by_date_joined_desc(self):
        self.username = 'volunteer@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=-date_joined", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 7)
        self.assertEqual(json.loads(response.content)[0]['date_joined'], '2021-05-27T21:34:01.149000Z')
        self.assertEqual(json.loads(response.content)[1]['date_joined'], '2021-05-25T00:00:52.353000Z')
        self.assertEqual(json.loads(response.content)[2]['date_joined'], '2021-05-24T23:55:04.556000Z')
        self.assertEqual(json.loads(response.content)[3]['date_joined'], '2021-05-24T23:50:53.484000Z')
        self.assertEqual(json.loads(response.content)[4]['date_joined'], '2021-02-19T01:56:29.756000Z')
        self.assertEqual(json.loads(response.content)[5]['date_joined'], '2021-02-19T01:56:06.115000Z')
        self.assertEqual(json.loads(response.content)[6]['date_joined'], '2021-02-19T01:55:01.810000Z')
