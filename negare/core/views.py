from drf_yasg.utils import swagger_auto_schema
from rest_flex_fields import FlexFieldsModelViewSet
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from .commonResponses import invalidDataResponse, successResponse
from .commonSchemas import invalid_data_schema
from .models import Image
from .schemas import content_schema
from .serializers import ImageSerializer, ContentSerializer
from .utils import add_new_content


class ImageViewSet(FlexFieldsModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


class ContentView(APIView):
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        request_body=ContentSerializer,
        responses={
            200: content_schema(),
            406: invalid_data_schema()
        },
    )
    def put(self, request):
        serializer = ContentSerializer(data={'file': request.FILES['file']})

        if not serializer.is_valid():
            return invalidDataResponse()

        content_id = add_new_content(serializer.validated_data['file'])

        return successResponse(content_id=content_id)
