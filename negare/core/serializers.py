from rest_framework import serializers

from art.services import get_art_piece_menu_dict
from authentication.models import AppUser
from authentication.serializers import UserSerializer
from .models import Image
from rest_flex_fields import FlexFieldsModelSerializer
from versatileimagefield.serializers import VersatileImageFieldSerializer

from .utils import get_comment_count_user_received_in_last_30_days, get_like_count_user_received_last_30_days, \
    get_comment_count_user_give_in_last_30_days, get_like_count_user_given_last_30_days, \
    get_most_commented_art_piece_last_7_days, get_most_liked_art_piece_last_7_days, get_most_commented_user_last_7_days, \
    get_user_feed


class ImageSerializer(FlexFieldsModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("full_size", "url"),
            ("thumbnail", "thumbnail__100x100"),
        ],
        allow_null=True,
        allow_empty_file=True,
        required=False,
    )

    class Meta:
        ref_name = "image_serializer"
        model = Image
        fields = ["id", "image"]


class PkSerializer(serializers.Serializer):
    pk = serializers.IntegerField()


class ContentSerializer(serializers.Serializer):
    file = serializers.FileField()


class HomePageSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField()
    offers = serializers.SerializerMethodField()
    feed = serializers.SerializerMethodField()

    @staticmethod
    def get_stats(user) -> dict:
        return {
            'comments_you_received_last_30_days': get_comment_count_user_received_in_last_30_days(user),
            'likes_you_received_last_30_days': get_like_count_user_received_last_30_days(user),
            'comments_you_given_last_30_days': get_comment_count_user_give_in_last_30_days(user),
            'likes_you_given_last_30_days': get_like_count_user_given_last_30_days(user)
        }

    def get_offers(self, user) -> dict:
        most_commented_art_piece = get_most_commented_art_piece_last_7_days()
        most_liked_art_piece = get_most_liked_art_piece_last_7_days()
        most_commented_user = get_most_commented_user_last_7_days()
        return {
            'most_commented_art_piece_last_7_days': get_art_piece_menu_dict(
                most_commented_art_piece,
                self.context
            ) if most_commented_art_piece else {},
            'most_liked_art_piece_last_7_days': get_art_piece_menu_dict(
                most_liked_art_piece,
                self.context
            ) if most_liked_art_piece else {},
            'most_commented_user_last_7_days': UserSerializer(
                instance=most_commented_user,
                context=self.context
            ).data if most_commented_user else {}
        }

    def get_feed(self, user) -> list:
        return get_user_feed(user, self.context)

    class Meta:
        model = AppUser
        fields = ['stats', 'offers', 'feed']


class PagedSerializer(serializers.Serializer):
    page = serializers.IntegerField(default=1, allow_null=True)
    page_count = serializers.IntegerField(default=10, allow_null=True)
