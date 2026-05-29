from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Notice

User = get_user_model()


class NoticeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123!',
            nickname='테스트사용자'
        )
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123!',
            nickname='관리자',
            is_staff=True
        )

    def test_공지사항_생성(self):
        notice = Notice.objects.create(
            title='테스트 공지',
            content='테스트 내용입니다.',
            author=self.admin,
            is_important=False
        )
        self.assertEqual(notice.title, '테스트 공지')
        self.assertEqual(notice.author, self.admin)
        self.assertFalse(notice.is_deleted)

    def test_공지사항_소프트_삭제(self):
        notice = Notice.objects.create(
            title='테스트 공지',
            content='테스트 내용입니다.',
            author=self.admin
        )
        notice.soft_delete()
        self.assertTrue(notice.is_deleted)
        self.assertEqual(Notice.objects.filter(is_deleted=False).count(), 0)

    def test_공지사항_정렬(self):
        notice1 = Notice.objects.create(
            title='일반 공지',
            content='내용1',
            author=self.admin,
            is_important=False
        )
        notice2 = Notice.objects.create(
            title='중요 공지',
            content='내용2',
            author=self.admin,
            is_important=True
        )
        notices = Notice.objects.filter(is_deleted=False)
        self.assertEqual(notices.first(), notice2)


class NoticeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123!',
            nickname='테스트사용자'
        )
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123!',
            nickname='관리자',
            is_staff=True
        )
        self.notice = Notice.objects.create(
            title='테스트 공지',
            content='테스트 내용입니다.',
            author=self.admin
        )

    def test_공지사항_목록_접근_가능(self):
        response = self.client.get(reverse('notices:list'))
        self.assertEqual(response.status_code, 200)

    def test_공지사항_상세_접근_가능(self):
        response = self.client.get(reverse('notices:detail', args=[self.notice.pk]))
        self.assertEqual(response.status_code, 200)

    def test_비로그인_사용자는_글쓰기_페이지_접근_불가(self):
        response = self.client.get(reverse('notices:create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_일반_회원은_글쓰기_접근_불가(self):
        self.client.login(username='testuser', password='testpass123!')
        response = self.client.get(reverse('notices:create'))
        self.assertEqual(response.status_code, 403)

    def test_관리자만_공지사항_작성할_수_있다(self):
        self.client.login(username='admin', password='adminpass123!')
        response = self.client.post(reverse('notices:create'), {
            'title': '새로운 공지',
            'content': '새로운 내용입니다.',
            'is_important': False
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Notice.objects.filter(title='새로운 공지').exists())

    def test_관리자만_공지사항_수정할_수_있다(self):
        self.client.login(username='admin', password='adminpass123!')
        response = self.client.post(
            reverse('notices:edit', args=[self.notice.pk]),
            {
                'title': '수정된 공지',
                'content': '수정된 내용입니다.',
                'is_important': True
            }
        )
        self.assertEqual(response.status_code, 302)
        self.notice.refresh_from_db()
        self.assertEqual(self.notice.title, '수정된 공지')
        self.assertTrue(self.notice.is_important)

    def test_관리자만_공지사항_삭제할_수_있다(self):
        self.client.login(username='admin', password='adminpass123!')
        response = self.client.post(reverse('notices:delete', args=[self.notice.pk]))
        self.assertEqual(response.status_code, 302)
        self.notice.refresh_from_db()
        self.assertTrue(self.notice.is_deleted)

    def test_일반_회원은_공지사항_수정_페이지_접근_불가(self):
        self.client.login(username='testuser', password='testpass123!')
        response = self.client.get(reverse('notices:edit', args=[self.notice.pk]))
        self.assertEqual(response.status_code, 403)

    def test_공지사항_작성_폼_유효성(self):
        self.client.login(username='admin', password='adminpass123!')
        response = self.client.post(reverse('notices:create'), {
            'title': 'a',
            'content': 'test'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Notice.objects.filter(title='a').exists())
