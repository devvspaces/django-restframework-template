import re
from functools import partial

import pytest
from cryptography.fernet import Fernet
from django.db import models
from django.test import TestCase
from rest_framework import serializers

from authentication.models import Profile
from tests.models import ModelText
from utils.base.general import (Crypthex, add_queryset, capture_output,
                                check_serialized_data, choices_to_dict,
                                compare_hash, convert_list_to_choices,
                                generate_unique_link_id, get_randint_range,
                                get_random_secret, get_tokens_for_user,
                                get_usable_name, invalid_str, merge_querysets,
                                printt, random_otp, random_text, send_email,
                                username_gen)


class GetUniqueNameModel(models.Model):
    username = models.CharField(max_length=255, unique=True)


@pytest.mark.django_db
def test_get_usable_name(settings):
    obj = GetUniqueNameModel()

    username = get_usable_name(Profile)
    assert username is not None
    assert username.startswith(settings.USERNAME_PREFIX)
    obj.username = username
    obj.save()

    username = get_usable_name(Profile)
    assert username != obj.username


def test_get_random_secret(settings):
    computed = get_random_secret()
    assert settings.WEBHOOK_SECRET_LENGTH_START <= \
        len(computed) <= settings.WEBHOOK_SECRET_LENGTH_STOP


@pytest.mark.parametrize(
    "value", ["a", "c", "b", "d"]
)
def test_crypt(value):
    fernet_key = Fernet.generate_key().decode()
    crypt = Crypthex(fernet_key)
    enc = crypt.encrypt(value)
    assert enc is not None
    dec = crypt.decrypt(enc)
    assert dec is not None
    assert dec == value


@pytest.mark.parametrize(
    "start, stop",
    [
        (1, 7), (14, 25), (-1, 40), (100, 1000)
    ]
)
def test_get_randint_range(start, stop):
    computed = get_randint_range(start, stop)
    assert start <= computed <= stop


def test_username_gen(settings):
    computed = username_gen(4)
    assert computed is not None
    assert computed.startswith(settings.USERNAME_PREFIX)


def test_random_otp():
    otp = random_otp()
    assert len(otp) == 6
    assert otp.isdigit()


def test_random_text():
    text: str = random_text()
    assert len(text) == 5

    text = random_text(length=6)
    assert len(text) == 6

    text = random_text(length=6, lower=False)
    pattern = re.compile(r"[a-z]")
    assert pattern.match(text) is None

    text = random_text(length=6, digits=False)
    pattern = re.compile(r"[0-9]")
    assert pattern.search(text) is None

    text = random_text(length=6, upper=False)
    pattern = re.compile(r"[A-Z]")
    assert pattern.search(text) is None


@pytest.mark.parametrize(
    "v1, v2, expected",
    [
        ("test", "test", True),
        ("test", "test1", False),
        ("test", "test ", False),
    ]
)
def test_compare_hash(v1, v2, expected):
    assert compare_hash(v1, v2) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        [
            ("test", "test1"),
            [
                ("test", "test"),
                ("test1", "test1"),
            ]
        ],
        [
            ("test", "test-1", "test 2"),
            [
                ("test", "test"),
                ("test-1", "test-1"),
                ("test-2", "test 2"),
            ]
        ],
    ]
)
def test_convert_list_to_choices(value, expected):
    assert convert_list_to_choices(value) == expected


class TestGeneral(TestCase):
    def setUp(self) -> None:
        for i in range(3):
            ModelText.objects.create(name=i)

    def test_count(self):
        count = ModelText.objects.count()
        self.assertEqual(count, 3)

    def test_add_queryset(self):
        q1 = ModelText.objects.filter(name='1')
        q2 = ModelText.objects.filter(name='2')
        q3 = add_queryset(q1, q2)
        self.assertEqual(q3.count(), 2)
        self.assertTrue(q3.filter(name='1').exists())
        self.assertTrue(q3.filter(name='2').exists())

    def test_merge_querysets(self):
        q1 = ModelText.objects.filter(name='0')
        q2 = ModelText.objects.filter(name='1')
        q3 = ModelText.objects.filter(name='2')
        q4 = merge_querysets(q1, q2, q3)
        self.assertEqual(q4.count(), 3)
        self.assertTrue(q4.filter(name='1').exists())
        self.assertTrue(q4.filter(name='2').exists())
        self.assertTrue(q4.filter(name='0').exists())


def test_capture_output():
    func = (lambda: print("test"))
    with capture_output(func) as output:
        assert output.strip("\n") == "test"


def test_capture_output_complex():
    def func(value):
        print(value)
    partial_func = partial(func, "test")
    with capture_output(partial_func) as output:
        assert output.strip("\n") == "test"


class GenerateUniqueLinkIdModel(models.Model):
    link_id = models.CharField(max_length=255, unique=True)


@pytest.mark.django_db
def test_generate_unique_link_id(settings):
    obj = GenerateUniqueLinkIdModel()

    link_id = generate_unique_link_id(obj)
    assert link_id is not None
    obj.link_id = link_id
    obj.save()

    link_id = generate_unique_link_id(obj)
    assert link_id != obj.link_id
    assert link_id.startswith(settings.LINK_ID_PREFIX)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("test", False),
        ("test@", True),
        ("#test", True),
        ("test$", True),
        ("te%st", True),
        ("test^", True),
        ("t&est", True),
        ("test*", True),
        ("tes+t", True),
    ]
)
def test_invalid_str(value, expected: bool):
    assert invalid_str(value) is expected


def test_choices_to_dict():
    choices = (
        ('1', 'one'),
        ('2', 'two'),
        ('3', 'three'),
    )
    expected = [
        {
            'value': '1',
            'name': 'one'
        },
        {
            'value': '2',
            'name': 'two'
        },
        {
            'value': '3',
            'name': 'three'
        }
    ]
    assert choices_to_dict(choices) == expected


def test_printt(settings):
    settings.PRINT_LOG = True
    func = (lambda: printt("test"))
    with capture_output(func) as output:
        assert output.strip("\n") == "test"

    settings.PRINT_LOG = False
    with capture_output(func) as output:
        assert output.strip("\n") == ""


def test_send_email(settings):
    email = "test@test.com"
    subject = "test"
    message = "test"
    settings.DEBUG = True
    with capture_output(
        partial(send_email, email, subject, message)
    ) as output:
        assert output.strip("\n") == "test"

    settings.DEBUG = False
    with capture_output(
        partial(send_email, email, subject, message)
    ) as output:
        assert output.strip("\n") == ""

    assert send_email(email, subject, message)


@pytest.mark.django_db
def test_get_tokens_for_user(user):
    tokens = get_tokens_for_user(user)
    assert tokens is not None
    assert tokens["access"] is not None
    assert tokens["refresh"] is not None


def test_check_serialized_data():
    class DemoSerializer(serializers.Serializer):
        field1 = serializers.CharField()
        field2 = serializers.CharField()

    check_serialized_data(DemoSerializer, {
        'field1': "Valid",
        'field2': "Valid",
    })

    with pytest.raises(AssertionError):
        check_serialized_data(DemoSerializer, {
            'field1': "Valid"
        })
