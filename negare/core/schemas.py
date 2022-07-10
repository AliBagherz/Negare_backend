from drf_yasg import openapi
from drf_yasg.openapi import Schema

from art.schemas import menu_art_piece_schema
from authentication.schemas import user_schema


def content_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "success": Schema(type=openapi.TYPE_BOOLEAN, default=True),
        "content_id": Schema(type=openapi.TYPE_INTEGER)
    })


def home_page_schema():
    return Schema(type=openapi.TYPE_OBJECT, properties={
        "stats": Schema(type=openapi.TYPE_OBJECT, properties={
            'comments_you_received_last_30_days': Schema(type=openapi.TYPE_INTEGER),
            'likes_you_received_last_30_days': Schema(type=openapi.TYPE_INTEGER),
            'comments_you_given_last_30_days': Schema(type=openapi.TYPE_INTEGER),
            'likes_you_given_last_30_days': Schema(type=openapi.TYPE_INTEGER),
        }),
        "offers": Schema(type=openapi.TYPE_OBJECT, properties={
            'most_commented_post_in_last_7_days': menu_art_piece_schema(),
            'most_liked_post_in_last_7_days': menu_art_piece_schema(),
            'most_favorite_user_in_last_7_days': user_schema()
        }),
        "feed": Schema(type=openapi.TYPE_ARRAY, items=menu_art_piece_schema())
    })
