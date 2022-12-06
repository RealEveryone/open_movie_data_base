from django.core.exceptions import ValidationError


def validate_file_size(img_size):
    if img_size.size > 5242880:
        raise ValidationError('The maximum file size is 5MB')
