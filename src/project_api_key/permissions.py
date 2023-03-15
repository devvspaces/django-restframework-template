from account.models import User
from django.conf import settings
from rest_framework import permissions
from rest_framework_simplejwt.models import TokenUser
from utils.base.logger import err_logger, logger  # noqa

from .models import ProjectApiKey


def check_user_set(request) -> bool:
    """
    Check if the user is a Token user
    and set user to request
    """
    if isinstance(request.user, TokenUser):
        try:
            # Get the real user object
            user = User.objects.get(id=request.user.id)
            request.user = user
        except User.DoesNotExist:
            return False
    return True


class HasStaffProjectAPIKey(permissions.BasePermission):
    """
    This is a permission class to validate api keys
    belongs to staffs and admins only
    """

    def has_permission(self, request, view):
        valid, api_obj = self.validate_apikey(request)

        if valid:
            if not check_user_set(request):
                return False
            return api_obj.is_staff()

    def validate_apikey(self, request):
        custom_header = settings.API_KEY_HEADER
        custom_sec_header = settings.API_SEC_KEY_HEADER

        pub_key = self.get_from_header(request, custom_header)
        sec_key = self.get_from_header(request, custom_sec_header)

        try:
            api_obj = ProjectApiKey.objects.select_related(
                'user').get(pub_key=pub_key)
        except ProjectApiKey.DoesNotExist:
            return False, None

        return api_obj.check_password(sec_key), api_obj

    def get_from_header(self, request, name):
        """
        Get the api key from the request header
        """
        return request.META.get(name)


class HasProjectAPIKey(HasStaffProjectAPIKey):
    """
    This is a permission class to validate api keys is valid
    """

    def has_permission(self, request, view):
        key, api_obj = self.validate_apikey(request)

        if key:
            if not check_user_set(request):
                return False
            return api_obj.is_active()


# Create instance to use on auth permissions and others
has_staff_key = HasStaffProjectAPIKey()
has_project_key = HasProjectAPIKey()
