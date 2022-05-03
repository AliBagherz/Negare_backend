from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ArtPiece

from art.serailizers import ArtPieceSerializer
from core.responseMessages import ErrorResponse


class ArtPieceView(APIView):
    @swagger_auto_schema(
        responses={
            200: ArtPieceSerializer,
            404: ErrorResponse.NOT_FOUND,
        },
    )
    def get(self, request, pk):
        art_piece = get_object_or_404(ArtPiece.objects.all(), id=pk)
        serializer = ArtPieceSerializer(art_piece, many=False, context={"user": request.user})
        return Response(serializer.data)

