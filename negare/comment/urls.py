from django.urls import path
from . import views

app_name = "comment"
urlpatterns = [
    path("<int:art_piece_id>/add-comment/", views.AddCommentView.as_view(), name="add-comment"),
    path('<int:art_piece_id>/all-comments/', views.GetArtPieceCommentsView.as_view(), name='all-comments')
]
