from rest_framework.generics import RetrieveUpdateAPIView

from authentication.models import AppUser
from userprofile.serializers import FullUserSerializer


class ProfileView(RetrieveUpdateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = FullUserSerializer
