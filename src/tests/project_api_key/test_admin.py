from project_api_key.admin import ProjectApiKeyAdmin
from project_api_key.models import ProjectApiKey
import pytest


@pytest.fixture
def project_api_key_admin(admin_site):
    return ProjectApiKeyAdmin(ProjectApiKey, admin_site)


@pytest.fixture
def api_obj(user):
    return ProjectApiKey(user=user)


@pytest.mark.django_db
def test_save_model(
    request_storage, project_api_key_admin,
    api_obj: ProjectApiKey
):

    request, storage = request_storage
    project_api_key_admin.save_model(request, api_obj)

    key = api_obj.get_cached_pass_key()
    assert key is not None

    message = (
        "The API Secret key for {} is: {} ".format(api_obj.user, key) +
        "Please store it somewhere safe: " +
        "you will not be able to see it again."
    )

    assert message in storage.store
