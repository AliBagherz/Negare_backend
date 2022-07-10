from rest_framework import serializers

from authentication.models import AppUser
from core.serializers import ImageSerializer
from userprofile.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    avatar = ImageSerializer(required=False)

    @staticmethod
    def get_followers_count(profile: UserProfile) -> int:
        return profile.followers.count()

    @staticmethod
    def get_following_count(profile: UserProfile) -> int:
        return profile.following.count()

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "following_count",
            "followers_count",
            "gender",
            "phone_number",
            "national_code",
            "birthdate",
            "avatar"
        ]


class FullUserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(required=False)

    class Meta:
        model = AppUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "user_profile"
        ]

    def update(self, instance, validated_data):
        profile_instance = instance.user_profile
        for key, value in validated_data.items():
            if key == "user_profile":
                for profile_key, profile_value in validated_data['user_profile'].items():
                    setattr(profile_instance, profile_key, profile_value)
            else:
                setattr(instance, key, value)

        instance.save()
        profile_instance.save()

        return instance


class AddImageSerializer(serializers.Serializer):
    profile_image_id = serializers.IntegerField()

