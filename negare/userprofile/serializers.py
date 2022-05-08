from rest_framework import serializers

from negare.userprofile.models import UserProfile


class FollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class RemoveFollowerSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField("get_full_name")
    username = serializers.SerializerMethodField("get_username")
    email = serializers.SerializerMethodField("get_email")
    followers_count = serializers.SerializerMethodField("get_followers_count")
    followings_count = serializers.SerializerMethodField("get_followings_count")

    @staticmethod
    def get_full_name(user_profile):
        first = user_profile.first_name
        last = user_profile.last_name
        if first or last:
            return first + (" " if (first and last) else "") + last
        return None

    @staticmethod
    def get_username(user_profile):
        return user_profile.user.username

    @staticmethod
    def get_email(user_profile):
        return user_profile.user.email

    @staticmethod
    def get_followers_count(user_profile):
        followers = user_profile.followers
        if followers:
            return len(followers)
        return 0

    @staticmethod
    def get_followings_count(user_profile):
        followings = user_profile.followings
        if followings:
            return len(followings)
        return 0

    class Meta:
        model = UserProfile
        fields = ["id", "username", "full_name", "following_count", "followers_count", "first_name", "last_name",
                  "gender", "phone_number", "national_code", "birthdate", "avatar"]
