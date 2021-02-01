import json
from unittest.mock import MagicMock
from django.core import mail
from django.test import TestCase, override_settings, TransactionTestCase
from rest_framework import exceptions as drf_exceptions
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .helper_functions import send_email_helper
from .models import UserProfile, User, RegistrationToken
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import UserSerializer, RegistrationTokenSerializer, UserProfileSerializer, AddMemberSerializer, CustomTokenObtainPairSerializer


class UserProfileTests(TestCase):

    def test_userprofile_is_pending(self):
        user_profile = UserProfile(user=None, status=UserProfile.PENDING)
        self.assertIs(user_profile.is_pending(), True)


class HelperFunctionsTest(TestCase):

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_send_email_helper(self):
        to_email = 'WWCodeSV@gmail.com'
        subject = 'Welcome to WWCode-SV'
        template_file = 'welcome_sample.html'
        context_data = {"user": "UserName",
                        "registration_link": "https://login.yahoo.com/account/create",
                        "social_media_link": "https://www.linkedin.com/company/women-who-code/"
                        }
        send_email_helper(to_email, subject, template_file, context_data)

        # Test that one message has been sent.
        self.assertEquals(len(mail.outbox), 1)

        # Verify that the "subject" of the first message is correct.
        self.assertEquals(mail.outbox[0].subject, 'Welcome to WWCode-SV')

        # Verify that the "to" of the first message is correct.
        self.assertEquals(mail.outbox[0].to, ['WWCodeSV@gmail.com'])


class TestAuthTokenObtainSerializer(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.password = 'test_password'

        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )

    def test_it_should_not_validate_if_any_fields_missing(self):
        s = TokenObtainSerializer(data={})
        self.assertFalse(s.is_valid())
        self.assertIn(s.username_field, s.errors)
        self.assertIn('password', s.errors)

        s = TokenObtainSerializer(data={
            TokenObtainSerializer.username_field: 'oieanrst',
        })
        self.assertFalse(s.is_valid())
        self.assertIn('password', s.errors)

        s = TokenObtainSerializer(data={
            'password': 'oieanrst',
        })
        self.assertFalse(s.is_valid())
        self.assertIn(s.username_field, s.errors)

    def test_it_should_not_validate_if_user_not_found(self):
        s = TokenObtainSerializer(context=MagicMock(), data={
            TokenObtainSerializer.username_field: 'missing',
            'password': 'pass',
        })

        with self.assertRaises(drf_exceptions.AuthenticationFailed):
            s.is_valid()

    def test_it_should_raise_if_user_not_active(self):
        self.user.is_active = False
        self.user.save()

        s = TokenObtainSerializer(context=MagicMock(), data={
            TokenObtainSerializer.username_field: self.username,
            'password': self.password,
        })

        with self.assertRaises(drf_exceptions.AuthenticationFailed):
            s.is_valid()


class TestAuthTokenObtainPairSerializer(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.password = 'test_password'

        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )

    def test_it_should_produce_a_json_web_token_when_valid(self):
        s = TokenObtainPairSerializer(context=MagicMock(), data={
            TokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })

        self.assertTrue(s.is_valid())
        self.assertIn('access', s.validated_data)
        self.assertIn('refresh', s.validated_data)

        # Expecting token type claim to be correct for both tokens.  If this is
        # the case, instantiating appropriate token subclass instances with
        # encoded tokens should not raise an exception.
        AccessToken(s.validated_data['access'])
        RefreshToken(s.validated_data['refresh'])


class TestAuthCustomTokenObtainPairSerializer(TestCase):
    def setUp(self):
        self.username = 'Mark_Doe@example.com'
        self.first_name = 'Mark'
        self.last_name = 'Doe'
        self.password = 'test_password1'
        self.email = 'Mark_Doe@example.com'

        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name
        )
        self.registration_token = RegistrationToken.objects.get(user_id=self.user.id)
        self.user_profile = UserProfile.objects.get(user_id=self.user.id)
        userProfile = UserProfileSerializer(instance=self.user_profile, data={
            "status": 'ACTIVE',
            "role": 'VOLUNTEER'
        })
        userProfile.is_valid()
        self.user_profile = userProfile.save()

    def test_it_should_produce_json_web_token_and_user_info_when_valid(self):
        s = CustomTokenObtainPairSerializer(context=MagicMock(), data={
            CustomTokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })

        self.assertTrue(s.is_valid())
        self.assertIn('access', s.validated_data)
        self.assertIn('refresh', s.validated_data)
        self.assertIn('id', s.validated_data)
        self.assertEquals(s.validated_data['email'], 'Mark_Doe@example.com')
        self.assertEquals(s.validated_data['first_name'], 'Mark')
        self.assertEquals(s.validated_data['last_name'], 'Doe')
        self.assertEqual(s.validated_data['role'], UserProfile.VOLUNTEER)
        AccessToken(s.validated_data['access'])
        RefreshToken(s.validated_data['refresh'])

    def test_it_should_raise_if_user_status_not_active(self):
        self.user_profile.status = 'PENDING'
        self.user_profile.save()

        s = CustomTokenObtainPairSerializer(context=MagicMock(), data={
            CustomTokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })

        with self.assertRaises(drf_exceptions.AuthenticationFailed):
            s.is_valid()


