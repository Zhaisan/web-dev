from django.urls import path
from .views_v2 import (
    PostListCreateViewV2,
    PostDetailViewV2,
    CommentListViewV2,
    CommentCreateViewV2,
)

urlpatterns = [
    path('posts/', PostListCreateViewV2.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailViewV2.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comments/', CommentListViewV2.as_view(), name='comment-list'),
    path('posts/<int:post_id>/comments/create/', CommentCreateViewV2.as_view(), name='comment-create'),
]