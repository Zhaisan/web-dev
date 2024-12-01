from rest_framework import serializers
from .models import Post, Comment

class CommentSerializerV2(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'post_title', 'author', 'content', 'timestamp']

class PostSerializerV2(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializerV2(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'timestamp', 'comment_count', 'comments']
