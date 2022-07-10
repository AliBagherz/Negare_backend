from django.urls import path

from userprofile.views import ProfileView, FollowUserView, AddProfileImageView

app_name = "userprofile"
urlpatterns = [
    path("<int:pk>/", ProfileView.as_view(), name="profile"),
    path("<int:pk>/follow/", FollowUserView.as_view(), name="follow-user"),
    path("add-profile-image/", AddProfileImageView.as_view(), name='add-profile-image')
]
