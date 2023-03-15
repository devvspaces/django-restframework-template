from typing import Type

from rest_framework.renderers import (INDENT_SEPARATORS, LONG_SEPARATORS,
                                      SHORT_SEPARATORS, JSONRenderer)
from rest_framework.utils import json
from utils.base.status import CustomStatusCode


class ResponseDecorator:
    """
    Class for customizing rest api return response
    """
    def __init__(
        self, request=None, status: str = '200',
        data: dict = None, message: str = None
    ):

        if data is None:
            data = {}

        self.data = data

        # Use the passed status or default
        if isinstance(dict, dict):
            self.status = data.pop("status", str(status))
        else:
            self.status = str(status)
        self.path = ''
        self.success = True
        if self.status.startswith('4') or self.status.startswith('5'):
            self.success = False

        if request is not None:
            self.path = request.META['PATH_INFO']

        self.message = message
        if self.message is None:
            self.set_message()

    def set_message(self):
        for key, value in CustomStatusCode.__dict__.items():
            if key.find(self.status) != -1:
                stat_obj_property: Type[property] = value
                self.message = stat_obj_property.__doc__
                break

    def get_response(self) -> dict:
        """
        Return response in nice format
        """

        if self.success:
            return self.get_success_response()
        return self.get_error_response()

    def get_error_response(self) -> dict:
        """
        Return a error response format

        :return: Error response
        :rtype: dict
        """

        return {
            "success": False,
            "error": {
                "code": self.status,
                "message": self.message,
            },
            "data": self.data,
            "path": self.path,
        }

    def get_success_response(self) -> dict:
        """
        Return a success response format

        :return: Success response
        :rtype: dict
        """

        return {
            "success": True,
            "message": self.message,
            "data": self.data,
            "path": self.path,
        }


class ApiRenderer(JSONRenderer):
    def render(
        self, data, accepted_media_type=None,
        renderer_context: dict = None
    ):
        """
        Render `data` into JSON, returning a bytestring.

        Used restframework main code and edited it
        """

        # Customize the response
        request = renderer_context.get('request')
        response = renderer_context.get('response')
        data_kwargs = {
            'request': request,
            'status': response.status_code,
            'data': response.data,
            'message': getattr(response, 'message', None)
        }
        data = ResponseDecorator(**data_kwargs).get_response()

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS

        ret = json.dumps(
            data, cls=self.encoder_class,
            indent=indent, ensure_ascii=self.ensure_ascii,
            allow_nan=not self.strict, separators=separators
        )

        # We always fully escape \u2028 and \u2029 to ensure we output JSON
        # that is a strict javascript subset.
        # See: http://timelessrepo.com/json-isnt-a-javascript-subset
        ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
        return ret.encode()
