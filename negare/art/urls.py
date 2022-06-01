from django.urls import path
from .views import ArtPieceView, LikeArtPieceView, ArtPieceCoverView, ArtPieceContentView

app_name = "art"
urlpatterns = [
    path("art-piece/<int:pk>/", ArtPieceView.as_view(), name="art-piece"),
    path("art-piece/<int:pk>/like/", LikeArtPieceView.as_view(), name='like-art-piece'),
    path("art-piece/cover/", ArtPieceCoverView.as_view(), name='art-piece-cover'),
    path("art-piece/<int:pk>/content/", ArtPieceContentView.as_view(), name='art-piece-content'),
]
