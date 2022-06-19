from django.db import models

# Create your models here.
from art.models import ArtPiece
from core.models import BaseModel
from userprofile.models import UserProfile


class CommentManager(models.Manager):
    def get_queryset(self):
        return super(CommentManager, self).get_queryset().filter(is_active=True)


class Comment(BaseModel):
    content = models.CharField(max_length=200)
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="comment_writer", null=True, blank=True
    )
    owner = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="comment_owner", null=True, blank=True
    )
    art_piece = models.ForeignKey(
        ArtPiece, on_delete=models.CASCADE, related_name="comment_art", null=True, blank=True
    )
    objects = CommentManager()