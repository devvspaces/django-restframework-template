import pytest
from authentication.models import User
from project_api_key.permissions import (HasProjectAPIKey,
                                         HasStaffProjectAPIKey, check_user_set)
from rest_framework_simplejwt.models import TokenUser


@pytest.mark.django_db
def test_check_user_set(user, mocker):
    token_user = TokenUser(token="test")
    token_user.id = user.id

    request = mocker.Mock()
    request.user = token_user
    assert isinstance(request.user, TokenUser)

    assert check_user_set(request)
    assert isinstance(request.user, User)

    request = mocker.Mock()
    request.user = user
    assert isinstance(request.user, User)

    assert check_user_set(request)
    assert isinstance(request.user, User)

    token_user = TokenUser(token="test")
    token_user.id = 10  # non existent user id

    request = mocker.Mock()
    request.user = token_user
    assert check_user_set(request) is False
    assert isinstance(request.user, TokenUser)


class TestHasStaffProjectAPIKey:
    @property
    def perm(self):
        return HasStaffProjectAPIKey()

    def test_get_from_header(self, mocker):
        request = mocker.Mock()
        request.META = {
            "HTTP_API_KEY": "test",
        }
        assert self.perm.get_from_header(request, "HTTP_API_KEY") == "test"
        assert self.perm.get_from_header(request, "HTTP_API_SEC_KEY") is None

    @pytest.mark.django_db
    def test_validate_apikey_valid(self, mocker, admin_api_key_headers):
        request = mocker.Mock()
        request.META = admin_api_key_headers
        valid, api_obj = self.perm.validate_apikey(request)
        assert valid
        assert api_obj is not None

    @pytest.mark.django_db
    def test_validate_apikey_false(self, mocker, settings):
        request = mocker.Mock()
        request.META = {
            settings.API_KEY_HEADER: "test",
            settings.API_SEC_KEY_HEADER: "test",
        }
        valid, api_obj = self.perm.validate_apikey(request)
        assert valid is False
        assert api_obj is None

        request.META = {
            settings.API_KEY_HEADER: "test",
        }
        valid, api_obj = self.perm.validate_apikey(request)
        assert valid is False
        assert api_obj is None

    @pytest.mark.django_db
    def test_has_permission_valid(
        self, mocker, admin_api_key_headers, admin, user
    ):
        request = mocker.Mock()
        request.META = admin_api_key_headers
        request.user = admin
        assert self.perm.has_permission(request, None)

        request.user = TokenUser(token="test")
        request.user.id = admin.id
        assert self.perm.has_permission(request, None)

        request.user = user
        assert self.perm.has_permission(request, None)

    @pytest.mark.django_db
    def test_has_permission_invalid(
        self, mocker, admin_api_key_headers,
        admin, basic_api_key_headers
    ):
        request = mocker.Mock()
        request.META = basic_api_key_headers
        request.user = admin
        assert self.perm.has_permission(request, None) is False

        request.user = TokenUser(token="test")
        request.user.id = 10  # non existent user id
        request.META = admin_api_key_headers
        assert self.perm.has_permission(request, None) is False


class TestHasProjectAPIKey:
    @property
    def perm(self):
        return HasProjectAPIKey()

    @pytest.mark.django_db
    def test_has_permission_valid(
        self, mocker, admin_api_key_headers,
        admin, user, basic_api_key_headers
    ):
        request = mocker.Mock()
        request.META = admin_api_key_headers
        request.user = admin
        assert self.perm.has_permission(request, None)

        request.META = basic_api_key_headers
        assert self.perm.has_permission(request, None)

        request.user = TokenUser(token="test")
        request.user.id = admin.id
        assert self.perm.has_permission(request, None)

        request.user = user
        assert self.perm.has_permission(request, None)

    @pytest.mark.django_db
    def test_has_permission_invalid(
        self, mocker, admin_api_key_headers,
        admin, user, basic_api_key_headers
    ):
        # Test inactive basic keys with both admin and basic user
        request = mocker.Mock()
        request.META = basic_api_key_headers
        user.active = False
        user.save()
        request.user = admin
        assert self.perm.has_permission(request, None) is False

        request.user = user
        assert self.perm.has_permission(request, None) is False

        # Test inactive admin keys with both admin and basic user
        request.META = admin_api_key_headers
        admin.active = False
        admin.save()
        assert self.perm.has_permission(request, None) is False

        request.user = admin
        assert self.perm.has_permission(request, None) is False

        # Test invalid user
        request.user = TokenUser(token="test")
        request.user.id = 10  # non existent user id
        request.META = admin_api_key_headers
        assert self.perm.has_permission(request, None) is False
