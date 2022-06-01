from drf_yasg import openapi
from drf_yasg.openapi import Schema


def create_user_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "user_id": Schema(type=openapi.TYPE_INTEGER)
    })


def otp_code_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "success": Schema(type=openapi.TYPE_BOOLEAN, default=True),
        "valid": Schema(type=openapi.TYPE_BOOLEAN),
        "access_token": Schema(type=openapi.TYPE_STRING)
    })