class TestUserSerializer(TestCase):

    def test_it_should_not_validate_if_username_missing(self):
        serializer = UserSerializer(data={
            'password': 'mypassword',
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['username']))

    def test_it_should_not_validate_if_password_missing(self):
        serializer = UserSerializer(data={
            'username': 'Jane@example.com',
        })

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['password']))

    def test_it_should_not_validate_if_user_email_is_invalid(self):
        serializer = UserSerializer(data={
            'email': 'Jan+e@Doe@Jane.com',
            'username': 'Jan+e@Doe@Jane.com',
            'password': 'password'
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['email']))

    def test_it_should_not_validate_if_email_and_username_not_same(self):
        serializer = UserSerializer(data={
            'email': 'JaneDoe@example.com',
            'username': 'JaneDoe',
            'password': 'password'
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['email_username']))

    def test_it_should_save_user_when_valid(self):
        serializer = UserSerializer(data={
            'email': 'JaneDoe@example.com',
            'username': 'JaneDoe@example.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'password': 'mypassword'
        })
        self.assertTrue(serializer.is_valid())
        self.assertEquals(serializer.errors, {})
        self.new_user = serializer.save()

        self.new_user.refresh_from_db()
        self.assertEquals(self.new_user.email, 'JaneDoe@example.com')
        self.assertEquals(self.new_user.username, 'JaneDoe@example.com')
        self.assertEquals(self.new_user.first_name, 'Jane')
        self.assertEquals(self.new_user.last_name, 'Doe')
        self.assertEqual(self.new_user.check_password('mypassword'), True)


class TestUserProfileSerializer(TestCase):

    def setUp(self):
        self.user_attributes = {
            "email": 'JohnDoe@example.com',
            "username": 'JohnDoe@example.com',
            "password": "passsword1"
        }
        self.new_user = User.objects.create_user(**self.user_attributes)
        self.user_profile = UserProfile.objects.get(user_id=self.new_user.id)

    def test_it_should_not_validate_if_status_is_blank(self):
        serializer = UserProfileSerializer(instance=self.user_profile, data={
            "status": '',
            "role": 'VOLUNTEER'
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['status']))

    def test_it_should_not_validate_if_role_is_blank(self):
        serializer = UserProfileSerializer(instance=self.user_profile, data={
            "status": 'PENDING',
            "role": ''
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['role']))

    def test_it_should_not_validate_if_status_invalid(self):
        serializer = UserProfileSerializer(instance=self.user_profile, data={
            "status": 'OBSOLETE',
            "role": UserProfile.LEADER
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['status']))

    def test_it_should_not_validate_if_role_invalid(self):
        serializer = UserProfileSerializer(instance=self.user_profile, data={
            "status": UserProfile.INACTIVE,
            "role": "MANAGER"
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['role']))

    def test_it_should_save_userprofile_when_valid(self):
        serializer = UserProfileSerializer(instance=self.user_profile, data={
            "status": UserProfile.PENDING,
            "role": UserProfile.VOLUNTEER
        })
        self.assertTrue(serializer.is_valid())
        self.assertEquals(serializer.errors, {})
        serializer.save()

        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.status, UserProfile.PENDING)
        self.assertEqual(self.user_profile.role, UserProfile.VOLUNTEER)


