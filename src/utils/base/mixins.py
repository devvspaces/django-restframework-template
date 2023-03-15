"""
Mixins to be used across all packages
"""

from typing import Callable, List

from django.contrib import admin
from django.db import models
from django.db.models.query import QuerySet
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from utils.base.fields import TrackingCodeField


class BaseModelTracker(models.Model):
    """
    Abstract model for creating tracking_code for models.
    Prefix for making tracking code diffent
    on each model if needed
    """

    code_prefix = 'UID'

    tracking_code = TrackingCodeField(prefix=code_prefix, max_length=60)

    class Meta:
        abstract = True


class ModelChangeFunc(models.Model):

    class Meta:
        abstract = True

    # Setup update func
    """
    Key and Update function to run when something changes
    """
    monitor_change: dict = None

    @property
    def monitor_change_fields(self) -> list:
        if self.monitor_change:
            return [key for key, _ in self.monitor_change.items()]
        return []

    @property
    def monitor_change_funcs(self) -> List[Callable[..., None]]:
        if self.monitor_change:
            return set([func for _, func in self.monitor_change.items()])
        return tuple()

    def get_clone_field(self, name: str) -> str:
        return f"__{name}"

    def get_attr(self, field: str):
        return getattr(self, field, None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def call_updates(self):
        """Forcefully call all update functions"""
        for function in self.monitor_change_funcs:
            function(self)

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        super().save(force_insert, force_update, *args, **kwargs)

        for field in self.monitor_change_fields:
            clone_field = self.get_clone_field(field)

            # Get clone and normal values
            clone_value = self.get_attr(clone_field)
            normal_value = self.get_attr(field)

            # Check if value are different
            if normal_value != clone_value:
                # Get Function to run
                change_func = self.monitor_change.get(field)
                change_func(self)

        for field in self.monitor_change_fields:
            clone_field = self.get_clone_field(field)
            default_value = self.get_attr(field)
            setattr(self, clone_field, default_value)


class UpdateRetrieveViewSet(
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    A viewset that provides `retrieve`, `update` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class ListMixinUtils(object):
    """
    Implementation of a get reponse passed a queryset manually,
    to be used with list views sets with different list urls.
    """
    def get_with_queryset(self, queryset: QuerySet):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ExtraAdminUtils(admin.ModelAdmin):
    add_fieldsets: dict = None
    add_form = None

    def get_fieldsets(self, request, obj=None):
        if not obj and self.add_fieldsets is not None:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None and self.add_form is not None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)
