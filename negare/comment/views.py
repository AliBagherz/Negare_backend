from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from comment.Serializers import CommentsSerializer, AddCommentSerializer, \
    SingleCommentSerializer
from comment.utils import get_art_piece_comments, add_comment_to_art_piece
from core.commonResponses import invalidDataResponse
from core.commonSchemas import not_found_schema, invalid_data_schema


class AddCommentView(APIView):
    @swagger_auto_schema(
        request_body=AddCommentSerializer,
        responses={
            200: SingleCommentSerializer(),
            404: not_found_schema(),
            406: invalid_data_schema()
        }
    )
    def post(self, request, art_piece_id):
        serializer = AddCommentSerializer(data=request.data)

        if not serializer.is_valid():
            return invalidDataResponse()

        comment = add_comment_to_art_piece(art_piece_id, serializer.validated_data, request.user)

        return Response(
            SingleCommentSerializer(
                comment,
                context={
                    "user": request.user,
                    "request": request
                }
            ).data
        )


class GetArtPieceCommentsView(APIView):
    @swagger_auto_schema(
        responses={
            200: CommentsSerializer(many=True),
            404: not_found_schema()
        }
    )
    def get(self, request, art_piece_id):
        comments = get_art_piece_comments(art_piece_id, request)

        return Response(comments)
