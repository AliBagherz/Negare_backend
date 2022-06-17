from drf_yasg import openapi
from drf_yasg.openapi import Schema

from authentication.schemas import user_schema


def chat_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "id": Schema(type=openapi.TYPE_INTEGER),
        "chat_code": Schema(type=openapi.TYPE_STRING),
        "user": user_schema(),
        "last_message": Schema(type=openapi.TYPE_STRING),
        "updated_at": Schema(type=openapi.TYPE_STRING),
        "created_at": Schema(type=openapi.TYPE_STRING)
    })


def many_chat_schema():
    return Schema(type=openapi.TYPE_ARRAY, items=chat_schema())
