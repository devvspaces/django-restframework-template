from io import BytesIO

import pytest
from rest_framework.serializers import ValidationError

from utils.base.validators import (ErrorCodes, regex_phone,
                                   validate_image_size, validate_phone,
                                   validate_positive_number,
                                   validate_special_char)


def test_validate_image_size():
    image = BytesIO(b'1234567890')
    image.size = 1024 * 1024 * 2
    with pytest.raises(ValidationError) as excinfo:
        validate_image_size(image)

    assert excinfo.value.get_codes()[0] == ErrorCodes.image_too_big

    image.size = 1024 * 1024
    validate_image_size(image)


def test_validate_positive_number():
    value = -1
    with pytest.raises(ValidationError) as excinfo:
        validate_positive_number(value)

    assert excinfo.value.get_codes()[0] == ErrorCodes.negative_number

    value = 1
    validate_positive_number(value)


def test_validate_special_char():
    value = 'abc'
    validate_special_char(value)

    value = 'abc123'
    validate_special_char(value)

    value = 'abc123@'
    with pytest.raises(ValidationError) as excinfo:
        validate_special_char(value)

    assert excinfo.value.get_codes()[0] == ErrorCodes.invalid_characters


def test_regex_phone():
    value = '+1234567890'
    regex_phone(value)


@pytest.mark.parametrize(
    'value',
    [
        "1234567890a", "123456789r", "123456d78901",
        "12345678901", "12345678923", "12345", "123456789"
    ]
)
def test_regex_phone_error(value):
    from django.core.exceptions import ValidationError
    with pytest.raises(ValidationError) as excinfo:
        regex_phone(value)

    assert excinfo.value.code == "invalid"


def test_validate_phone():
    value = '+1234567890'
    validate_phone(value)


@pytest.mark.parametrize(
    'value',
    [
        "+1234567890a", "+123456789r", "+123456d78901",
        "+1234567890145635", "+12345"
    ]
)
def test_validate_phone_error(value):
    with pytest.raises(ValidationError) as excinfo:
        validate_phone(value)

    assert excinfo.value.get_codes()[0] == ErrorCodes.invalid_phone
