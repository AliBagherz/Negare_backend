from rest_framework.request import Request

from core.models import Content, Image
from core.serializers import ImageSerializer


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
