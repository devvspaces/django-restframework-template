import json
from utils.base.renderer import ApiRenderer
from django.test import RequestFactory

from utils.base.renderer import ResponseDecorator


class Response:
    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code
        self.message = None


class TestApiRenderer:
    def request(self):
        return RequestFactory().get('/')

    def test_render_with_message(self):
        response = Response({'name': 'test'}, 200)
        response.message = "test"

        renderer = ApiRenderer()
        renderer_context = {
            'request': self.request(),
            'response': response,
        }
        computed = renderer.render(
            response.data,
            renderer_context=renderer_context
        )

        expected = ResponseDecorator(
            request=renderer_context['request'],
            status=response.status_code,
            data=response.data,
            message=response.message
        ).get_response()

        assert computed is not None
        assert json.loads(computed) == expected

    def test_render_without_message(self):
        response = Response({'data': 'test'}, 200)
        renderer = ApiRenderer()
        renderer_context = {
            'request': self.request(),
            'response': response,
        }
        computed = renderer.render(
            response.data,
            renderer_context=renderer_context
        )

        expected = ResponseDecorator(
            request=renderer_context['request'],
            status=response.status_code,
            data=response.data,
            message=None
        ).get_response()

        assert computed is not None
        assert json.loads(computed) == expected

    def test_render_indent(self):
        renderer = ApiRenderer()
        request = self.request()
        response = Response({'message': 'test'}, 200)
        result = renderer.render(
            response.data,
            renderer_context={
                'request': request,
                'response': response,
                'indent': 4,
            }
        )
        assert result is not None
