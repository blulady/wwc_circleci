from django.test import TestCase
from api.validators.FirstAndLastNameValidator import validate_first_name, validate_last_name
from django.core.exceptions import ValidationError


class TestNameValidator(TestCase):

    def test_validation_fails_for_empty_first_name(self):
        test_first_name = ""
        with self.assertRaises(ValidationError):
            validate_first_name(test_first_name)

    def test_validation_fails_for_first_name_too_long(self):
        test_first_name = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
        with self.assertRaises(ValidationError):
            validate_first_name(test_first_name)

    def test_validation_fails_for_whitespaces_first_name(self):
        test_first_name = "  "
        with self.assertRaises(ValidationError):
            validate_first_name(test_first_name)

    def test_validation_fails_for_empty_last_name(self):
        test_last_name = ""
        with self.assertRaises(ValidationError):
            validate_last_name(test_last_name)

    def test_validation_fails_for_last_name_too_long(self):
        test_last_name = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
        with self.assertRaises(ValidationError):
            validate_last_name(test_last_name)

    def test_validation_fails_for_whitespaces_last_name(self):
        test_last_name = "  "
        with self.assertRaises(ValidationError):
            validate_last_name(test_last_name)
