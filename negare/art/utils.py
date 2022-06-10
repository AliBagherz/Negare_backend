from rest_framework.generics import get_object_or_404

from art.models import ArtPiece
from authentication.models import AppUser
from core.models import Image, Content


def likeArtPiece(art_piece: ArtPiece, user: AppUser):
    if user in art_piece.liked_users.all():
        art_piece.liked_users.remove(user)
        art_piece.save()
        return False
    else:
        art_piece.liked_users.add(user)
        art_piece.save()
        return True


def create_new_art_piece(owner: AppUser, cover_id: int, art_type: str) -> int:
    image = get_object_or_404(Image, pk=cover_id)
    art_piece = ArtPiece(owner=owner, cover=image, type=art_type)
    art_piece.save()
    return art_piece.id


def add_content_to_art_piece(art_piece: ArtPiece, content_id):
    content = get_object_or_404(Content.objects.all(), id=content_id)
    art_piece.content = content
    art_piece.save()


def add_detail_to_art_piece(art_piece: ArtPiece, data: dict):
    if data.get('title'):
        art_piece.title = data['title']
    if data.get('price'):
        art_piece.price = data['price']
    if data.get('description'):
        art_piece.description = data['description']
    art_piece.category_id = data['category_id']
    art_piece.is_active = True

    art_piece.save()

