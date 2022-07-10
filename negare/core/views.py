from drf_yasg.utils import swagger_auto_schema
from rest_flex_fields import FlexFieldsModelViewSet
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .commonResponses import invalidDataResponse, successResponse
from .commonSchemas import invalid_data_schema
from .models import Image
from .schemas import content_schema, home_page_schema
from .serializers import ImageSerializer, ContentSerializer, PagedSerializer, HomePageSerializer
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


class HomePageView(APIView):
    @swagger_auto_schema(
        query_serializer=PagedSerializer,
        responses={
            200: home_page_schema(),
            406: invalid_data_schema()
        }
    )
    def get(self, request):
        serializer = PagedSerializer(data=request.GET)

        if not serializer.is_valid():
            return invalidDataResponse()

        return Response(
            HomePageSerializer(
                instance=request.user,
                context={
                    "request": request,
                    "user": request.user,
                    "page": serializer.validated_data.get('page', 1),
                    "page_count": serializer.validated_data.get('page_count', 10)
                }
            ).data,
            status=200
        )
