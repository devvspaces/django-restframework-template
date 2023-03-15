from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

from project_api_key.permissions import check_user_set

User = get_user_model()


class IsAuthenticatedAdmin(BasePermission):
    """Validates logged in user is an admin"""
    def has_permission(self, request, view):
        if check_user_set(request):
            if request.user.is_authenticated:
                return request.user.staff or request.user.admin
        return False
