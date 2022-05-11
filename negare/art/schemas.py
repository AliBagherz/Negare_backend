from drf_yasg import openapi
from drf_yasg.openapi import Schema


def like_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "like": Schema(type=openapi.TYPE_BOOLEAN, default=True)
    })


def art_piece_id_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "art_piece_id": Schema(type=openapi.TYPE_INTEGER)
    })
