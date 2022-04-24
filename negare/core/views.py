from django.shortcuts import render

# Create your views here.
from rest_flex_fields import FlexFieldsModelViewSet

from negare.core.models import Image
from negare.core.serializers import ImageSerializer


class ImageViewSet(FlexFieldsModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()





