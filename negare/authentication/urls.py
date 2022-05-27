
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import RegisterView, LoginView, SendOtpCodeView

app_name = "authentication"
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", jwt_views.TokenRefreshView.as_view(), name="logout"),
    path("verify/", jwt_views.TokenVerifyView.as_view(), name="verify"),
    path('send-otp-code/<int:pk>/', SendOtpCodeView.as_view(), name='send-otp-code')
]
