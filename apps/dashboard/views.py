from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta

from apps.accounts.models import CustomUser
from apps.board.models import Post, Comment
from apps.notices.models import Notice
from apps.calendar_app.models import Event
from apps.votes.models import Poll
from apps.surveys.models import Survey

# Admin Dashboard Views


def is_staff(user):
    return user.is_staff


def staff_required(view_func):
    """관리자 권한 확인 데코레이터"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@user_passes_test(is_staff)
def index(request):
    """대시보드 메인 - 통계 및 최근 활동"""
    # 통계 계산
    total_users = CustomUser.objects.filter(is_deleted=False).count()
    today = timezone.now().date()

    today_posts = Post.objects.filter(
        is_deleted=False,
        created_at__date=today
    ).count()

    active_polls = Poll.objects.filter(
        expires_at__gt=timezone.now()
    ).count()

    active_surveys = Survey.objects.filter(
        expires_at__gt=timezone.now()
    ).count()

    upcoming_events = Event.objects.filter(
        is_deleted=False,
        start_date__gte=today
    ).count()

    recent_posts = Post.objects.filter(
        is_deleted=False
    ).select_related('author').order_by('-created_at')[:5]

    recent_comments = Comment.objects.filter(
        is_deleted=False
    ).select_related('author', 'post').order_by('-created_at')[:5]

    recent_users = CustomUser.objects.filter(
        is_deleted=False
    ).order_by('-date_joined')[:5]

    context = {
        'total_users': total_users,
        'today_posts': today_posts,
        'active_polls': active_polls,
        'active_surveys': active_surveys,
        'upcoming_events': upcoming_events,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
        'recent_users': recent_users,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
@user_passes_test(is_staff)
def users(request):
    """회원 관리"""
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '-date_joined')

    users_list = CustomUser.objects.filter(is_deleted=False)

    if search_query:
        users_list = users_list.filter(
            Q(nickname__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    users_list = users_list.order_by(sort_by)

    # 페이징
    from django.core.paginator import Paginator
    paginator = Paginator(users_list, 20)
    page = request.GET.get('page', 1)
    users_page = paginator.get_page(page)

    context = {
        'users': users_page,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'dashboard/users.html', context)


@login_required
@user_passes_test(is_staff)
def user_detail(request, user_id):
    """사용자 상세 및 권한 변경"""
    user = get_object_or_404(CustomUser, pk=user_id, is_deleted=False)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'toggle_staff':
            user.is_staff = not user.is_staff
            user.save(update_fields=['is_staff'])
        elif action == 'toggle_active':
            user.is_active = not user.is_active
            user.save(update_fields=['is_active'])
        elif action == 'soft_delete':
            user.is_deleted = True
            user.save(update_fields=['is_deleted'])
            return redirect('dashboard:users')

        return redirect('dashboard:user_detail', user_id=user_id)

    user_stats = {
        'posts': user.posts.filter(is_deleted=False).count(),
        'comments': user.comments.filter(is_deleted=False).count(),
        'poll_votes': user.poll_votes.count(),
        'survey_responses': user.survey_responses.count(),
        'likes': user.liked_posts.count(),
    }

    context = {
        'user': user,
        'user_stats': user_stats,
    }
    return render(request, 'dashboard/user_detail.html', context)


@login_required
@user_passes_test(is_staff)
def notices(request):
    """공지사항 관리"""
    notices_list = Notice.objects.filter(
        is_deleted=False
    ).select_related('author').order_by('-is_important', '-created_at')

    context = {
        'notices': notices_list,
    }
    return render(request, 'dashboard/notices.html', context)


@login_required
@user_passes_test(is_staff)
def notice_manage(request, notice_id):
    """공지사항 수정/삭제"""
    notice = get_object_or_404(Notice, pk=notice_id, is_deleted=False)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'toggle_important':
            notice.is_important = not notice.is_important
            notice.save(update_fields=['is_important'])
        elif action == 'delete':
            notice.soft_delete()
            return redirect('dashboard:notices')
        elif action == 'edit':
            notice.title = request.POST.get('title', notice.title)
            notice.content = request.POST.get('content', notice.content)
            notice.save(update_fields=['title', 'content'])

        return redirect('dashboard:notice_manage', notice_id=notice_id)

    context = {
        'notice': notice,
    }
    return render(request, 'dashboard/notice_manage.html', context)


@login_required
@user_passes_test(is_staff)
def posts(request):
    """게시글 관리"""
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '-created_at')

    posts_list = Post.objects.filter(
        is_deleted=False
    ).select_related('author')

    if search_query:
        posts_list = posts_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    posts_list = posts_list.order_by(sort_by)

    from django.core.paginator import Paginator
    paginator = Paginator(posts_list, 20)
    page = request.GET.get('page', 1)
    posts_page = paginator.get_page(page)

    context = {
        'posts': posts_page,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'dashboard/posts.html', context)


@login_required
@user_passes_test(is_staff)
def post_manage(request, post_id):
    """게시글 상세 및 관리"""
    post = get_object_or_404(Post, pk=post_id, is_deleted=False)
    comments = post.comments.filter(is_deleted=False).select_related('author')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete':
            post.soft_delete()
            return redirect('dashboard:posts')
        elif action == 'delete_comment':
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, pk=comment_id)
            comment.soft_delete()
            return redirect('dashboard:post_manage', post_id=post_id)

    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'dashboard/post_manage.html', context)


@login_required
@user_passes_test(is_staff)
def calendar_manage(request):
    """일정 관리"""
    today = timezone.now().date()
    events_list = Event.objects.filter(
        is_deleted=False
    ).select_related('created_by').order_by('start_date')

    context = {
        'events': events_list,
        'today': today,
    }
    return render(request, 'dashboard/calendar.html', context)


@login_required
@user_passes_test(is_staff)
def event_manage(request, event_id):
    """일정 수정/삭제"""
    event = get_object_or_404(Event, pk=event_id, is_deleted=False)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete':
            event.soft_delete()
            return redirect('dashboard:calendar_manage')
        elif action == 'edit':
            event.title = request.POST.get('title', event.title)
            event.description = request.POST.get('description', event.description)
            event.save(update_fields=['title', 'description'])

        return redirect('dashboard:event_manage', event_id=event_id)

    context = {
        'event': event,
    }
    return render(request, 'dashboard/event_manage.html', context)


@login_required
@user_passes_test(is_staff)
def polls(request):
    """투표 관리"""
    polls_list = Poll.objects.select_related('created_by').order_by('-created_at')

    context = {
        'polls': polls_list,
    }
    return render(request, 'dashboard/polls.html', context)


@login_required
@user_passes_test(is_staff)
def poll_detail(request, poll_id):
    """투표 상세"""
    poll = get_object_or_404(Poll, pk=poll_id)
    options = poll.options.all().prefetch_related('user_votes')

    context = {
        'poll': poll,
        'options': options,
    }
    return render(request, 'dashboard/poll_detail.html', context)


@login_required
@user_passes_test(is_staff)
def surveys(request):
    """설문조사 관리"""
    surveys_list = Survey.objects.select_related('created_by').order_by('-created_at')

    context = {
        'surveys': surveys_list,
    }
    return render(request, 'dashboard/surveys.html', context)


@login_required
@user_passes_test(is_staff)
def survey_detail(request, survey_id):
    """설문조사 상세"""
    survey = get_object_or_404(Survey, pk=survey_id)
    questions = survey.questions.all()

    context = {
        'survey': survey,
        'questions': questions,
    }
    return render(request, 'dashboard/survey_detail.html', context)


@login_required
@user_passes_test(is_staff)
def reports(request):
    """신고 처리 (현재는 비활성화, 향후 신고 시스템 추가시 사용)"""
    return render(request, 'dashboard/reports.html')
