from drf_yasg import openapi
from drf_yasg.openapi import Schema

from authentication.schemas import user_schema


def like_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "like": Schema(type=openapi.TYPE_BOOLEAN, default=True)
    })


def art_piece_id_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "art_piece_id": Schema(type=openapi.TYPE_INTEGER)
    })


def menu_art_piece_schema():
    return Schema(
        type=openapi.TYPE_OBJECT,
        required=[],
        properties={
            "id": Schema(type=openapi.TYPE_INTEGER),
            "title": Schema(type=openapi.TYPE_STRING),
            "type": Schema(type=openapi.TYPE_STRING),
            "image": Schema(type=openapi.TYPE_STRING),
            "count_like": Schema(type=openapi.TYPE_INTEGER),
            "count_comment": Schema(type=openapi.TYPE_INTEGER),
            "price": Schema(type=openapi.TYPE_INTEGER, default=0)
        }
    )


def gallery_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "owner": user_schema(),
        "profile": Schema(type=openapi.TYPE_OBJECT, properties={
            "follower_count": Schema(type=openapi.TYPE_INTEGER),
            "following_count": Schema(type=openapi.TYPE_INTEGER),
            "is_followed_by_you": Schema(type=openapi.TYPE_BOOLEAN),
            "is_business": Schema(type=openapi.TYPE_BOOLEAN, default=False)
        }),
        "posts_count": Schema(type=openapi.TYPE_INTEGER),
        "posts": Schema(type=openapi.TYPE_ARRAY, items=menu_art_piece_schema())
    })
