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


def user_id_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "user_id": Schema(type=openapi.TYPE_INTEGER)
    })


def not_verified_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "verified": Schema(type=openapi.TYPE_BOOLEAN, default=False)
    })


def un_authorized_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "detail": Schema(type=openapi.TYPE_STRING, default="No active account found with the given credentials")
    })


def user_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "id": Schema(type=openapi.TYPE_INTEGER),
        "full_name": Schema(type=openapi.TYPE_STRING),
        "profile_photo": Schema(type=openapi.TYPE_STRING)
    })
