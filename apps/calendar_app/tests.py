from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import datetime, timedelta
from .models import Event

User = get_user_model()


class EventModelTest(TestCase):
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

    def test_일정_생성(self):
        event = Event.objects.create(
            title='테스트 일정',
            description='테스트 설명',
            start_date=datetime.now().date(),
            created_by=self.admin
        )
        self.assertEqual(event.title, '테스트 일정')
        self.assertEqual(event.created_by, self.admin)
        self.assertFalse(event.is_deleted)

    def test_다중일_일정(self):
        start = datetime.now().date()
        end = start + timedelta(days=3)
        event = Event.objects.create(
            title='다중일 일정',
            start_date=start,
            end_date=end,
            created_by=self.admin
        )
        self.assertTrue(event.is_multiday)
        self.assertIn('~', event.duration_display)

    def test_단일일_일정(self):
        today = datetime.now().date()
        event = Event.objects.create(
            title='단일일 일정',
            start_date=today,
            created_by=self.admin
        )
        self.assertFalse(event.is_multiday)
        self.assertNotIn('~', event.duration_display)

    def test_일정_소프트_삭제(self):
        event = Event.objects.create(
            title='테스트 일정',
            start_date=datetime.now().date(),
            created_by=self.admin
        )
        event.soft_delete()
        self.assertTrue(event.is_deleted)


class EventViewTest(TestCase):
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
        self.today = datetime.now().date()
        self.event = Event.objects.create(
            title='테스트 일정',
            description='테스트 설명',
            start_date=self.today,
            location='테스트 장소',
            created_by=self.admin
        )

    def test_일정_목록_접근_가능(self):
        response = self.client.get(reverse('calendar:list'))
        self.assertEqual(response.status_code, 200)

    def test_일정_상세_접근_가능(self):
        response = self.client.get(reverse('calendar:detail', args=[self.event.pk]))
        self.assertEqual(response.status_code, 200)

    def test_비로그인_사용자는_일정_추가_불가(self):
        response = self.client.get(reverse('calendar:create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_일반_회원은_일정_추가_불가(self):
        self.client.login(username='test@example.com', password='testpass123!')
        response = self.client.get(reverse('calendar:create'))
        self.assertEqual(response.status_code, 403)

    def test_관리자만_일정_추가_가능(self):
        self.client.login(username='admin@example.com', password='adminpass123!')
        response = self.client.post(reverse('calendar:create'), {
            'title': '새로운 일정',
            'description': '새 설명',
            'start_date': self.today,
            'location': '새 장소'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(title='새로운 일정').exists())

    def test_관리자만_일정_수정_가능(self):
        self.client.login(username='admin@example.com', password='adminpass123!')
        response = self.client.post(reverse('calendar:edit', args=[self.event.pk]), {
            'title': '수정된 일정',
            'description': '수정된 설명',
            'start_date': self.today,
            'location': '수정된 장소'
        })
        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, '수정된 일정')

    def test_관리자만_일정_삭제_가능(self):
        self.client.login(username='admin@example.com', password='adminpass123!')
        response = self.client.post(reverse('calendar:delete', args=[self.event.pk]))
        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertTrue(self.event.is_deleted)

    def test_일반_회원은_일정_수정_페이지_접근_불가(self):
        self.client.login(username='test@example.com', password='testpass123!')
        response = self.client.get(reverse('calendar:edit', args=[self.event.pk]))
        self.assertEqual(response.status_code, 403)

    def test_캘린더_데이터_생성(self):
        """캘린더 뷰에 데이터가 포함되는지 확인"""
        response = self.client.get(reverse('calendar:list'))
        self.assertIn('calendar', response.context)
        self.assertIn('events_by_date', response.context)
        self.assertIn('month_name', response.context)

    def test_월_네비게이션(self):
        """이전/다음 달로 이동할 수 있는지 확인"""
        response = self.client.get(reverse('calendar:list'), {'year': 2026, 'month': 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['month'], 5)
        self.assertEqual(response.context['year'], 2026)
