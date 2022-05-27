from drf_yasg import openapi
from drf_yasg.openapi import Schema

from core.responseMessages import ErrorResponse


def not_found_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "detail": Schema(read_only=True, type=openapi.TYPE_STRING, default=ErrorResponse.NOT_FOUND)
    })


def success_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "success": Schema(type=openapi.TYPE_BOOLEAN, default=True)
    })


def invalid_data_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "success": Schema(type=openapi.TYPE_BOOLEAN, default=False),
        "error": Schema(type=openapi.TYPE_STRING, default=ErrorResponse.INVALID_DATA)
    })


def permission_denied_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={})
