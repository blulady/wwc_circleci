
from api.validators.password_validator import validate_password
from django.core.exceptions import ValidationError
from django.test import TestCase


class PasswordValidatorTestCase(TestCase):

    def test_missing_uppercase_validate_password_fails(self):
        passwd = "womenwhocode1"
        with self.assertRaises(ValidationError) as error:
            validate_password(passwd)
        self.assertEqual(error.exception.message, 'Password should have at least one uppercase letter')

    def test_missing_lowercase_validate_password_fails(self):
        passwd = "WOMENWHOCODE1"
        with self.assertRaises(ValidationError) as error:
            validate_password(passwd)
        self.assertEqual(error.exception.message, 'Password should have at least one lowercase letter')

    def test_missing_numeric_validate_password_fails(self):
        passwd = "WomeWhoCode"
        with self.assertRaises(ValidationError) as error:
            validate_password(passwd)
        self.assertEqual(error.exception.message, 'Password should have at least one number')

    def test_password_too_long_validate_password_fails(self):
        passwd = "WomeWhoCodeA1bcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
        with self.assertRaises(ValidationError) as error:
            validate_password(passwd)
        self.assertEqual(error.exception.message, 'Password should be a minimum of 8 and maximum of 50 characters long')

    def test_password_too_short_validate_password_fails(self):
        passwd = "WWCode1"
        with self.assertRaises(ValidationError) as error:
            validate_password(passwd)
        self.assertEqual(error.exception.message, 'Password should be a minimum of 8 and maximum of 50 characters long')

    def test_validate_password_success(self):
        passwd = "WomenWhoCode123"
        result = validate_password(passwd)
        self.assertEqual(result, passwd)
