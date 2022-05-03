from django.db import models
from django_minio_backend import MinioBackend, iso_date_prefix

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
    cover = models.ForeignKey(Image, on_delete=models.CASCADE, blank=True, related_name='art_pieces', null=True)
    file = models.FileField(
        storage=MinioBackend(bucket_name='art-pieces'),
        upload_to=iso_date_prefix,
        null=True
    )
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='art_pieces')
    liked_users = models.ManyToManyField(AppUser, related_name='liked_art_pieces')
