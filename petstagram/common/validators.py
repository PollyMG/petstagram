from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


def only_letters_validator(value):
    for ch in value:
        if not ch.isalpha():
            # Invalid case
            raise ValidationError('Value must contain only letters!')
        # Valid case

    # if not all(ch.isalpha() for ch in value):
    #     raise ValidationError('Value must contain only letters!')


def validate_file_max_size_in_mb(max_size):
    def validate(value):
        file_size = value.file.size
        if file_size > max_size * 1024 * 1024:
            raise ValidationError('The maximum size of the photo can be 5MB')
        return validate


@deconstructible
class MinDateValidator:
    def __init__(self, min_date):
        self.min_date = min_date

    def __call__(self, value):
        if value < self.min_date:
            raise ValidationError(f'Date must be greater than {self.min_date}')


@deconstructible
class MaxDateValidator:
    def __init__(self, max_date):
        self.max_date = max_date

    def __call__(self, value):
        if self.max_date < value:
            raise ValidationError(f'Date must be earlier than {self.max_date}')
