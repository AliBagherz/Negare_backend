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


def gallery_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "owner": Schema(type=openapi.TYPE_OBJECT, properties={
            "id": Schema(type=openapi.TYPE_INTEGER),
            "profile_photo": Schema(type=openapi.TYPE_STRING),
            "full_name": Schema(type=openapi.TYPE_STRING)
        }),
        "posts_count": Schema(type=openapi.TYPE_INTEGER),
        "posts": Schema(type=openapi.TYPE_ARRAY, items=Schema(type=openapi.TYPE_OBJECT, properties={
            "id": Schema(type=openapi.TYPE_INTEGER),
            "title": Schema(type=openapi.TYPE_STRING),
            "type": Schema(type=openapi.TYPE_STRING),
            "image": Schema(type=openapi.TYPE_STRING),
            "count_like": Schema(type=openapi.TYPE_INTEGER)
        }))
    })
