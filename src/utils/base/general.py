from functools import reduce
import hmac
import os
import secrets
import string
import sys
from contextlib import contextmanager
from io import StringIO
from typing import Callable, Generator, List

from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.template.defaultfilters import slugify
from django.utils.crypto import RANDOM_STRING_CHARS, get_random_string
from django.utils.encoding import force_bytes
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.openapi import Schema
from rest_framework.serializers import Serializer

from .logger import err_logger, logger  # noqa


def get_model_fields(model):
    """Get model fields"""
    return [field.name for field in model._meta.fields]


def custom_auto_schema(error_codes: List[str] = None, *args, **kwargs):
    """
    Added error codes functionality to swagger_auto_schema
    Allows user to specify error status codes in a list
    and automatically added it to the responses dictionary to
    be passed to swagger_auto_schema.

    :param error_codes: list of error codes, defaults to None
    :type error_codes: List[str], optional
    :return: swagger_auto_schema response
    :rtype: swagger_auto_schema
    """
    if error_codes is None:
        error_codes = ['400']
    default_responses: dict = kwargs.get('responses', {})
    for code in error_codes:
        if default_responses.get(code) is None:
            default_responses[code] = Schema(
                type='object'
            )
    kwargs['responses'] = default_responses

    return swagger_auto_schema(*args, **kwargs)


def sha256_hash(value, key=None) -> str:
    """Returns hexdigest of value using key if passed
    else uses settings.SECRET_KEY as default"""
    if key is None:
        key = settings.SECRET_KEY
    key = force_bytes(key)
    value = force_bytes(value)
    hash_obj = hmac.new(key, value, 'SHA256')
    return hash_obj.hexdigest()


def compare_hash(a, b) -> bool:
    """Compares passed hashes"""
    return hmac.compare_digest(a, b)


def add_queryset(a, b) -> QuerySet:
    """
    Add two querysets
    """
    return a | b


def merge_querysets(*args) -> QuerySet:
    """
    Merge querysets
    """
    return reduce(add_queryset, args)


