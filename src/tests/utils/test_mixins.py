import pytest
from django.db import models
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from utils.base.mixins import (CustomModelViewSet, CustomResponse,
                               ModelChangeFunc, UidCreatedModel,
                               ValidateUidb64)
from utils.base.status import StatCode


class _UidCreatedModel(UidCreatedModel):
    pass


@pytest.mark.django_db
def test_uid():
    model = _UidCreatedModel()
    model.save()
    assert model.uid
    assert str(model.uid) == str(model)


@pytest.mark.django_db
class TestValidateUidb64:

    class ViewSetOne(ValidateUidb64):

        class Request:
            data = {'uidb64': 'test'}

        request = Request()

    def test_validate_uidb64(self, user):
        view = self.ViewSetOne()
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        view.request.data = {'uidb64': uidb64}
        assert view.validate_uid_token() == user

    def test_validate_uidb64_fake_user(self):
        view = self.ViewSetOne()
        response = view.validate_uid_token()
        assert response
        assert response.status_code == StatCode.HTTP_435_INVALID_UIDB64

    def test_validate_uidb64_no_uidb64(self):
        view = self.ViewSetOne()
        view.request.data = {}
        response = view.validate_uid_token()
        assert response
        assert response.status_code == StatCode.HTTP_435_INVALID_UIDB64


def test_custom_response():
    data = {'test': 'test'}
    response = CustomResponse(data, message='test')
    assert response.data == data
    assert response.message == 'test'


class TestCustomModelViewSet:
    class ViewOne(CustomModelViewSet):
        created_message: str = "Testing"

    class DemoModelOne(models.Model):
        pass

    def test_view_one(self):
        assert self.ViewOne().get_created_message() == "Testing"

    def test_created_msg_none(self):
        self.ViewOne.created_message = None
        assert self.ViewOne().get_created_message() == \
            "Object successfully created"

    def test_with_instance(self):
        self.ViewOne.created_message = None
        assert self.ViewOne().get_created_message(self.DemoModelOne()) == \
            "DemoModelOne successfully created"


@pytest.mark.django_db
class TestModelChangeMixin:

    class _Model(ModelChangeFunc):
        field = models.CharField(max_length=100)
        other = models.CharField(max_length=100)
        check = None

        def check_field(self):
            self.check = True

        monitor_change = {
            'field': check_field,
        }

    class NoModelCheck(ModelChangeFunc):
        field = models.CharField(max_length=100)
        other = models.CharField(max_length=100)

    class SimilarModelCheck(ModelChangeFunc):
        field = models.CharField(max_length=100)
        other = models.CharField(max_length=100)
        check = None

        def check_field(self):
            self.check = True

        monitor_change = {
            'field': check_field,
            'other': check_field,
        }

    class MultiModel(ModelChangeFunc):
        field = models.CharField(max_length=100)
        other = models.CharField(max_length=100)
        check = []

        def check_field(self):
            self.check.append()

        monitor_change = {
            'field': check_field,
            'other': check_field,
        }

    def test_monitor_change_fields(self):
        assert self._Model().monitor_change_fields == ['field']

    def test_monitor_change_fields_no_model_check(self):
        assert self.NoModelCheck().monitor_change_fields == []

    def test_monitor_change_funcs(self):
        assert self._Model().monitor_change_funcs == [
            self._Model.check_field,
        ]

    def test_monitor_change_funcs_no_model_check(self):
        assert self.NoModelCheck().monitor_change_funcs == []

    def test_monitor_change_funcs_similar_model_check(self):
        assert self.SimilarModelCheck().monitor_change_funcs == [
            self.SimilarModelCheck.check_field,
        ]

    def test_get_clone_field(self):
        assert self._Model().get_clone_field('field') == '__field'

    def test_get_attr(self):
        model = self._Model(
            field='test1',
            other='test2',
        )
        model.save()
        assert model.get_attr('field') == 'test1'
        assert model.get_attr('other') == 'test2'

    def test_call_updates(self):
        model = self._Model(
            field='test1',
            other='test2',
        )
        model.save()
        assert model.check is None
        assert model.field == 'test1'

        model.call_updates()
        assert model.check is True
        assert model.field == 'test1'

    def test_model_change_func_valid_change(self):
        model = self._Model(
            field='test1',
            other='test2',
        )
        model.save()
        assert model.check is None
        assert model.field == 'test1'

        model.field = 'test'
        model.save()
        assert model.check is True
        assert model.field == 'test'

    def test_model_change_func_no_change(self):
        model = self._Model(
            field='test1',
            other='test2',
        )
        model.save()
        assert model.check is None
        assert model.field == 'test1'

        model.field = 'test1'
        model.save()
        assert model.check is None
        assert model.field == 'test1'

    def test_model_change_func_invalid_change(self):
        model = self._Model(
            field='test1',
            other='test2',
        )
        model.save()
        assert model.check is None
        assert model.field == 'test1'

        model.other = "error"
        model.save()
        assert model.check is None
        assert model.field == 'test1'
        assert model.other == 'error'
