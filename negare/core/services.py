from rest_framework.request import Request

from core.models import Image


def get_image_full_path_by_image(image: Image, request: Request) -> str:
    from core.serializers import ImageSerializer
    url = request.build_absolute_uri()
    base_index = url.index('//')
    slash_index = url.index('/', base_index + 2)
    base_url = url[0:slash_index]
    return base_url + ImageSerializer(instance=image).data['image']['full_size']