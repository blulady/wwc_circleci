import json
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class GetMembersViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['get_members_data.json']

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # Testing get members with role = DIRECTOR
    # 'PENDING' status members and 'email' field are in the response
    def test_get_members_role_director(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 4)
        self.assertEqual(json.loads(response.content)[0]['id'], 4)
        self.assertEqual(json.loads(response.content)[0]['email'], 'leaderPendingStatus@example.com')
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'Caroline')
        self.assertEqual(json.loads(response.content)[0]['last_name'], 'Miller')
        self.assertEqual(json.loads(response.content)[0]['status'], 'PENDING')
        self.assertEqual(json.loads(response.content)[0]['role'], 'LEADER')
        self.assertEqual(json.loads(response.content)[0]['date_joined'], '2021-02-19T01:56:51.160000Z')
        for i in range(responseLength):
            self.assertIsNotNone(json.loads(response.content)[i]['email'])

    # Testing get members with role = VOLUNTEER
    # 'PENDING' status members and 'email' field not in the response
    def test_get_members_role_volunteer(self):
        self.username = 'volunteer@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 3)
        self.assertEqual(json.loads(response.content)[0]['id'], 3)
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'Bruno')
        self.assertEqual(json.loads(response.content)[0]['last_name'], 'Clark')
        self.assertEqual(json.loads(response.content)[0]['role'], 'LEADER')
        self.assertEqual(json.loads(response.content)[0]['date_joined'], '2021-02-19T01:56:29.756000Z')
        self.assertEqual(json.loads(response.content)[0]['status'], 'ACTIVE')
        for i in range(responseLength):
            self.assertRaises(KeyError, lambda: json.loads(response.content)[i]['email'])
            self.assertNotEqual(json.loads(response.content)[i]['status'], 'PENDING')

    # Testing get members with role = LEADER
    # 'PENDING' status members and 'email' field not in the response
    def test_get_members_role_leader(self):
        self.username = 'leader@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 3)
        self.assertEqual(json.loads(response.content)[0]['id'], 3)
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'Bruno')
        self.assertEqual(json.loads(response.content)[0]['last_name'], 'Clark')
        self.assertEqual(json.loads(response.content)[0]['role'], 'LEADER')
        self.assertEqual(json.loads(response.content)[0]['date_joined'], '2021-02-19T01:56:29.756000Z')
        self.assertEqual(json.loads(response.content)[0]['status'], 'ACTIVE')
        for i in range(responseLength):
            self.assertRaises(KeyError, lambda: json.loads(response.content)[i]['email'])
            self.assertNotEqual(json.loads(response.content)[i]['status'], 'PENDING')
