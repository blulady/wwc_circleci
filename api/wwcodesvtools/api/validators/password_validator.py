from django.core.exceptions import ValidationError
import re


def validate_password(value):
    """
    Check that the password is correct:
        8-50 characters.
        At least one upper case letter
        At least one lower case letter
        At least one numeric char
    """
    pw_min = 8
    pw_max = 50

    if not re.search(r'[A-Z]', value):
        raise ValidationError("Password should have at least one uppercase letter")
    if not re.search(r'[a-z]', value):
        raise ValidationError("Password should have at least one lowercase letter")
    if not re.search(r'\d', value):
        raise ValidationError("Password should have at least one number")
    if (pw_min > len(value) or len(value) > pw_max):
        raise ValidationError("Password should be a minimum of 8 and maximum of 50 characters long")
    return value
