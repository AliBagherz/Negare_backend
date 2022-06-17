from django.db import models

from core.models import BaseModel, Image
from django.utils.translation import gettext_lazy as _

from authentication.models import AppUser


class ArtTypeChoice(models.TextChoices):
    MUSIC = 'M', _('music')
    VIDEO = 'V', _('video')
    PICTURE = 'P', _('picture')


class ArtPiece(BaseModel):
    title = models.CharField(max_length=150, blank=True, null=False, default="")
    price = models.IntegerField(null=False, default=0)
    description = models.TextField(null=False, blank=True, default="")
    type = models.CharField(
        max_length=1,
        choices=ArtTypeChoice.choices,
        default=ArtTypeChoice.PICTURE
    )
    cover = models.ForeignKey(Image, on_delete=models.CASCADE, blank=True, related_name='art_pieces_cover', null=True)
    content = models.ForeignKey("core.Content", on_delete=models.CASCADE, related_name='art_piece', null=True)
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='art_pieces')
    liked_users = models.ManyToManyField(AppUser, related_name='liked_art_pieces')
    is_active = models.BooleanField(default=False)
    category = models.ForeignKey("category.Category", on_delete=models.CASCADE, related_name='art_pieces',
                                 null=True, default=None)
    images = models.ManyToManyField(Image, blank=True, related_name="art_pieces_images")
