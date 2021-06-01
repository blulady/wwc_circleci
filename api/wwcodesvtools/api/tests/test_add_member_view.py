
import json
from django.test import TransactionTestCase, override_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import Role
from rest_framework import status
from django.conf import settings
from django.core import mail
from django.utils.http import urlencode
from django.utils.html import escape
from ..helper_functions import send_email_helper


class AddMemberViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']
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
                "role": Role.VOLUNTEER,
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
                "role": Role.LEADER,
                "message": "optional message"
                }
        response = self.client.post("/api/user/create/", data, **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', json.loads(response.content)['error'])

    # test add member saves with valid data
    def test_add_member_saves_with_valid_data(self):
        data = {"email": "WWCodeSV@gmail.com",
                "role": Role.DIRECTOR,
                "message": "optional message"
                }
        response = self.client.post("/api/user/create/", data, **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', json.loads(response.content))

    # test add member saves with blank message
    def test_add_member_saves_with_blank_message(self):
        data = {"email": "volunteersv@gmail.com",
                "role": Role.LEADER,
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
                "role": Role.LEADER,
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
                "role": Role.VOLUNTEER,
                "message": "Hello"
                }
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.post("/api/user/create/", data, **bearer)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail': self.EXPECTED_MESSAGE})

    # Test the registration link in the registration notification email message
    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_registration_notification_email_link(self):
        email = "Ja-ne++Do-e@example.com"
        token = "7b4152bbf09444cdbe97ce574b88634c20210219015501"
        optional_message = "Testing registration link"
        registration_link = f'{settings.FRONTEND_APP_URL}/register?{urlencode({"email": email, "token": token})}'
        context_data = {"user": email,
                        "registration_link": registration_link,
                        "optional_message": optional_message
                        }
        send_email_helper(
            email, 'Invitation to Join Chapter Portal, Action Required', 'new_member_email.html', context_data)

        expected_encoded_email_param = "email=Ja-ne%2B%2BDo-e%40example.com"
        expected_encoded_token_param = "token=7b4152bbf09444cdbe97ce574b88634c20210219015501"
        expected_host_api_endpoint = "https://wwcode-chtools-fe.herokuapp.com/register?"

        # Verify that one email message has been sent.
        self.assertEquals(len(mail.outbox), 1)
        # Verify that the "subject" of the first message is correct.
        self.assertEquals(mail.outbox[0].subject, 'Invitation to Join Chapter Portal, Action Required')
        # Verify that the "to" of the first message is correct.
        self.assertEquals(mail.outbox[0].to, ['Ja-ne++Do-e@example.com'])
        # Verify the user registration url in the email html message body
        self.assertIn(escape(registration_link), mail.outbox[0].body)
        # verify the encoded email param
        self.assertIn(expected_encoded_email_param, mail.outbox[0].body)
        # verify the encoded token param
        self.assertIn(expected_encoded_token_param, mail.outbox[0].body)
        # verify the host api_endpoint
        self.assertIn(expected_host_api_endpoint, mail.outbox[0].body)
        # verify the optional message
        self.assertIn(optional_message, mail.outbox[0].body)
