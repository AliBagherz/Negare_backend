from django.db.models import Q
from rest_framework import serializers

from authentication.serializers import UserSerializer
from category.serializers import CategorySerializer
from .models import ArtPiece, ArtTypeChoice
from core.serializers import ImageSerializer

from authentication.models import AppUser
from .services import get_art_piece_menu_dict


class ArtPieceCompactSerializer(serializers.ModelSerializer):
    cover = ImageSerializer(many=False)
    owner = UserSerializer()
    like_count = serializers.SerializerMethodField()
    is_user_liked = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    category = CategorySerializer()

    def get_is_user_liked(self, art_piece) -> bool:
        user = self.context.get("user")
        return user in art_piece.liked_users.all()

    @staticmethod
    def get_like_count(art_piece) -> int:
        return art_piece.liked_users.count()

    @staticmethod
    def get_type(art_piece):
        return art_piece.get_type_display()

    class Meta:
        model = ArtPiece
        fields = [
            "id",
            "title",
            "category",
            "cover",
            "owner",
            "like_count",
            "type",
            "is_user_liked"
        ]


class ArtPieceSerializer(ArtPieceCompactSerializer):
    images = ImageSerializer(many=True)
    url = serializers.SerializerMethodField()

    @staticmethod
    def get_url(art_piece):
        if not art_piece.content:
            return ""
        return art_piece.content.file.url

    class Meta:
        model = ArtPiece
        fields = [
            "id",
            "title",
            "price",
            "category",
            "description",
            "cover",
            "images",
            "owner",
            "like_count",
            "type",
            "is_user_liked",
            "url",
            "created_at",
            "updated_at"
        ]


class ArtPieceContentSerializer(serializers.Serializer):
    content_id = serializers.IntegerField()


class ArtPieceCoverSerializer(serializers.Serializer):
    cover = serializers.IntegerField()
    type = serializers.ChoiceField(ArtTypeChoice, default=ArtTypeChoice.PICTURE)


class ArtPieceDetailSerializer(serializers.Serializer):
    price = serializers.IntegerField(allow_null=True, required=False)
    title = serializers.CharField(max_length=200, allow_null=True, required=False)
    description = serializers.CharField(max_length=1000, allow_null=True, required=False)
    category_id = serializers.IntegerField(allow_null=False, required=False)
    image_ids = serializers.ListField(child=serializers.IntegerField(), required=False, allow_null=True)


class GallerySerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    def get_owner(self, owner):
        return UserSerializer(instance=owner, context={"request": self.context['request']}).data

    @staticmethod
    def get_posts_count(owner) -> int:
        return owner.art_pieces.count()

    def get_profile(self, owner: AppUser) -> dict:
        profile = owner.user_profile
        user = self.context['user']
        return {
            "follower_count": profile.followers.count(),
            'following_count': profile.following.count(),
            'is_followed_by_you': user.user_profile in profile.followers.all(),
            'is_business': profile.is_business
        }

    def get_posts(self, owner):
        list_posts = []
        business = self.context['business']

        if business:
            price_query = Q(price__gt=0)
        else:
            price_query = Q(price=0)

        for post in owner.art_pieces.filter(price_query).order_by('-created_at'):
            list_posts.append(get_art_piece_menu_dict(post, self.context))
        return list_posts

    class Meta:
        model = AppUser
        fields = ['owner', 'profile', 'posts_count', 'posts']


class GetExploreSerializer(serializers.Serializer):
    page = serializers.IntegerField(default=1, required=False)
    page_count = serializers.IntegerField(default=15, required=False)
    category_id = serializers.IntegerField(allow_null=True, default=None, required=False)


class GetSearchSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=200, required=False, allow_blank=True, default='')


class SearchResultSerializer(serializers.Serializer):
    artists = UserSerializer(many=True)
    art_pieces = ArtPieceCompactSerializer(many=True)


class GetGallerySerializer(serializers.Serializer):
    business = serializers.BooleanField(default=False, allow_null=True)
