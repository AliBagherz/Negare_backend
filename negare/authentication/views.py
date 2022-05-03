from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AppUser
from .serializers import RegisterSerializer
from core.commonResponses import invalidDataResponse

from .utils import register_user
from core.responseMessages import ErrorResponse, SuccessResponse


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            201: SuccessResponse.CREATED,
            406: ErrorResponse.INVALID_DATA,
        },
    )
    def post(self, request):
        post_data = request.data
        serializer = RegisterSerializer(data=post_data)
        if not serializer.is_valid():
            return invalidDataResponse()
        response = register_user(serializer.data)
        if isinstance(response, AppUser):
            return Response(
                {"user_id": response.id},
                status=status.HTTP_201_CREATED
            )
        return response
