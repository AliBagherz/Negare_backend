from rest_framework.request import Request
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

from core.models import Content, Image
from core.serializers import ImageSerializer
from jwt import decode as jwt_decode
from django.conf import settings
from typing import Optional


def add_new_content(file):
    content = Content(file=file)
    content.save()
    return content.id


def get_image_full_path_by_image(image: Image, request: Request) -> str:
    url = request.build_absolute_uri()
    base_index = url.index('//')
    slash_index = url.index('/', base_index + 2)
    base_url = url[0:slash_index]
    return base_url + ImageSerializer(instance=image).data['image']['full_size']


def get_user_id_from_jwt_token(token: str) -> Optional[int]:
    try:
        UntypedToken(token)
    except (InvalidToken, TokenError) as e:
        return None
    else:
        decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_data['user_id']
