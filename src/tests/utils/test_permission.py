from utils.base import permissions
import pytest


class TestIsAuthenticatedAdmin:

    @property
    def perm(self):
        return permissions.IsAuthenticatedAdmin()

    @pytest.mark.parametrize(
        'is_authenticated, staff, admin, expected',
        [
            (True, True, False, True),
            (True, False, True, True),
            (True, False, False, False),
            (False, False, False, False),
        ]
    )
    def test_has_permission(
        self, mocker, is_authenticated, staff, admin, expected
    ):
        mock_request = mocker.Mock()
        mock_request.user = mocker.Mock()
        mock_request.user.is_authenticated = is_authenticated
        mock_request.user.staff = staff
        mock_request.user.admin = admin

        assert self.perm.has_permission(mock_request, None) is expected


@pytest.mark.django_db
class TestLevelOne:

    @property
    def perm(self):
        return permissions.LevelOne()

    def test_has_permission_staff(
        self, mocker, admin, admin_api_key_headers
    ):
        mock_request = mocker.Mock()
        mock_request.user = admin
        mock_request.META = admin_api_key_headers

        assert self.perm.has_permission(mock_request, None)

    def test_has_permission_auth_admin(
        self, mocker, basic_api_key_headers
    ):
        mock_request = mocker.Mock()
        mock_request.user = mocker.Mock()
        mock_request.META = basic_api_key_headers

        mock_request.user.is_authenticated = True
        mock_request.user.staff = False
        mock_request.user.admin = True

        assert self.perm.has_permission(mock_request, None)


@pytest.mark.django_db
class TestLevelTwo:

    @property
    def perm(self):
        return permissions.LevelTwo()

    def test_has_permission_staff(
        self, mocker, admin, admin_api_key_headers
    ):
        mock_request = mocker.Mock()
        mock_request.user = mocker.Mock()
        mock_request.META = admin_api_key_headers
        mock_request.user.is_authenticated = True
        assert self.perm.has_permission(mock_request, None)

    def test_has_permission_auth_admin(
        self, mocker, basic_api_key_headers
    ):
        mock_request = mocker.Mock()
        mock_request.user = mocker.Mock()
        mock_request.META = basic_api_key_headers

        mock_request.user.is_authenticated = True
        mock_request.user.staff = False
        mock_request.user.admin = True

        assert self.perm.has_permission(mock_request, None)
