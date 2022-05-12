from django.utils.module_loading import import_string
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.commonSchemas import invalid_data_schema
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings

from .models import AppUser
from .schemas import create_user_schema
from .serializers import RegisterSerializer, UserIdSerializer, AccessRefreshSerializer
from core.commonResponses import invalidDataResponse

from .utils import register_user
from core.responseMessages import ErrorResponse, SuccessResponse


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            201: UserIdSerializer,
            406: invalid_data_schema(),
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
                UserIdSerializer(response).data,
                status=status.HTTP_201_CREATED
            )
        return response


class LoginView(APIView):
    permission_classes = ()
    authentication_classes = ()

    @swagger_auto_schema(
        request_body=import_string(api_settings.TOKEN_OBTAIN_SERIALIZER),
        responses={
            201: AccessRefreshSerializer,
            401: invalid_data_schema(),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer_class = import_string(api_settings.TOKEN_OBTAIN_SERIALIZER)
        serializer = serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
