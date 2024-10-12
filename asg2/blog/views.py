from django.shortcuts import HttpResponse
from .models import Post

def post_list(request):
    posts = Post.objects.all()
    return HttpResponse(f'Number of posts: {posts.count()}')
