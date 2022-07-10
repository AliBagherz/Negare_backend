from art.models import ArtPiece
from comment.models import Comment
from core.services import get_image_full_path_by_image


def get_art_piece_menu_dict(post: ArtPiece, context: dict) -> dict:
    return {
        "id": post.id,
        "title": post.title,
        "type": post.type,
        "image": get_image_full_path_by_image(post.cover, context['request']) if post.cover else '',
        "count_like": post.liked_users.count(),
        "count_comment": Comment.objects.filter(art_piece_id=post.id).count(),
        "price": post.price,
        "description": post.description
    }
