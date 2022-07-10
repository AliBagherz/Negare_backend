from rest_framework.generics import get_object_or_404

from authentication.models import AppUser
from core.models import Image
from userprofile.models import UserProfile


def remove_follower_user(user: UserProfile, follower: UserProfile):
    follower.followers.remove(user)


def add_profile_image(user: AppUser, profile_image_id: int):
    profile = user.user_profile
    image = get_object_or_404(Image.objects.all(), pk=profile_image_id)

    profile.avatar = image
    profile.save()


def follow_user(profile_user: AppUser, my_user: AppUser):
    my_profile = my_user.user_profile
    user_profile = profile_user.user_profile
    if my_profile in user_profile.followers.all():
        user_profile.followers.remove(my_profile)
        user_profile.save()
        return False
    else:
        user_profile.followers.add(my_profile)
        user_profile.save()
        return True
