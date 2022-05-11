from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from negare.art.models import ArtPiece
from negare.comment.models import Comment
from negare.comment.serializers import CommentPostSerializer, CommentSerializer, ArtCommentSerializer, \
    ManyCommentSerializer, AdminCommentSerializer, DeleteCommentSerializer
from negare.comment.utils import save_a_comment, get_art_piece_comments, get_owner_comments
from negare.core.responseMessages import SuccessResponse, ErrorResponse
from negare.userprofile.models import UserProfile


@swagger_auto_schema(
    method="post",
    request_body=CommentPostSerializer,
    responses={
        201: SuccessResponse.CREATED,
        406: ErrorResponse.INVALID_DATA,
    },
)
@api_view(["POST"])
def save_comment(request):
    comment_serializer = CommentPostSerializer(data=request.data)
    if not comment_serializer.is_valid():
        return Response(
            {"Error": ErrorResponse.INVALID_DATA},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
    comment = save_a_comment(
        comment_serializer.validated_data, request.user.user_profile
    )
    return Response(
        {"success": SuccessResponse.CREATED, "comment": CommentSerializer(instance=comment).data},
        status=status.HTTP_201_CREATED
    )

@swagger_auto_schema(
    method="get",
    query_serializer=ArtCommentSerializer,
    responses={200: ManyCommentSerializer, 406: ErrorResponse.INVALID_DATA},
)
@api_view(["GET"])
def get_all_art_piece_comments(request):
    event_serializer = ArtCommentSerializer(data=request.GET)
    if not event_serializer.is_valid():
        return Response(
            {"Error": ErrorResponse.INVALID_DATA},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
    art_piece = ArtPiece.objects.get(id=event_serializer.validated_data["event_id"])
    comments = get_art_piece_comments(art_piece)
    return Response(
        {"comments": CommentSerializer(instance=comments, many=True).data},
        status=status.HTTP_200_OK,
    )


@swagger_auto_schema(
    method="get",
    query_serializer=AdminCommentSerializer,
    responses={200: ManyCommentSerializer, 406: ErrorResponse.INVALID_DATA},
)
@api_view(["GET"])
def get_all_owner_comments(request):
    admin_serializer = AdminCommentSerializer(data=request.GET)
    if not admin_serializer.is_valid():
        return Response(
            {"Error": ErrorResponse.INVALID_DATA},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
    owner = UserProfile.objects.get(id=admin_serializer.validated_data['admin_id'])
    comments = get_owner_comments(owner)
    return Response(
        {"comments": CommentSerializer(instance=comments, many=True).data},
        status=status.HTTP_200_OK,
    )


@swagger_auto_schema(
    method="get",
    responses={200: CommentSerializer, 406: ErrorResponse.INVALID_DATA},
)
@api_view(["GET"])
def get_comment_of_owner(request):
    owner = UserProfile.objects.get(user=request.user)
    comments = get_owner_comments(owner)
    return Response(
        {"comments": CommentSerializer(instance=comments, many=True).data},
        status=status.HTTP_200_OK,
    )


@swagger_auto_schema(
    method="DELETE",
    request_body=DeleteCommentSerializer,
    responses={
        201: SuccessResponse.DELETED,
        406: ErrorResponse.INVALID_DATA,
    },
)
@api_view(["DELETE"])
def remove_comment(request):
    query_serializer = DeleteCommentSerializer(data=request.data)
    if not query_serializer.is_valid():
        return Response({"status": "Error"})
    try:
        profile = get_object_or_404(UserProfile, user=request.user)
    except:
        return Response({"message": "profile not found"})
    comment = get_object_or_404(Comment, Q(owner=profile) | Q(event__owner=profile),
                                id=query_serializer.validated_data['comment_id'])
    try:
        comment.is_active = False
        comment.save()
        return Response(
            {"success": SuccessResponse.DELETED}, status=status.HTTP_200_OK
        )
    except:
        return Response(
            {"status": "Error", "detail": ErrorResponse.DID_NOT_FOLLOW},
            status=status.HTTP_400_BAD_REQUEST,
        )