class TestRegistrationTokenSerializer(TestCase):
    def setUp(self):
        self.user_attributes = {
            "email": 'Martha@example.com',
            "username": 'Martha@example.com',
            "password": "passsword2"
        }
        self.new_user = User.objects.create_user(**self.user_attributes)
        self.registration_token = RegistrationToken.objects.get(user_id=self.new_user.id)

    def test_it_should_not_validate_if_token_is_blank(self):
        serializer = RegistrationTokenSerializer(instance=self.registration_token, data={
            "token": '',
            "used": False
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['token']))

    def test_it_should_not_validate_if_used_is_blank(self):
        serializer = RegistrationTokenSerializer(instance=self.registration_token, data={
            "token": "#%6token%#",
            "used": ''
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['used']))

    def test_it_should_not_validate_if_used_invalid(self):
        serializer = RegistrationTokenSerializer(instance=self.registration_token, data={
            "token": "#%6token%",
            "used": "Yesss"
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['used']))

    def test_it_should_not_validate_if_token_invalid(self):
        serializer = RegistrationTokenSerializer(instance=self.registration_token, data={
            "token": True,
            "used":  False
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['token']))

    def test_it_should_save_registration_token_when_valid(self):
        serializer = RegistrationTokenSerializer(instance=self.registration_token, data={
            "token": "#$%deftoken#",
            "used": False
        })
        self.assertTrue(serializer.is_valid())
        self.assertEquals(serializer.errors, {})
        serializer.save()

        self.registration_token.refresh_from_db()
        self.assertEqual(self.registration_token.token, "#$%deftoken#")
        self.assertEqual(self.registration_token.used, False)


class TestAddMemberSerializer(TestCase):

    def test_it_should_not_validate_if_email_is_blank(self):
        serializer = AddMemberSerializer(data={
            "email": '',
            "role": 'LEADER',
            "message": 'test message'
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['email']))

    def test_it_should_not_validate_if_role_is_blank(self):
        serializer = AddMemberSerializer(data={
            "email": 'jane@jane.com',
            "role": '',
            "message": 'test message'
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['role']))

    def test_it_should_not_validate_if_email_is_invalid(self):
        serializer = AddMemberSerializer(data={
            "email": "newUser'semail@$@example.com",
            "role": UserProfile.DIRECTOR,
            "message": ""
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['email']))

    def test_it_should_not_validate_if_role_invalid(self):
        serializer = AddMemberSerializer(data={
            'email': 'newUser@example.com',
            "role": 'PRESIDENT',
            "message": "test message"
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['role']))

    def test_it_should_validate_if_message_is_blank(self):
        serializer = AddMemberSerializer(data={
            "email": 'newMember@example.com',
            "role": UserProfile.LEADER,
            "message": ""
        })
        self.assertTrue(serializer.is_valid())
        self.assertEquals(serializer.errors, {})

    def test_it_should_validate_when_valid_data(self):
        serializer = AddMemberSerializer(data={
            "email": 'newUser@example.com',
            "role": UserProfile.VOLUNTEER,
            "message": "optional message"
        })
        self.assertTrue(serializer.is_valid())
        self.assertEquals(serializer.errors, {})


