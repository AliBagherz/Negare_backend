from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from authentication.serializers import UserSerializer
from comment.models import Comment


class SingleCommentSerializer(ModelSerializer):
    writer = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'writer', 'parent', 'created_at']


class ChildCommentSerializer(ModelSerializer):
    writer = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'writer', 'created_at']


class CommentsSerializer(ModelSerializer):
    writer = UserSerializer()
    child_comments = ChildCommentSerializer(many=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'writer', 'child_comments', 'created_at']


class AddCommentSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=500)
    parent_id = serializers.IntegerField(allow_null=True, default=None)
