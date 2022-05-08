from django.shortcuts import render

# Create your views here.
from django.urls import path

from negare.userprofile.urls import UserView, FollowUser, remove_follower

app_name = "userprofile"
urlpatterns = [
    path("user/", UserView.as_view(), name="user_get"),
    path("follow/", FollowUser.as_view(), name="follow"),
    path("follow/remove-follower", remove_follower, name="follow-remove")
]
