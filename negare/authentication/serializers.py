from rest_framework import serializers

from authentication.models import AppUser
from core.services import get_image_full_path_by_image


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(max_length=200)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=300)


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()

    def get_profile_photo(self, app_user):
        return get_image_full_path_by_image(app_user.user_profile.avatar, self.context['request']) \
            if app_user.user_profile.avatar else ''

    @staticmethod
    def get_full_name(app_user) -> str:
        return app_user.get_full_name()

    class Meta:
        model = AppUser
        fields = ["id", "full_name", "profile_photo"]


class UserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id']


class AccessRefreshSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class OtpCodeSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=300)

