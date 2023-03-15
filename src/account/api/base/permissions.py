from rest_framework.permissions import BasePermission, IsAuthenticated

from project_api_key.permissions import has_staff_key
from utils.base.logger import err_logger, logger  # noqa


class IsAuthenticatedAdmin(BasePermission):
    def has_permission(self, request, view):
        # Get the user, if the user is staff or admin (open access)
        try:
            if request.user.is_authenticated:
                user = request.user
                if user.staff or user.admin:
                    return True
        except Exception as e:
            err_logger.exception(e)


# Create instance for other permissisions to user
is_auth_admin = IsAuthenticatedAdmin()
is_auth_normal = IsAuthenticated()


class PermA(BasePermission):
    """
    Permission to check if user uses a staff project
    api key or is an authenticated admin
    """

    def has_permission(self, request, view):
        # Check if the user has staff project api key
        if has_staff_key.has_permission(request, view):
            return True

        # Check if the user is an authenticated admin
        if is_auth_admin.has_permission(request, view):
            return True


class PermB(BasePermission):
    """
    Permissions to check if user has a project
    staff api key and is authenticated
    Or user is authenticated admin
    """

    def has_permission(self, request, view):
        # Check if the user has project api key
        if has_staff_key.has_permission(request, view):

            # Check if the user is authenticated
            if is_auth_normal.has_permission(request, view):
                return True

        # Check if the user is an authenticated admin
        if is_auth_admin.has_permission(request, view):
            return True
