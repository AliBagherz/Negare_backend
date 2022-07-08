from django.db import models

from art.models import ArtPiece
from authentication.models import AppUser
from core.models import BaseModel


class Comment(BaseModel):
    content = models.CharField(max_length=500)
    writer = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, related_name="written_comments", null=False, blank=False
    )
    art_piece = models.ForeignKey(
        ArtPiece, on_delete=models.CASCADE, related_name="comments", null=False, blank=False
    )
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name="child_comments", null=True, blank=True, db_index=True
    )
