
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import RegisterView

app_name = "authentication"
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", jwt_views.TokenObtainPairView.as_view(), name="login"),
    path("logout/", jwt_views.TokenRefreshView.as_view(), name="logout"),
    path("verify/", jwt_views.TokenVerifyView.as_view(), name="verify"),
]
