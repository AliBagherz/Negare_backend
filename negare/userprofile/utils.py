from negare.userprofile.models import UserProfile


def remove_follower_user(user: UserProfile, follower: UserProfile):
    follower.followers.remove(user)