class Singleton(type):
    """
    Singleton metaclass.
    Source:
    http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(
                *args, **kwargs
            )
        return cls._instances[cls]


def convert_list_to_choices(array=None) -> list:
    """
    Convert list to choices
    """
    if not array:
        array = []

    choices = []

    for i in array:
        tup = (slugify(i), i,)
        choices.append(tup)

    return choices


def get_tokens_for_user(user) -> dict:
    """
    Get jwt tokens for user

    :param user: Authenticated user
    :type user: authentication.models.User
    :return: JWT tokens dictionary
    :rtype: dict
    """

    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def url_with_params(url: str, params: dict) -> str:
    """
    Append to url parameters params dictionary

    :param url: Url is a relative or full link
    :type url: str
    :param params: Dictionary of key/value pairs of the query parameters
    {id: 3, name: 'John doe'}
    :type params: dict
    :return: URL with parameters from params attached
    :rtype: str
    """

    # Add trailing backslash to url
    if not url.endswith('/'):
        url += '/'

    # Join the key/value pairs into a string
    assiged = [f'{key}={value}' for key, value in params.items()]
    return url + '?' + '&'.join(assiged)


def choices_to_dict(dicts=None):
    """
    This is for choices of model, helps pass
    it to context as a list of dicts
    """
    if dicts is None:
        dicts = {}

    return [{'value': a[0], 'name': a[1]} for a in dicts]


def printt(*args, **kwargs):
    """
    Override python print to only print when allowed
    """
    if settings.PRINT_LOG is True:
        return print(*args, **kwargs)


def send_email(email, subject, message, fail=True):
    """
    Send mail function
    """
    if settings.DEBUG is True:
        print(message)

    if settings.OFF_EMAIL:
        return True

    val = send_mail(
        subject=subject, message=message,
        html_message=message, rom_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email], fail_silently=fail)

    return True if val else False


def upload_to_image(instance, filename: str, *args, **kwargs) -> str:
    """
    Function for dynamic upload directory for images

    :param instance: Model instance
    :param filename: File name
    :type filename: str
    :return: Joined path for uploading image/file
    :rtype: str
    """

    # file will be uploaded to MEDIA_ROOT/<base_dir>/<slugified_instance_label>
    path = os.path.join(
        instance.default_upload_to,
        instance.label,
        filename
    )
    return path


def upload_to_product(instance, filename, *args, **kwargs):
    """
    Function for dynamic upload directory for product images

    :param instance: Model instance
    :param filename: File name
    :type filename: str
    :return: Joined path for uploading image/file
    :rtype: str
    """

    path = os.path.join(
        instance.default_upload_to,
        instance.product.label,
        filename
    )
    return path


class Crypthex:
    """
    Class for encryption and decryption
    """

    def __init__(self, key: str = settings.ENCRYPTING_KEY):
        self._fernet = Fernet(key.encode())

    def encrypt(self, text) -> str:
        """
        Use the fernet created in the __init__ to encrypt text,
        which will return an encoded string example
        of result = b'example'
        """
        text = str(text)

        result = self._fernet.encrypt(text.encode())
        return result.decode()

    def decrypt(self, text) -> str:
        """
        Use the fernet created in the __init__ to decrypt text,
        which will return an encoded string
        example of result = b'example'
        """
        text = str(text)
        try:
            result = self._fernet.decrypt(text.encode())
            return result.decode()
        except InvalidToken:
            pass

        return False


def random_otp(length: int = 6) -> str:
    """
    Generating OTP with 6 or length digits

    :return: random numbers of length provided
    :rtype: str
    """
    return get_random_string(length=length, allowed_chars='1234567890')


def random_text(length=5, upper=True, lower=True, digits=True) -> str:
    rtext = ''

    if upper:
        rtext += string.ascii_uppercase

    if lower:
        rtext += string.ascii_lowercase

    if digits:
        rtext += string.digits

    return get_random_string(length, rtext)


def invalid_str(value):
    # This checks if a string contains special chars or not
    for i in '@#$%^&*+=://;?><}{[]()':
        if i in value:
            return True
    return False


def username_gen(n: int) -> str:
    """
    This will generate a text in this format 'user<n random digits>'

    :param n: number of random characters
    :type n: int
    :return: user + random characters
    :rtype: str
    """
    return settings.USERNAME_PREFIX + get_random_string(n)


def get_randint_range(start, stop) -> int:
    """Gets a random number between start and stop
    securely with start and stop inclusive"""
    return secrets.choice(range(start, stop + 1))


def get_random_secret() -> str:
    """
    Return a random secret chars of random length

    :return: secret chars
    :rtype: str
    """
    length = get_randint_range(
        settings.WEBHOOK_SECRET_LENGTH_START,
        settings.WEBHOOK_SECRET_LENGTH_STOP
    )
    allowed_chars = RANDOM_STRING_CHARS + '.-_!$;*#@'
    return get_random_string(length, allowed_chars)


def get_usable_name(profile, name: str = None) -> str:
    """
    Get a unique username for newly created users

    :param profile: Profile model
    :type profile: authentication.models.Profile
    :param name: last generated username, defaults to None
    :type name: str, optional
    :return: unique username
    :rtype: str
    """
    if not name:
        name = username_gen(5)

    # Check if the name exists in the Profile table
    exists = profile.objects.filter(username=name).exists()
    if exists:
        return get_usable_name(profile, username_gen(5))
    return name


@contextmanager
def capture_output(func: Callable[..., None]) -> Generator[str, None, None]:
    """Context manager to capture
    standart output when calling function as
    a string"""
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    func()
    sys.stdout = old_stdout

    yield mystdout.getvalue()


def check_serialized_data(serializer: Serializer, data: dict):
    s_fields = serializer().get_fields()
    for key in s_fields:
        assert data.get(key)


def regexify(name: str) -> str:
    """Wraps name with regex to use in restframework action url path"""
    return f"(?P<{name}>[^/.]+)"
