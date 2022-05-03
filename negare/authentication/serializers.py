from rest_framework import serializers

from authentication.models import AppUser


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(max_length=200)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=300)


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    @staticmethod
    def get_full_name(app_user):
        app_user.get_full_name()

    class Meta:
        model = AppUser
        fields = ["id", "full_name"]
