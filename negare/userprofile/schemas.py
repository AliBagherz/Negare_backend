from drf_yasg import openapi
from drf_yasg.openapi import Schema


def follow_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "follow": Schema(type=openapi.TYPE_BOOLEAN, default=True)
    })


def business_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "business": Schema(type=openapi.TYPE_BOOLEAN, default=False)
    })
