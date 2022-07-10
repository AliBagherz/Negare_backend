from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import AppUser
from core.commonResponses import invalidDataResponse, successResponse
from core.commonSchemas import not_found_schema, invalid_data_schema, success_schema
from userprofile.schemas import follow_schema, business_schema
from userprofile.serializers import FullUserSerializer, AddImageSerializer
from userprofile.utils import add_profile_image, follow_user, toggle_business


class ProfileView(RetrieveUpdateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = FullUserSerializer


class AddProfileImageView(APIView):
    @swagger_auto_schema(
        request_body=AddImageSerializer,
        responses={
            200: success_schema(),
            404: not_found_schema(),
            406: invalid_data_schema()
        }
    )
    def post(self, request):
        serializer = AddImageSerializer(data=request.data)

        if not serializer.is_valid():
            return invalidDataResponse()

        add_profile_image(request.user, serializer.validated_data['profile_image_id'])

        return successResponse()


class FollowUserView(APIView):
    @swagger_auto_schema(
        responses={
            200: follow_schema(),
            404: not_found_schema(),
        },
    )
    def put(self, request, pk):
        user = get_object_or_404(AppUser.objects.all(), id=pk)

        follow_response = follow_user(user, request.user)

        return Response({"follow": follow_response}, status=200)


class ToggleBusinessView(APIView):
    @swagger_auto_schema(
        responses={
            200: business_schema(),
            404: not_found_schema(),
        },
    )
    def put(self, request):
        business_response = toggle_business(request.user)

        return Response({"business": business_response}, status=200)
