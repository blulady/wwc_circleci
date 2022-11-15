from django.core.exceptions import ValidationError


def validate_first_name(value):
    min = 1
    max = 50
    fn_len = len(value)
    if not value:
        raise ValidationError("First Name cannot be empty")
    if value.isspace():
        raise ValidationError("First Name it's only whitespaces, it should contain characters")
    if fn_len < min or fn_len > max:
        raise ValidationError("Length of First Name not in range of 1 to 50 characters")
    return value


def validate_last_name(value):
    min = 1
    max = 50
    ln_len = len(value)
    if not value:
        raise ValidationError("Last Name cannot be empty")
    if value.isspace():
        raise ValidationError("Last Name it's only whitespaces, it should contain characters")
    if ln_len < min or ln_len > max:
        raise ValidationError("Length of Last Name not in range of 1 to 50 characters")
    return value
