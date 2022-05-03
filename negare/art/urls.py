from django.urls import path
from .views import ArtPieceView

app_name = "art"
urlpatterns = [
    path("art-piece/<int:pk>/", ArtPieceView.as_view(), name="art-piece"),
]
