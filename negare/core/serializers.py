from abc import ABC

from rest_framework import serializers

from .models import Image
from rest_flex_fields import FlexFieldsModelSerializer
from versatileimagefield.serializers import VersatileImageFieldSerializer


class ImageSerializer(FlexFieldsModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("full_size", "url"),
            ("thumbnail", "thumbnail__100x100"),
        ],
        allow_null=True,
        allow_empty_file=True,
        required=False,
    )

    class Meta:
        ref_name = "image_serializer"
        model = Image
        fields = ["id", "image"]


class PkSerializer(serializers.Serializer):
    pk = serializers.IntegerField()


class ContentSerializer(serializers.Serializer):
    file = serializers.FileField()
