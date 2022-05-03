from rest_framework import serializers

from authentication.serializers import UserSerializer
from .models import ArtPiece
from core.serializers import ImageSerializer


class ArtPieceSerializer(serializers.ModelSerializer):
    cover = ImageSerializer(many=False)
    owner = UserSerializer()
    like_count = serializers.SerializerMethodField()
    is_user_liked = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    def get_is_user_liked(self, art_piece):
        user = self.context.get("user")
        return user in art_piece.liked_users.all()

    @staticmethod
    def get_like_count(art_piece):
        return art_piece.liked_users.count()

    @staticmethod
    def get_type(art_piece):
        return art_piece.get_type_display()

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
