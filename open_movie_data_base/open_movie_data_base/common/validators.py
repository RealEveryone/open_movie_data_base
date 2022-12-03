from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class InRangeValidator:

    def __init__(self, value1, value2, err_msg):
        self.min_value1 = value1
        self.max_value2 = value2
        self.err_msg = err_msg

    def __call__(self, value):
        if self.min_value1 > value or value > self.max_value2:
            raise ValidationError(self.err_msg)

    def __eq__(self, other):
        return (
                isinstance(other, InRangeValidator)
                and self.max_value2 == other.max_value
                and self.min_value1 == other.min_value1
                and (self.err_msg == other.err_msg)
        )
