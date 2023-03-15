from utils.base.renderer import ResponseDecorator
from django.test import SimpleTestCase
from utils.base.status import CustomStatusCode
from django.test import RequestFactory


class TestResponseDecorator(SimpleTestCase):
    def setUp(self) -> None:
        self.data = {
            'user': 1,
            'name': 'tester'
        }

    def test_with_request(self):
        request = RequestFactory().get('/')
        res = ResponseDecorator(
            request=request,
            status='200',
            data={'test': 'test'},
        )
        assert res.path == '/'

    def test_get_response(self):
        decorator = ResponseDecorator(
            data=self.data,
            status=200
        )

        response = decorator.get_response()
        expected = {
            "success": True,
            "message": CustomStatusCode.HTTP_200_OK.__doc__,
            "data": self.data,
            "path": '',
        }

        self.assertDictEqual(response, expected)
        self.assertDictEqual(decorator.data, self.data)

    def test_with_message(self):
        message = 'test message'
        decorator = ResponseDecorator(
            data=self.data,
            status=200,
            message=message
        )

        response = decorator.get_response()
        expected = {
            "success": True,
            "message": message,
            "data": self.data,
            "path": '',
        }

        self.assertDictEqual(response, expected)

    def test_set_message(self):
        decorator = ResponseDecorator(
            data=self.data,
            status=438
        )
        self.assertEqual(
            decorator.message,
            CustomStatusCode.HTTP_438_NOT_VERIFIED.__doc__
        )

    def test_get_error_response(self):
        decorator = ResponseDecorator(
            data=self.data,
            status=438
        )

        response = decorator.get_response()
        expected = {
            "success": False,
            "error": {
                "code": '438',
                "message": CustomStatusCode.HTTP_438_NOT_VERIFIED.__doc__,
            },
            "data": self.data,
            "path": '',
        }

        self.assertDictEqual(response, expected)
        self.assertDictEqual(decorator.data, self.data)
