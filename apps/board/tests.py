from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post, Comment, Like

User = get_user_model()


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123!',
            nickname='테스트사용자'
        )

    def test_게시글_생성(self):
        post = Post.objects.create(
            title='테스트 게시글',
            content='테스트 내용입니다.',
            author=self.user
        )
        self.assertEqual(post.title, '테스트 게시글')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.views, 0)
        self.assertFalse(post.is_deleted)

    def test_게시글_소프트_삭제(self):
        post = Post.objects.create(
            title='테스트 게시글',
            content='테스트 내용입니다.',
            author=self.user
        )
        post.soft_delete()
        self.assertTrue(post.is_deleted)

    def test_게시글_조회수_증가(self):
        post = Post.objects.create(
            title='테스트 게시글',
            content='테스트 내용입니다.',
            author=self.user
        )
        self.assertEqual(post.views, 0)
        post.increment_views()
        post.refresh_from_db()
        self.assertEqual(post.views, 1)


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123!',
            nickname='테스트사용자'
        )
        self.post = Post.objects.create(
            title='테스트 게시글',
            content='테스트 내용입니다.',
            author=self.user
        )

    def test_댓글_생성(self):
        comment = Comment.objects.create(
            content='테스트 댓글',
            author=self.user,
            post=self.post
        )
        self.assertEqual(comment.content, '테스트 댓글')
        self.assertFalse(comment.is_reply)
        self.assertFalse(comment.is_deleted)

    def test_대댓글_생성(self):
        parent = Comment.objects.create(
            content='부모 댓글',
            author=self.user,
            post=self.post
        )
        reply = Comment.objects.create(
            content='자식 댓글',
            author=self.user,
            post=self.post,
            parent=parent
        )
        self.assertTrue(reply.is_reply)
        self.assertEqual(reply.parent, parent)

    def test_댓글_소프트_삭제(self):
        comment = Comment.objects.create(
            content='테스트 댓글',
            author=self.user,
            post=self.post
        )
        comment.soft_delete()
        self.assertTrue(comment.is_deleted)


class LikeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123!',
            nickname='테스트사용자'
        )
        self.post = Post.objects.create(
            title='테스트 게시글',
            content='테스트 내용입니다.',
            author=self.user
        )

    def test_좋아요_생성(self):
        like = Like.objects.create(user=self.user, post=self.post)
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.post, self.post)

    def test_좋아요_중복_방지(self):
        Like.objects.create(user=self.user, post=self.post)
        with self.assertRaises(Exception):
            Like.objects.create(user=self.user, post=self.post)


class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123!',
            nickname='테스트사용자'
        )
        self.post = Post.objects.create(
            title='테스트 게시글',
            content='테스트 내용입니다.',
            author=self.user
        )

    def test_게시글_목록_접근_가능(self):
        response = self.client.get(reverse('board:list'))
        self.assertEqual(response.status_code, 200)

    def test_게시글_상세_접근_가능(self):
        response = self.client.get(reverse('board:detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_비로그인_사용자는_글쓰기_접근_불가(self):
        response = self.client.get(reverse('board:create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_로그인_사용자는_글쓰기_접근_가능(self):
        self.client.login(username='test@example.com', password='testpass123!')
        response = self.client.get(reverse('board:create'))
        self.assertEqual(response.status_code, 200)

    def test_게시글_작성_성공(self):
        self.client.login(username='test@example.com', password='testpass123!')
        response = self.client.post(reverse('board:create'), {
            'title': '새로운 게시글',
            'content': '새로운 내용입니다.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='새로운 게시글').exists())

    def test_작성자만_게시글_삭제_가능(self):
        self.client.login(username='test@example.com', password='testpass123!')
        response = self.client.post(reverse('board:delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertTrue(self.post.is_deleted)

    def test_다른_사용자는_게시글_삭제_불가(self):
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123!',
            nickname='다른사용자'
        )
        self.client.login(username='other@example.com', password='testpass123!')
        response = self.client.post(reverse('board:delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 403)

    def test_게시글_검색(self):
        Post.objects.create(
            title='검색 테스트',
            content='내용',
            author=self.user
        )
        response = self.client.get(reverse('board:list'), {'q': '검색'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 1)


class CommentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123!',
            nickname='테스트사용자'
        )
        self.post = Post.objects.create(
            title='테스트 게시글',
            content='테스트 내용입니다.',
            author=self.user
        )

    def test_비로그인_사용자는_댓글_작성_불가(self):
        response = self.client.post(reverse('board:comment_create', args=[self.post.pk]), {
            'content': '댓글 내용'
        })
        self.assertEqual(response.status_code, 302)

    def test_로그인_사용자는_댓글_작성_가능(self):
        self.client.login(username='test@example.com', password='testpass123!')
        response = self.client.post(reverse('board:comment_create', args=[self.post.pk]), {
            'content': '테스트 댓글'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(content='테스트 댓글').exists())

    def test_작성자만_댓글_삭제_가능(self):
        comment = Comment.objects.create(
            content='테스트 댓글',
            author=self.user,
            post=self.post
        )
        self.client.login(username='test@example.com', password='testpass123!')
        response = self.client.post(reverse('board:comment_delete', args=[comment.pk]))
        self.assertEqual(response.status_code, 200)
        comment.refresh_from_db()
        self.assertTrue(comment.is_deleted)


class LikeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123!',
            nickname='테스트사용자'
        )
        self.post = Post.objects.create(
            title='테스트 게시글',
            content='테스트 내용입니다.',
            author=self.user
        )

    def test_비로그인_사용자는_좋아요_불가(self):
        response = self.client.post(reverse('board:like_toggle', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)

    def test_로그인_사용자는_좋아요_가능(self):
        self.client.login(username='test@example.com', password='testpass123!')
        response = self.client.post(reverse('board:like_toggle', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Like.objects.filter(user=self.user, post=self.post).exists())

    def test_좋아요_취소_가능(self):
        Like.objects.create(user=self.user, post=self.post)
        self.client.login(username='test@example.com', password='testpass123!')
        response = self.client.post(reverse('board:like_toggle', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Like.objects.filter(user=self.user, post=self.post).exists())
