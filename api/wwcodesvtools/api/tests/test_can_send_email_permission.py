import json
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status


class CanSendEmailPermissionTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']
    EXPECTED_MESSAGE = 'You do not have permission to perform this action.'

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # Testing can send email permissions wit valid data -> role = DIRECTOR
    def test_can_send_email_with_permission(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        data = {"email": 'WWCodeSV@gmail.com'}
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.post("/api/send_email_example/", data, **bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing can send email permissions with invalid data -> role = VOLUNTEER
    def test_can_send_email_with_no_permission(self):
        self.username = 'volunteer@example.com'
        self.password = 'Password123'
        data = {"email": 'WWCodeSV@gmail.com'}
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.post("/api/send_email_example/", data, **bearer)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail': self.EXPECTED_MESSAGE})
