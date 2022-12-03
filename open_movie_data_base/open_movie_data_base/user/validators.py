from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r"^[\w.-]+\Z"
    message = (
        "Username may contain only latin letters, numbers, and dashes between characters.")
