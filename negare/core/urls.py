from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet

router = DefaultRouter()
router.register(r"upload", ImageViewSet)

urlpatterns = [
    path(r"image/", include(router.urls))
]
