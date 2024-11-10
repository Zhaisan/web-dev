from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import Post
from django.shortcuts import get_object_or_404
from .forms import PostForm
from django.shortcuts import render, redirect


def published_posts(request):
    posts = Post.published.all()
    posts_data = [{"title": post.title, "author": post.author, "published_date": post.published_date} for post in posts]
    return JsonResponse(posts_data, safe=False)

def posts_by_author(request, author_name):
    posts = Post.published.by_author(author_name)
    posts_data = [{"title": post.title, "author": post.author, "published_date": post.published_date} for post in posts]
    return JsonResponse(posts_data, safe=False)

def list_posts(request):
    posts = Post.objects.all()
    posts_data = [{"id": post.id, "title": post.title, "author": post.author, "published_date": post.published_date} for post in posts]
    return JsonResponse(posts_data, safe=False)

def single_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_data = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author": post.author,
        "published_date": post.published_date
    }
    return JsonResponse(post_data)

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_posts')
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})
