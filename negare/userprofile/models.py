from django.db import models

# Create your models here.
from negare.authentication.models import AppUser
from negare.core.models import BaseModel, Image

GENDER_CHOICES = (
    ('M', 'male'),
    ('F', 'female'),
    ('N', 'not specified'),
)


class ProfileBase(BaseModel):
    first_name = models.CharField(max_length=20, null= True, blank=True)
    last_name = models.CharField(max_length=20, null= True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, default='N')
    national_code = models.IntegerField(max_length=10, null=True, blank=True)
    birthdate = models.CharField(max_length=10, null=True, blank=True)


    class Meta:
        abstract = True


class UserProfile(ProfileBase):
    user = models.OneToOneField(
        AppUser, on_delete=models.CASCADE, related_name="user_profile"
    )
    followings = models.ManyToManyField("UserProfile", blank=True, related_name="followers")
    followers = models.ManyToManyField("UserProfile", blank=True, related_name="following")
    def __str__(self):
        return self.user.username

    avatar = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="avatar_user"
    )