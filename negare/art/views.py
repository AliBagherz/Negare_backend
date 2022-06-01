from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.commonResponses import successResponse, invalidDataResponse
from core.commonSchemas import not_found_schema, success_schema, invalid_data_schema
from .models import ArtPiece

from art.serailizers import ArtPieceSerializer, ArtPieceCoverSerializer, ArtPieceContentSerializer, \
    ArtPieceDetailSerializer
from .schemas import like_schema, art_piece_id_schema
from .serailizers import GallerySerializer
from .utils import likeArtPiece, create_new_art_piece, add_content_to_art_piece, add_detail_to_art_piece
from ..core.responseMessages import SuccessResponse, ErrorResponse


class ArtPieceView(APIView):
    @swagger_auto_schema(
        responses={
            200: ArtPieceSerializer,
            404: not_found_schema()
        },
    )
    def get(self, request, pk):
        art_piece = get_object_or_404(ArtPiece.objects.all(), id=pk)
        serializer = ArtPieceSerializer(
            art_piece,
            many=False,
            context=
            {
                "user": request.user,
                "request": request
            }
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ArtPieceDetailSerializer,
        responses={
            200: success_schema(),
            404: not_found_schema(),
        },
    )
    def put(self, request, pk):
        art_piece = get_object_or_404(ArtPiece.objects.all(), id=pk)
        serializer = ArtPieceDetailSerializer(data=request.data)

        if not serializer.is_valid():
            return invalidDataResponse()

        add_detail_to_art_piece(art_piece, serializer.validated_data)

        return successResponse()


class LikeArtPieceView(APIView):
    @swagger_auto_schema(
        responses={
            200: like_schema(),
            404: not_found_schema(),
        },
    )
    def put(self, request, pk):
        art_piece = get_object_or_404(ArtPiece.objects.all(), id=pk)

        likeResponse = likeArtPiece(art_piece, request.user)

        return successResponse(like=likeResponse)


class ArtPieceCoverView(APIView):
    @swagger_auto_schema(
        request_body=ArtPieceCoverSerializer,
        responses={
            200: art_piece_id_schema(),
            406: invalid_data_schema(),
        },
    )
    def post(self, request):
        serializer = ArtPieceCoverSerializer(data=request.data)

        if not serializer.is_valid():
            return invalidDataResponse()

        art_piece_id = create_new_art_piece(
            request.user,
            serializer.validated_data['cover'],
            serializer.validated_data['type']
        )

        return successResponse(art_piece_id=art_piece_id)


class ArtPieceContentView(APIView):
    @swagger_auto_schema(
        request_body=ArtPieceContentSerializer,
        responses={
            200: success_schema(),
            406: invalid_data_schema(),
            404: not_found_schema()
        },
    )
    def put(self, request, pk):
        art_piece = get_object_or_404(ArtPiece.objects.all(), id=pk)
        serializer = ArtPieceContentSerializer(data=request.data)

        if not serializer.is_valid():
            return invalidDataResponse()

        add_content_to_art_piece(art_piece, serializer.validated_data['content_id'])

        return successResponse()

class Gallery(APIView):
    @swagger_auto_schema(
        request_body=GallerySerializer,
        responses={
            200: SuccessResponse.SUCCESS,
            406: ErrorResponse.INVALID_DATA,
            404: ErrorResponse.NOT_FOUND
        },
    )
    def get(self, request):
        serializer = GallerySerializer(
            many=False,
            context=
            {
                "user": request.user,
                "request": request
            }
        )
        return Response(serializer.data)