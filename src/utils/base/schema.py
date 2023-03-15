from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.openapi import Schema

from rest_framework.status import is_success


class BaseSchema(SwaggerAutoSchema):
    def wrap_schema_success(self, schema):
        """Wrap schema with success, status, message, data and path fields

        :param schema: Schema to wrap
        :type schema: Schema
        :return: Wrapped schema
        :rtype: Schema
        """
        return Schema(
            type='object',
            properties={
                'success': Schema(type='boolean'),
                'message': Schema(type='string'),
                'data': schema,
                'path': Schema(type='string'),
            }
        )

    def wrap_schema_error(self, schema):
        """Wrap schema with success, status, message, data and path fields

        :param schema: Schema to wrap
        :type schema: Schema
        :return: Wrapped schema
        :rtype: Schema
        """
        return Schema(
            type='object',
            properties={
                'success': Schema(type='boolean'),
                'error': Schema(
                    type='object',
                    properties={
                        'code': Schema(type='integer'),
                        'message': Schema(type='string'),
                    }
                ),
                'data': schema,
                'path': Schema(type='string'),
            }
        )

    def get_responses(self):
        """Get responses for swagger,
        wrap all responses with success, status, message, data and path fields

        :return: Responses
        :rtype: openapi.Responses
        """
        response_serializers = self.get_response_serializers()
        data = self.get_response_schemas(response_serializers)
        for code in data.keys():
            try:
                if is_success(int(code)):
                    data[code].schema = self.wrap_schema_success(
                        data[code].schema)
                else:
                    data[code].schema = self.wrap_schema_error(
                        data[code].schema)
            except AttributeError:
                pass

        return openapi.Responses(
            responses=data
        )
