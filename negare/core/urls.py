from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet, ContentView, HomePageView

router = DefaultRouter()
router.register(r"upload", ImageViewSet)

urlpatterns = [
    path(r"image/", include(router.urls)),
    path("content/", ContentView.as_view(), name='upload-content'),
    path('homepage/', HomePageView.as_view(), name='home-page')
]