class AddMemberViewTestCase(APITestCase):
    NO_ERRORS = 'No Errors'

    # test add member fails with blank email
    def test_add_member_fails_with_blank_email(self):
        data = {"email": '',
                "role": 'VOLUNTEER',
                "message": "optional message"
                }
        response = self.client.post("/api/add_member/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(json.loads(response.content)['error'].keys()), set(['email']))

    # test add member fails with blank role
    def test_add_member_fails_with_blank_role(self):
        data = {"email": "WWCodeSV@gmail.com",
                "role": '',
                "message": "optional message"
                }
        response = self.client.post("/api/add_member/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(json.loads(response.content)['error'].keys()), set(['role']))

    # test add member fails with invalid role
    def test_add_member_fails_with_invalid_role(self):
        data = {"email": "WWCodeSV@gmail.com",
                "role": "MANAGER",
                "message": "optional message"
                }
        response = self.client.post("/api/add_member/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(json.loads(response.content)['error'].keys()), set(['role']))

    # test add member fails with invalid email
    def test_add_member_fails_with_invalid_email(self):
        data = {"email": "abc@235",
                "role": UserProfile.LEADER,
                "message": "optional message"
                }
        response = self.client.post("/api/add_member/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', json.loads(response.content)['error'])

    # test add member saves with valid data
    def test_add_member_saves_with_valid_data(self):
        data = {"email": "WWCodeSV@gmail.com",
                "role": UserProfile.DIRECTOR,
                "message": "optional message"
                }
        response = self.client.post("/api/add_member/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'error': self.NO_ERRORS})

    # test add member saves with blank message
    def test_add_member_saves_with_blank_message(self):
        data = {"email": "volunteersv@gmail.com",
                "role": UserProfile.VOLUNTEER,
                "message": ""
                }
        response = self.client.post("/api/add_member/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'error': self.NO_ERRORS})


class TestCanSendEmailPermission(TransactionTestCase):
    reset_sequences = True
    fixtures = ['permissions_data.json']
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
        self.username = 'UserDirector@example.com'
        self.password = 'Password1@'
        data = {"email": 'WWCodeSV@gmail.com'}
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.post("/api/send_email_example/", data, **bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing can send email permissions with invalid data -> role = VOLUNTEER
    def test_can_send_email_with_no_permission(self):
        self.username = 'UserVolunteer@example.com'
        self.password = 'Password1@'
        data = {"email": 'WWCodeSV@gmail.com'}
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.post("/api/send_email_example/", data, **bearer)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail': self.EXPECTED_MESSAGE})


class TestGetMembersView(TransactionTestCase):
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
        self.username = 'UserDirector@example.com'
        self.password = 'Password1@'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/get_members/", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 4)
        self.assertEqual(json.loads(response.content)[0]['id'], 4)
        self.assertEqual(json.loads(response.content)[0]['email'], 'UserLeaderPending@example.com')
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'new')
        self.assertEqual(json.loads(response.content)[0]['last_name'], 'user')
        self.assertEqual(json.loads(response.content)[0]['userprofile']['status'], 'PENDING')
        self.assertEqual(json.loads(response.content)[0]['userprofile']['role'], 'LEADER')
        self.assertEqual(json.loads(response.content)[0]['date_joined'], '2020-12-14T20:26:55.902000Z')
        for i in range(responseLength):
            self.assertIsNotNone(json.loads(response.content)[i]['email'])

    # Testing get members with role = VOLUNTEER
    # 'PENDING' status members and 'email' field not in the response
    def test_get_members_role_volunteer(self):
        self.username = 'UserVolunteer@example.com'
        self.password = 'Password1@'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/get_members/", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 3)
        self.assertEqual(json.loads(response.content)[0]['id'], 3)
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'User FirstName')
        self.assertEqual(json.loads(response.content)[0]['last_name'], 'User LastName')
        self.assertEqual(json.loads(response.content)[0]['userprofile']['role'], 'LEADER')
        self.assertEqual(json.loads(response.content)[0]['date_joined'], '2020-12-14T20:13:39.660000Z')
        self.assertEqual(json.loads(response.content)[0]['userprofile']['status'], 'ACTIVE')
        for i in range(responseLength):
            self.assertRaises(KeyError, lambda: json.loads(response.content)[i]['email'])
            self.assertNotEqual(json.loads(response.content)[i]['userprofile']['status'], 'PENDING')

    # Testing get members with role = LEADER
    # 'PENDING' status members and 'email' field not in the response
    def test_get_members_role_leader(self):
        self.username = 'UserLeader@example.com'
        self.password = 'Password1@'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/get_members/", **bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 3)
        self.assertEqual(json.loads(response.content)[0]['id'], 3)
        self.assertEqual(json.loads(response.content)[0]['first_name'], 'User FirstName')
        self.assertEqual(json.loads(response.content)[0]['last_name'], 'User LastName')
        self.assertEqual(json.loads(response.content)[0]['userprofile']['role'], 'LEADER')
        self.assertEqual(json.loads(response.content)[0]['date_joined'], '2020-12-14T20:13:39.660000Z')
        self.assertEqual(json.loads(response.content)[0]['userprofile']['status'], 'ACTIVE')
        for i in range(responseLength):
            self.assertRaises(KeyError, lambda: json.loads(response.content)[i]['email'])
            self.assertNotEqual(json.loads(response.content)[i]['userprofile']['status'], 'PENDING')


class TestGetMemberInfoView(TransactionTestCase):
    reset_sequences = True
    fixtures = ['get_members_data.json']

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # Testing get member info with role = DIRECTOR
    def test_get_member_info_for_director(self):
        self.username = 'UserDirector@example.com'
        self.password = 'Password1@'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/get_member_info/1", **bearer)
        self.assertEqual(json.loads(response.content)['id'], 1)
        self.assertEqual(json.loads(response.content)['email'], 'UserDirector@example.com')
        self.assertEqual(json.loads(response.content)['first_name'], 'User FirstName')
        self.assertEqual(json.loads(response.content)['last_name'], 'User LastName')
        self.assertEqual(json.loads(response.content)['userprofile']['status'], 'ACTIVE')
        self.assertEqual(json.loads(response.content)['userprofile']['role'], 'DIRECTOR')
        self.assertEqual(json.loads(response.content)['date_joined'], '2020-12-14T20:13:19.823000Z')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing get member info with role = LEADER
    def test_get_member_info_for_leader(self):
        self.username = 'UserLeader@example.com'
        self.password = 'Password1@'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/get_member_info/1", **bearer)
        self.assertIn('You do not have permission to perform this action.', json.loads(response.content)['detail'])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Testing get member info with role = VOLUNTEER
    def test_get_member_info_for_volunteer(self):
        self.username = 'UserVolunteer@example.com'
        self.password = 'Password1@'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/get_member_info/2", **bearer)
        self.assertIn('You do not have permission to perform this action.', json.loads(response.content)['detail'])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
