from django.urls import path
from . import views

urlpatterns = [
    path('published/', views.published_posts, name='published_posts'),
    path('author/<str:author_name>/', views.posts_by_author, name='posts_by_author'),
    path('posts/', views.PostListView.as_view(), name='list_posts'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='single_post'),
    path('posts/new/', views.create_post, name='create_post'),
]
