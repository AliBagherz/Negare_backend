
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from .models import Comment
from ..core.serializers import ImageAvatarSerializer


class CommentSerializer(FlexFieldsModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id",
                  "content",
                  'user',
                  "created_at",
                  ]

    def get_user(self, obj: Comment):
        return {"name": obj.user.user.get_full_name(), "image": ImageAvatarSerializer(instance=obj.user.avatar).data}


class CommentPostSerializer(serializers.Serializer):
    owner_id = serializers.IntegerField(allow_null=True, required=False)
    art_piece_id = serializers.IntegerField(allow_null=True, required=False)
    content = serializers.CharField()


class ManyCommentSerializer(serializers.Serializer):
    comments = CommentSerializer(many=True)


class AllCommentSerializer(serializers.Serializer):
    search_query = serializers.CharField(
        max_length=200, allow_null=False, allow_blank=True
    )


class ArtCommentSerializer(serializers.Serializer):
    art_piece_id = serializers.IntegerField()


class AdminCommentSerializer(serializers.Serializer):
    admin_id = serializers.IntegerField()


class DeleteCommentSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()
