
import json
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import UserProfile
from rest_framework import status


class AddMemberViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json']
    EXPECTED_MESSAGE = 'You do not have permission to perform this action.'

    def setUp(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        self.access_token = self.get_token(self.username, self.password)
        self.bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.access_token)}

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # test add member fails with blank email
    def test_add_member_fails_with_blank_email(self):
        data = {"email": '',
                "role": 'VOLUNTEER',
                "message": "optional message"
                }
        response = self.client.post("/api/user/create/", data, **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(json.loads(response.content)['error'].keys()), set(['email']))

    # test add member fails with blank role
    def test_add_member_fails_with_blank_role(self):
        data = {"email": "WWCodeSV@gmail.com",
                "role": '',
                "message": "optional message"
                }
        response = self.client.post("/api/user/create/", data, **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(json.loads(response.content)['error'].keys()), set(['role']))

    # test add member fails with invalid role
    def test_add_member_fails_with_invalid_role(self):
        data = {"email": "WWCodeSV@gmail.com",
                "role": "MANAGER",
                "message": "optional message"
                }
        response = self.client.post("/api/user/create/", data, **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(json.loads(response.content)['error'].keys()), set(['role']))

    # test add member fails with invalid email
    def test_add_member_fails_with_invalid_email(self):
        data = {"email": "abc@235",
                "role": UserProfile.LEADER,
                "message": "optional message"
                }
        response = self.client.post("/api/user/create/", data, **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', json.loads(response.content)['error'])

    # test add member saves with valid data
    def test_add_member_saves_with_valid_data(self):
        data = {"email": "WWCodeSV@gmail.com",
                "role": UserProfile.DIRECTOR,
                "message": "optional message"
                }
        response = self.client.post("/api/user/create/", data, **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', json.loads(response.content))

    # test add member saves with blank message
    def test_add_member_saves_with_blank_message(self):
        data = {"email": "volunteersv@gmail.com",
                "role": UserProfile.VOLUNTEER,
                "message": ""
                }
        response = self.client.post("/api/user/create/", data, **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', json.loads(response.content))

    # test can add member permissions with role = VOLUNTEER
    def test_can_add_member_with_no_permission_for_volunteer(self):
        self.username = 'volunteer@example.com'
        self.password = 'Password123'
        data = {"email": "volunteersv@gmail.com",
                "role": UserProfile.LEADER,
                "message": ""
                }
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.post("/api/user/create/", data, **bearer)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail': self.EXPECTED_MESSAGE})

    # test can add member permission with role = LEADER
    def test_can_add_member_with_no_permission_for_leader(self):
        self.username = 'leader@example.com'
        self.password = 'Password123'
        data = {"email": "someonev@gmail.com",
                "role": UserProfile.VOLUNTEER,
                "message": "Hello"
                }
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.post("/api/user/create/", data, **bearer)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail': self.EXPECTED_MESSAGE})
