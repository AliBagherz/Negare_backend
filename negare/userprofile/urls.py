from django.db.models import F
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from negare.core.models import Image
from negare.core.responseMessages import ErrorResponse, SuccessResponse
from negare.core.serializers import ImageSerializer, ImageAvatarSerializer
from negare.userprofile.models import UserProfile
from negare.userprofile.serializers import FollowSerializer, RemoveFollowerSerializer
from negare.userprofile.utils import remove_follower_user


class UserView(APIView):
    permission_classes = (AllowAny, IsAuthenticated)

    def _get_profile(self):
        try:
            return UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            raise Exception('No profile Found!')

    def get(self, request):
        try:
            profile = self._get_profile()
        except KeyError as err:
            return Response(
                {"status": "Error", "detail": ErrorResponse.NOT_PROFILE_FOUND},
                status=400,
            )
        return Response(
            {
                "username": self.request.user.username,
                "id": self.request.user.id,
                "first_name": self.request.user.first_name,
                "last_name": self.request.user.last_name,
                "full_name": self.request.user.full_name,
                "email": self.request.user.email,
                "phone_number": profile.phone_number,
                "national_code": profile.national_code,
                "birthdate": profile.birthdate,
                "gender": profile.gender,
                "avatar": ImageSerializer(instance=profile.avatar).data,
                "followings_count": self.request.followings_count,
                "followers_count": self.request.followers_count
            }
        )


class FollowUser(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer

    def _get_user_profile(self):
        return get_object_or_404(UserProfile, id=self.request.data["user_id"])

    def _get_user_profile(self):
        return get_object_or_404(UserProfile, user=self.request.user)

    def get(self, request):
        profile: UserProfile = get_object_or_404(UserProfile, user=self.request.user)
        followers = profile.followers.values('id', 'avatar', username=F('user__username'),
                                             email=F('user__email'))
        for index in range(len(followers)):
            if followers[index]["avatar"] is None:
                followers[index]["avatar"] = {'image': None}
            else:
                followers[index]["avatar"] = ImageAvatarSerializer(
                    instance=get_object_or_404(Image, id=followers[index]['avatar'])).data

        return Response(followers)

    def post(self, request):
        follower = self._get_user_profile()
        following = self._get_user_profile()
        if following in follower.followings.all():
            follower.following.remove(following)
            follower.save()
            return Response({"status": "Done Remove"})

        follower.following.add(following)
        follower.save()
        return Response({"status": "Done"})

    def delete(self, request, employee_id=None):
        follower = self._get_user_profile()
        following = self._get_user_profile()
        if following in follower.following.all():
            follower.following.remove(following)
            follower.save()
            return Response({"status": "Done"})
        return Response(
            {"status": "Error", "detail": ErrorResponse.DID_NOT_FOLLOW},
            status=400,
        )

@swagger_auto_schema(
    method="DELETE",
    request_body=RemoveFollowerSerializer,
    responses={
        201: SuccessResponse.DELETED,
        406: ErrorResponse.INVALID_DATA,
    },
)
@api_view(["DELETE"])
def remove_follower(request):
    follower_serializer = RemoveFollowerSerializer(data=request.data)
    if not follower_serializer.is_valid():
        return Response(
            {"Error": ErrorResponse.INVALID_DATA},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
    following = get_object_or_404(UserProfile, user=request.user)
    follower = get_object_or_404(UserProfile, id=follower_serializer.validated_data['user_id'])
    if follower in following.followers.all():
        remove_follower_user(follower, following)
        return Response(
            {"success": SuccessResponse.DELETED}, status=status.HTTP_200_OK
        )
    return Response(
        {"status": "Error", "detail": ErrorResponse.DID_NOT_FOLLOW},
        status=status.HTTP_400_BAD_REQUEST,
    )