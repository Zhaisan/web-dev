from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    PostListCreateView,
    PostDetailView,
    CommentListView,
    CommentCreateView,
)

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comments/', CommentListView.as_view(), name='comment-list'),
    path('posts/<int:post_id>/comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]