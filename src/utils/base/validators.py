from io import BytesIO

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError
from .general import invalid_str


class ErrorCodes:
    image_too_big = 'max_image_size_limit_reached'
    link_insecure = 'url_insecure'
    invalid_image_ext = 'invalid_image_extension'
    negative_number = 'negative_number'
    invalid_characters = 'invalid_string_characters'
    invalid_phone = 'invalid_phone'
    exchange_min = 'max_exchange_amount_reached'


def validate_image_size(image):
    """Validate the image size"""
    if isinstance(image, BytesIO):
        file_size = image.size
    else:
        file_size = image.file.size

    limit_mb = 1
    if file_size > (limit_mb * 1024 * 1024):
        raise ValidationError(
            detail=f"Max size of file is {limit_mb} MB",
            code=ErrorCodes.image_too_big
        )


def validate_positive_number(value):
    """Validate the value is a positive integer or float or decimal"""
    if value < 0:
        raise ValidationError(
            detail=f"Negative numbers, {value}, is not allowed",
            code=ErrorCodes.negative_number
        )


def validate_special_char(value):
    """Validate string does not contain defined special characters"""
    if invalid_str(value):
        raise ValidationError(
            detail=_(f'{value} contains special characters'),
            code=ErrorCodes.invalid_characters
        )


regex_phone = RegexValidator(
    regex=r'^\+(?:[0-9] ?){6,14}[0-9]$',
    message='Your phone number is not in the right format')


def validate_phone(phone: str):
    """Validate the phone number is valid"""
    phone = str(phone).replace(' ', '')
    try:
        regex_phone(phone)
    except Exception:
        raise ValidationError(
            detail='Invalid phone number provided',
            code='invalid_phone'
        )
