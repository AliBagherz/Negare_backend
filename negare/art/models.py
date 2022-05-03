from django.db import models

from core.models import BaseModel, Image
from django.utils.translation import gettext_lazy as _

from authentication.models import AppUser


class ArtTypeChoice(models.TextChoices):
    MUSIC = 'M', _('music')
    VIDEO = 'V', _('video')
    PICTURE = 'P', _('picture')


class ArtPiece(BaseModel):
    title = models.CharField(max_length=150, blank=False, null=False)
    price = models.IntegerField(null=False, default=0)
    description = models.TextField(null=False, blank=True, default="")
    type = models.CharField(
        max_length=1,
        choices=ArtTypeChoice.choices,
        default=ArtTypeChoice.PICTURE
    )
    cover = models.ForeignKey(Image, on_delete=models.CASCADE, blank=True, related_name='art_pieces')
    url = models.URLField(null=True, blank=False)
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='art_pieces')
    liked_users = models.ManyToManyField(AppUser, related_name='liked_art_pieces')
