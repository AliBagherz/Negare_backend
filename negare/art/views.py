from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import UserSerializer
from core.commonResponses import successResponse, invalidDataResponse
from core.commonSchemas import not_found_schema, success_schema, invalid_data_schema
from .models import ArtPiece

from art.serailizers import ArtPieceSerializer, ArtPieceCoverSerializer, ArtPieceContentSerializer, \
    ArtPieceDetailSerializer, GetExploreSerializer, SearchResultSerializer, GetSearchSerializer, \
    ArtPieceCompactSerializer, GetGallerySerializer
from .schemas import like_schema, art_piece_id_schema, gallery_schema
from .serailizers import GallerySerializer
from .utils import likeArtPiece, create_new_art_piece, add_content_to_art_piece, add_detail_to_art_piece, \
    get_art_pieces_on_explore, get_art_pieces_in_search, get_artists_in_search

from authentication.models import AppUser


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
            context={
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

        return Response({"like": likeResponse}, status=200)


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


class GalleryView(APIView):
    @swagger_auto_schema(
        query_serializer=GetGallerySerializer,
        responses={
            200: gallery_schema(),
            406: invalid_data_schema(),
            404: not_found_schema()
        },
    )
    def get(self, request, pk):
        serializer = GetGallerySerializer(data=request.GET)

        if not serializer.is_valid():
            return invalidDataResponse()

        owner = get_object_or_404(AppUser.objects.all(), pk=pk)
        business = serializer.validated_data.get('business', False)
        serializer = GallerySerializer(
            many=False,
            instance=owner,
            context={
                "request": request,
                "user": request.user,
                "business": business
            }
        )
        return Response(serializer.data, status=200)


class ExploreView(APIView):
    @swagger_auto_schema(
        query_serializer=GetExploreSerializer,
        responses={
            200: ArtPieceSerializer(many=True),
            406: invalid_data_schema()
        },
    )
    def get(self, request):
        serializer = GetExploreSerializer(data=request.GET)

        if not serializer.is_valid():
            return invalidDataResponse()

        art_pieces = get_art_pieces_on_explore(request.user, serializer.validated_data)

        return Response(
            ArtPieceSerializer(
                instance=art_pieces,
                many=True,
                context={
                    "user": request.user,
                    "request": request
                }
            ).data,
            status=200
        )


class SearchView(APIView):
    @swagger_auto_schema(
        query_serializer=GetSearchSerializer,
        responses={
            200: SearchResultSerializer,
            406: invalid_data_schema()
        }
    )
    def get(self, request):
        serializer = GetSearchSerializer(data=request.GET)

        if not serializer.is_valid():
            return invalidDataResponse()

        query = serializer.validated_data['query']
        art_pieces = get_art_pieces_in_search(query)
        artists = get_artists_in_search(query)

        return Response(
            {
                "artists": UserSerializer(instance=artists, many=True, context={"request": request}).data,
                "art_pieces": ArtPieceCompactSerializer(
                    instance=art_pieces,
                    many=True,
                    context={
                        "user": request.user,
                        "request": request
                    }
                ).data
            },
            status=200
        )
