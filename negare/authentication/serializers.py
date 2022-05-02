from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(max_length=200)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=300)
