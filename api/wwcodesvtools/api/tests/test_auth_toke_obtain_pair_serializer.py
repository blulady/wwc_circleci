from unittest.mock import MagicMock
from django.test import TestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from ..models import User


class AuthTokenObtainPairSerializerTestCase(TestCase):
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
