from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post, Comment
from .serializers_v2 import PostSerializerV2, CommentSerializerV2
from .permissions import IsAuthorOrReadOnly

class PostListCreateViewV2(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerV2
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailViewV2(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerV2
    permission_classes = [IsAuthorOrReadOnly]

class CommentListViewV2(generics.ListAPIView):
    serializer_class = CommentSerializerV2

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

class CommentCreateViewV2(generics.CreateAPIView):
    serializer_class = CommentSerializerV2
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(id=post_id)
        serializer.save(
            post=post,
            author=self.request.user
        )