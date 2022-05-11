from .models import Comment
from ..art.models import ArtPiece
from ..userprofile.models import UserProfile


def save_a_comment(validated_data: map, user):
    if "art_piece_id" in validated_data:
        art_piece = ArtPiece.objects.get(id=validated_data["art_piece_id"])
        comment = Comment.objects.create(
            content=validated_data["content"],
            art_piece=art_piece,
            user=user
        )
        return comment

    elif "owner_id" in validated_data:
        profile = UserProfile.objects.get(id=validated_data["owner_id"])
        comment = Comment.objects.create(
            content=validated_data["content"],
            owner=profile,
            user=user
        )
        return comment
    else:
        raise Exception("incorrect args")


def get_art_piece_comments(event):
    return Comment.objects.filter(event__id=event.id).order_by('-updated_at')


def get_owner_comments(owner):
    return Comment.objects.filter(owner__id=owner.id).order_by('-updated_at')
