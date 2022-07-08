from typing import Optional

from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from art.models import ArtPiece
from authentication.models import AppUser
from comment.Serializers import CommentsSerializer
from comment.models import Comment


def get_art_piece_comments(art_piece_id: int, request: Request) -> list:
    comments = Comment.objects.filter(art_piece_id=art_piece_id, parent=None)
    return CommentsSerializer(
        comments,
        many=True,
        context={
            "user": request.user,
            "request": request
        }
    ).data


def add_comment_to_art_piece(art_piece_id: int, data: dict, user: AppUser) -> Comment:
    parent_id = data.get('parent_id', None)

    parent = None
    if parent_id:
        parent = get_object_or_404(Comment.objects.all(), pk=parent_id)

    art_piece = get_object_or_404(ArtPiece.objects.all(), pk=art_piece_id)

    content = data.get('content')

    comment = Comment()
    comment.parent = parent
    comment.art_piece = art_piece
    comment.content = content
    comment.writer = user
    comment.save()

    return comment
