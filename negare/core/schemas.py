from drf_yasg import openapi
from drf_yasg.openapi import Schema


def content_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "success": Schema(type=openapi.TYPE_BOOLEAN, default=True),
        "content_id": Schema(type=openapi.TYPE_INTEGER)
    })
