import pytest

from project_api_key.models import ProjectApiKey
from django.contrib.auth.hashers import check_password
from django.core.cache import cache


@pytest.fixture
def api_key(user):
    return ProjectApiKey.objects.create(user=user)


@pytest.mark.django_db
class TestProjectApiKey:
    def test_str_saved(self, api_key):
        assert str(api_key) == api_key.pub_key

    def test_str_not_saved(self, user):
        api_key = ProjectApiKey(user=user)
        assert str(api_key) == "Not created"

    def test_create_project_api(self, api_key):
        assert api_key is not None
        assert api_key.pub_key is not None
        assert api_key.sec_key is not None
        assert api_key.get_cached_pass_key() is not None

    def test_cache_pass_key(self, api_key):
        api_key.cache_pass_key("test")
        assert cache.get(api_key.pub_key) == "test"

    def test_get_cached_pass_key(self, api_key):
        cache.set(api_key.pub_key, "test", timeout=api_key.cache_timeout)
        assert api_key.get_cached_pass_key() == "test"

    def test_set_sec_key(self, api_key):
        api_key.set_sec_key("test")
        assert check_password("test", api_key.sec_key)
        assert check_password("test1", api_key.sec_key) is False

    def test_check_password(self, api_key):
        api_key.set_sec_key("test")
        assert api_key.check_password("test")
        assert api_key.check_password("test1") is False

    def test_is_active(self, api_key):
        assert api_key.is_active()

    def test_is_active_false(self, user):
        user.active = False
        user.save()
        api_key = ProjectApiKey.objects.create(user=user)
        assert api_key.is_active() is False

    def test_is_staff_false(self, api_key):
        assert api_key.is_staff() is False

    def test_is_staff(self, admin):
        api_key = ProjectApiKey.objects.create(user=admin)
        assert api_key.is_staff()
