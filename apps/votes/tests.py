from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Poll, PollOption, Vote

User = get_user_model()


class PollModelTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123!',
            nickname='관리자',
            is_staff=True
        )
        self.poll = Poll.objects.create(
            question='가장 좋아하는 음식은?',
            created_by=self.admin,
            expires_at=timezone.now() + timedelta(days=7)
        )
        PollOption.objects.create(poll=self.poll, text='피자')
        PollOption.objects.create(poll=self.poll, text='버거')

    def test_투표_생성(self):
        self.assertEqual(self.poll.question, '가장 좋아하는 음식은?')
        self.assertEqual(self.poll.created_by, self.admin)
        self.assertFalse(self.poll.is_expired)

    def test_투표_마감(self):
        expired_poll = Poll.objects.create(
            question='지난 투표',
            created_by=self.admin,
            expires_at=timezone.now() - timedelta(days=1)
        )
        self.assertTrue(expired_poll.is_expired)

    def test_선택지_비율(self):
        option1 = self.poll.options.all()[0]
        option2 = self.poll.options.all()[1]

        option1.votes_count = 3
        option1.save()
        option2.votes_count = 7
        option2.save()

        self.assertEqual(option1.percentage, 30.0)
        self.assertEqual(option2.percentage, 70.0)


class VoteModelTest(TestCase):
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
        self.poll = Poll.objects.create(
            question='가장 좋아하는 음식은?',
            created_by=self.admin,
            expires_at=timezone.now() + timedelta(days=7)
        )
        self.option1 = PollOption.objects.create(poll=self.poll, text='피자')
        self.option2 = PollOption.objects.create(poll=self.poll, text='버거')

    def test_투표_생성(self):
        vote = Vote.objects.create(
            poll=self.poll,
            option=self.option1,
            user=self.user
        )
        self.assertEqual(vote.poll, self.poll)
        self.assertEqual(vote.option, self.option1)
        self.assertEqual(vote.user, self.user)

    def test_한_사람당_한번만_투표(self):
        Vote.objects.create(
            poll=self.poll,
            option=self.option1,
            user=self.user
        )

        with self.assertRaises(Exception):
            Vote.objects.create(
                poll=self.poll,
                option=self.option2,
                user=self.user
            )


class PollViewTest(TestCase):
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
        self.poll = Poll.objects.create(
            question='가장 좋아하는 음식은?',
            created_by=self.admin,
            expires_at=timezone.now() + timedelta(days=7)
        )
        self.option1 = PollOption.objects.create(poll=self.poll, text='피자')
        self.option2 = PollOption.objects.create(poll=self.poll, text='버거')

    def test_투표_목록_접근_가능(self):
        response = self.client.get(reverse('votes:list'))
        self.assertEqual(response.status_code, 200)

    def test_투표_상세_접근_가능(self):
        response = self.client.get(reverse('votes:detail', args=[self.poll.pk]))
        self.assertEqual(response.status_code, 200)

    def test_비로그인_사용자는_투표_불가(self):
        response = self.client.post(reverse('votes:detail', args=[self.poll.pk]), {
            'option_id': self.option1.pk
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_로그인_사용자는_투표_가능(self):
        self.client.login(username='testuser', password='testpass123!')

        # Verify poll and options exist
        self.assertIsNotNone(self.poll)
        self.assertEqual(self.poll.options.count(), 2)

        response = self.client.post(reverse('votes:detail', args=[self.poll.pk]), {
            'option_id': str(self.option1.pk)
        }, follow=False)

        # Vote was created
        vote_count = Vote.objects.filter(poll=self.poll, user=self.user).count()
        self.assertEqual(vote_count, 1)

    def test_비로그인_사용자는_투표_생성_불가(self):
        response = self.client.get(reverse('votes:create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_일반_사용자는_투표_생성_불가(self):
        self.client.login(username='testuser', password='testpass123!')
        response = self.client.get(reverse('votes:create'))
        self.assertEqual(response.status_code, 403)

    def test_관리자만_투표_생성_가능(self):
        self.client.login(username='admin', password='adminpass123!')

        expires_at = (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M')
        response = self.client.post(reverse('votes:create'), {
            'question': '새로운 투표 질문입니다',
            'expires_at': expires_at,
            'options': '선택지1\n선택지2\n선택지3'
        })

        # Check that a new poll was created
        new_poll = Poll.objects.filter(question='새로운 투표 질문입니다').first()
        self.assertIsNotNone(new_poll)
        self.assertEqual(new_poll.created_by, self.admin)
        self.assertEqual(new_poll.options.count(), 3)

    def test_관리자만_투표_수정_가능(self):
        self.client.login(username='admin', password='adminpass123!')
        response = self.client.post(reverse('votes:edit', args=[self.poll.pk]), {
            'question': '수정된 투표 질문',
            'expires_at': (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M'),
            'options': '새선택지1\n새선택지2'
        })
        self.assertEqual(response.status_code, 302)

        self.poll.refresh_from_db()
        self.assertEqual(self.poll.question, '수정된 투표 질문')

    def test_관리자만_투표_삭제_가능(self):
        self.client.login(username='admin', password='adminpass123!')
        response = self.client.post(reverse('votes:delete', args=[self.poll.pk]))
        self.assertEqual(response.status_code, 302)

        poll_exists = Poll.objects.filter(pk=self.poll.pk).exists()
        self.assertFalse(poll_exists)

    def test_마감된_투표는_결과만_표시(self):
        expired_poll = Poll.objects.create(
            question='마감된 투표',
            created_by=self.admin,
            expires_at=timezone.now() - timedelta(days=1)
        )
        PollOption.objects.create(poll=expired_poll, text='선택지')

        response = self.client.get(reverse('votes:detail', args=[expired_poll.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '마감됨')
