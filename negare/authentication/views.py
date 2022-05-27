from django.utils.module_loading import import_string
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.commonSchemas import invalid_data_schema, success_schema, not_found_schema
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings

from .models import AppUser
from .schemas import otp_code_schema
from .serializers import RegisterSerializer, UserIdSerializer, AccessRefreshSerializer, OtpCodeSerializer
from core.commonResponses import invalidDataResponse, successResponse

from .utils import register_user, is_otp_code_valid
from .tasks import send_email


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


class SendOtpCodeView(APIView):
    permission_classes = ()
    authentication_classes = ()

    @swagger_auto_schema(
        responses={
            200: success_schema(),
            404: not_found_schema()
        },
    )
    def post(self, request, pk):
        user = get_object_or_404(AppUser.objects.all(), pk=pk)

        send_email.apply_async(args=(user.id,))

        return successResponse()


class VerifyOtpCode(APIView):
    permission_classes = ()
    authentication_classes = ()

    @swagger_auto_schema(
        request_body= OtpCodeSerializer,
        responses={
            200: otp_code_schema(),
            404: not_found_schema()
        },
    )
    def post(self, request, pk):
        user = get_object_or_404(AppUser.objects.all(), pk=pk)
        serializer = OtpCodeSerializer(data=request.data)

        if not serializer.is_valid():
            return invalidDataResponse()

        is_valid = is_otp_code_valid(user.id, serializer.validated_data['otp_code'])

        return successResponse(valid=is_valid)
