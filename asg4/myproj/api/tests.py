from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Post, Comment

class PostTests(APITestCase):
    def test_list_posts(self):
        url = reverse('post-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_authenticated(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)
        url = reverse('post-list-create')
        data = {'title': 'Test Post', 'content': 'This is a test post.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Test Post')

    def test_create_post_unauthenticated(self):
        url = reverse('post-list-create')
        data = {'title': 'Test Post', 'content': 'This is a test post.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_post(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        post = Post.objects.create(title='Test Post', content='This is a test post.', author=user)
        url = reverse('post-detail', kwargs={'pk': post.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post')

    def test_update_post_authorized(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)
        post = Post.objects.create(title='Old Title', content='Old content.', author=user)
        url = reverse('post-detail', kwargs={'pk': post.id})
        data = {'title': 'New Title', 'content': 'New content.'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, 'New Title')

    def test_update_post_unauthorized(self):
        user1 = User.objects.create_user(username='author', password='testpass')
        user2 = User.objects.create_user(username='otheruser', password='testpass')
        post = Post.objects.create(title='Original Title', content='Original content.', author=user1)
        self.client.force_authenticate(user=user2)
        url = reverse('post-detail', kwargs={'pk': post.id})
        data = {'title': 'Hacked Title', 'content': 'Hacked content.'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_authorized(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)
        post = Post.objects.create(title='Test Post', content='This is a test post.', author=user)
        url = reverse('post-detail', kwargs={'pk': post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_delete_post_unauthorized(self):
        user1 = User.objects.create_user(username='author', password='testpass')
        user2 = User.objects.create_user(username='otheruser', password='testpass')
        post = Post.objects.create(title='Test Post', content='This is a test post.', author=user1)
        self.client.force_authenticate(user=user2)
        url = reverse('post-detail', kwargs={'pk': post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)

    def test_create_post_invalid_data(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)
        url = reverse('post-list-create')
        data = {'title': '', 'content': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_post(self):
        url = reverse('post-detail', kwargs={'pk': 999})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CommentTests(APITestCase):
    def test_list_comments(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        post = Post.objects.create(title='Test Post', content='This is a test post.', author=user)
        Comment.objects.create(content='First comment', post=post, author=user)
        Comment.objects.create(content='Second comment', post=post, author=user)
        url = reverse('comment-list', kwargs={'post_id': post.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_comment_authenticated(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)
        post = Post.objects.create(title='Test Post', content='This is a test post.', author=user)
        url = reverse('comment-create', kwargs={'post_id': post.id})
        data = {'content': 'This is a test comment.'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, 'This is a test comment.')

    def test_create_comment_unauthenticated(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        post = Post.objects.create(title='Test Post', content='This is a test post.', author=user)
        url = reverse('comment-create', kwargs={'post_id': post.id})
        data = {'content': 'This is a test comment.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


