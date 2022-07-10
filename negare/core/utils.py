import datetime

from django.db.models import Count
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

from art.models import ArtPiece
from art.services import get_art_piece_menu_dict
from authentication.models import AppUser
from comment.models import Comment
from core.models import Content
from jwt import decode as jwt_decode
from django.conf import settings
from typing import Optional


def add_new_content(file):
    content = Content(file=file)
    content.save()
    return content.id


def get_user_id_from_jwt_token(token: str) -> Optional[int]:
    try:
        UntypedToken(token)
    except (InvalidToken, TokenError) as e:
        return None
    else:
        decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_data['user_id']


def get_last_days_range(days: int) -> list:
    today = timezone.datetime.today()
    thirty_days_ago = today - datetime.timedelta(days=days)
    end = today + datetime.timedelta(days=1)
    return [thirty_days_ago, end]


def get_comment_count_user_give_in_last_30_days(user: AppUser) -> int:
    return Comment.objects.filter(writer=user, created_at__range=get_last_days_range(30)).count()


def get_comment_count_user_received_in_last_30_days(user: AppUser) -> int:
    return Comment.objects.filter(art_piece__owner=user, created_at__range=get_last_days_range(30)).count()


def get_like_count_user_received_last_30_days(user: AppUser) -> int:
    return int(ArtPiece.objects.filter(owner=user).aggregate(sum_likes=Count('liked_users'))['sum_likes'])


def get_like_count_user_given_last_30_days(user: AppUser) -> int:
    return int(ArtPiece.objects.filter(liked_users=user).count())


def get_most_commented_art_piece_last_7_days() -> Optional[ArtPiece]:
    query_set = Comment.objects.filter(created_at__range=get_last_days_range(7)).values('art_piece_id').annotate(
        art_piece_count=Count('art_piece_id')
    ).order_by('-art_piece_count')

    if query_set.count():
        art_piece_id = query_set.first()['art_piece_id']
    else:
        return None
    return ArtPiece.objects.get(pk=art_piece_id)


def get_most_liked_art_piece_last_7_days() -> Optional[ArtPiece]:
    query_set = ArtPiece.objects.values('id').annotate(
        count_likes=Count('liked_users')
    ).order_by('-count_likes')

    if query_set.count():
        art_piece_id = query_set.first()['id']
    else:
        return None

    return ArtPiece.objects.get(pk=art_piece_id)


def get_most_commented_user_last_7_days() -> Optional[AppUser]:
    query_set = Comment.objects.filter(created_at__range=get_last_days_range(7)).values('art_piece__owner').annotate(
        user_count=Count('art_piece__owner')
    ).order_by('-user_count')

    if query_set.count():
        user_id = query_set.first()['art_piece__owner']
    else:
        return None
    return AppUser.objects.get(pk=user_id)


def get_user_feed(user: AppUser, context: dict) -> list:
    paginator = PageNumberPagination()
    paginator.page_size = context['page_count']
    paginator.page = context['page']
    following = user.user_profile.following.values_list('user', flat=True)
    art_piece_ids = ArtPiece.objects.filter(owner__in=following).values('id').annotate(
        count_likes_comments=Count('comments', distinct=True) + Count('liked_users', distinct=True)
    ).order_by('-count_likes_comments').values_list('id', flat=True)

    paginated_ids = paginator.paginate_queryset(art_piece_ids, context['request'])
    print(paginated_ids)

    result_list = []

    for pid in paginated_ids:
        result_list.append(get_art_piece_menu_dict(ArtPiece.objects.get(pk=pid), context))

    return result_list

