from rest_framework import serializers

from authentication.serializers import UserSerializer
from .models import ArtPiece, ArtTypeChoice
from core.serializers import ImageSerializer


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
        if not art_piece.file:
            return ""
        return art_piece.file.url

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
    file = serializers.FileField()


class ArtPieceCoverSerializer(serializers.Serializer):
    cover = serializers.IntegerField()
    type = serializers.ChoiceField(ArtTypeChoice, default=ArtTypeChoice.PICTURE)


class ArtPieceDetailSerializer(serializers.Serializer):
    price = serializers.IntegerField(allow_null=True)
    title = serializers.CharField(max_length=200, allow_null=True)
    description = serializers.CharField(max_length=1000, allow_null=True)

class GallerySerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    posts_count = serializers.SerializerMethodField("get_posts_count")
    posts = serializers.SerializerMethodField("get_posts")
    likes_count = serializers.SerializerMethodField("get_likes_count")

    @staticmethod
    def get_posts_count(owner):
        return owner.art_pieces.count()

    @staticmethod
    def get_posts(owner):
        return owner.art_pieces

    @staticmethod
    def get_likes_count(art_piece):
        return art_piece.liked_users.count()

    class Meta:
        model = ArtPiece
        fields = [
            'title',
            'type',
            'likes_count',
            'posts_count'
        ]
        
