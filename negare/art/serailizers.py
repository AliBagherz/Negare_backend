from rest_framework import serializers

from authentication.serializers import UserSerializer
from core.utils import get_image_full_path_by_image
from .models import ArtPiece, ArtTypeChoice
from core.serializers import ImageSerializer

from authentication.models import AppUser


class ArtPieceSerializer(serializers.ModelSerializer):
    cover = ImageSerializer(many=False)
    owner = UserSerializer()
    like_count = serializers.SerializerMethodField()
    is_user_liked = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_is_user_liked(self, art_piece):
        user = self.context.get("user")
        return user in art_piece.liked_users.all()

    @staticmethod
    def get_like_count(art_piece):
        return art_piece.liked_users.count()

    @staticmethod
    def get_type(art_piece):
        return art_piece.get_type_display()

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
            "description",
            "cover",
            "owner",
            "like_count",
            "type",
            "is_user_liked",
            "url"
        ]


class ArtPieceContentSerializer(serializers.Serializer):
    content_id = serializers.IntegerField()


class ArtPieceCoverSerializer(serializers.Serializer):
    cover = serializers.IntegerField()
    type = serializers.ChoiceField(ArtTypeChoice, default=ArtTypeChoice.PICTURE)


class ArtPieceDetailSerializer(serializers.Serializer):
    price = serializers.IntegerField(allow_null=True)
    title = serializers.CharField(max_length=200, allow_null=True)
    description = serializers.CharField(max_length=1000, allow_null=True)


class GallerySerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    def get_owner(self, owner):
        return UserSerializer(instance=owner, context={"request": self.context['request']}).data

    @staticmethod
    def get_posts_count(owner) -> int:
        return owner.art_pieces.count()

    def get_posts(self, owner):
        list_posts = []

        for post in owner.art_pieces.all():
            list_posts.append({
                "id": post.id,
                "title": post.title,
                "type": post.type,
                "image": get_image_full_path_by_image(post.cover, self.context['request']) if post.cover else '',
                "count_like": post.liked_users.count()
            })
        return list_posts

    class Meta:
        model = AppUser
        fields = ['owner', 'posts_count', 'posts']
