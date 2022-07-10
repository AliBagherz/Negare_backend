from django.db import models

from authentication.models import AppUser
from core.models import BaseModel, Image

GENDER_CHOICES = (
    ('M', 'male'),
    ('F', 'female'),
    ('N', 'not specified'),
)


class UserProfile(BaseModel):
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, default='N')
    national_code = models.CharField(max_length=10, null=True, blank=True)
    birthdate = models.CharField(max_length=10, null=True, blank=True)
    is_business = models.BooleanField(default=False, null=False, blank=False)

    user = models.OneToOneField(
        AppUser, on_delete=models.CASCADE, related_name="user_profile"
    )

    followers = models.ManyToManyField("UserProfile", blank=True, related_name="following")

    avatar = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="avatar_user"
    )
