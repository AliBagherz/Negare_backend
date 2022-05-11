from drf_yasg import openapi
from drf_yasg.openapi import Schema


def create_user_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "user_id": Schema(type=openapi.TYPE_INTEGER)
    })
