from django.db.models import F, CharField, Value
from django.db.models.functions import Concat
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
    if data.get('category_id'):
        art_piece.category_id = data['category_id']
    if data.get('image_ids'):
        art_piece.images.add(*data['image_ids'])
    art_piece.is_active = True

    art_piece.save()


def get_art_pieces_on_explore(user: AppUser, data: dict):
    category_id = data.get("category_id")
    if not category_id:
        return ArtPiece.objects.raw('''
        select aa.id, count(artpiece_id) as like_count from art_artpiece aa
        inner join art_artpiece_liked_users aalu on aa.id = aalu.artpiece_id
        left join category_category cc on aa.category_id = cc.id
        where aa.owner_id != %s
        group by aa.id
        order by like_count desc
        limit %s
        offset %s
        ''', [user.id, data['page_count'], data['page'] - 1])
    else:
        return ArtPiece.objects.raw('''
            select aa.id, count(artpiece_id) as like_count from art_artpiece aa
            inner join art_artpiece_liked_users aalu on aa.id = aalu.artpiece_id
            left join category_category cc on aa.category_id = cc.id
            where aa.owner_id != %s AND (cc.id = %s)
            group by aa.id
            order by like_count desc
            limit %s
            offset %s
            ''', [user.id, category_id, data['page_count'], data['page'] - 1])


def get_art_pieces_in_search(query: str):
    return ArtPiece.objects.filter(title__icontains=query)[:10]


def get_artists_in_search(query: str):
    return AppUser.objects.annotate(
        full_name=Concat(F('first_name'), Value(' '), F('last_name'), output_field=CharField())
    ).filter(
        full_name__icontains=query
    )[:10]

