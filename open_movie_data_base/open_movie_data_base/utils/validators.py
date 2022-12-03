import re
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class CharValidator:

    def __init__(self, pattern, message):
        self.pattern = pattern
        self.message = message

    def __call__(self, value):
        valid_input = re.match(self.pattern, str(value))
        if not valid_input:
            raise ValidationError(self.message)

    def __eq__(self, other):
        return (
                isinstance(other, CharValidator)
                and self.pattern == other.pattern
                and (self.message == other.message)
        )

