import re

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r"^[\w.-]+\Z"
    message = (
        "Username may contain only latin letters, numbers, and dashes between characters.")


def names_validator(value):
    pattern = '^[A-Za-zа-яА-Я-]*$'
    if not re.match(pattern, value):
        raise ValidationError('Can contain only letters and dashes')
