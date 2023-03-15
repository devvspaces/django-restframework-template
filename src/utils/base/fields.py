"""
Custom fields to be used across all packages
"""

from django.core import checks
from django.db import models
from model_bakery import baker
from utils.base.general import create_unique_tracking_id


class ModelBakeryGenerator:

    @classmethod
    def register(cls, baker: baker):
        baker.generators.add(cls, cls.baker_gen_func)

    @classmethod
    def baker_gen_func(cls):
        """Function to generate values for model bakery to use"""
        raise NotImplementedError


class TrackingCodeField(ModelBakeryGenerator, models.CharField):
    """
    Automatically generates a tracking code that can be
    prefixed.
    prefix_max_length is 10
    """

    prefix_max_length = 10
    default_prefix = "UID"

    @classmethod
    def baker_gen_func(cls):
        return create_unique_tracking_id(prefix=cls.default_prefix)

    def __init__(self, *args, prefix: str = None, max_length: int = 225, **kwargs):
        kwargs["max_length"] = max_length
        kwargs["editable"] = False
        kwargs["unique"] = True

        if prefix is None:
            prefix = self.default_prefix

        self.prefix = prefix
        self.max_length = max_length
        super().__init__(*args, **kwargs)

    def _check_prefix_attribute(self):
        if not isinstance(self.prefix, str):
            return [
                checks.Error(
                    "'prefix' must be a string.",
                    obj=self,
                    id='tripapi.E001',
                )
            ]
        elif len(self.prefix) > self.prefix_max_length:
            return [
                checks.Error(
                    f"'prefix' length must not be greater \
than {self.prefix_max_length}.",
                    obj=self,
                    id='tripapi.E002',
                )
            ]
        else:
            return []

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_prefix_attribute(),
        ]

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["editable"]
        del kwargs["unique"]

        if self.prefix != self.default_prefix:
            kwargs['prefix'] = self.prefix
            kwargs["max_length"] = self.max_length

        return name, path, args, kwargs

    def pre_save(self, model_instance, add: bool):
        if add:
            value = create_unique_tracking_id(prefix=self.prefix)
            setattr(model_instance, self.attname, value)
            return value
        return super().pre_save(model_instance, add)
