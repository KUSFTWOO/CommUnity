from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.db.models import Count, Sum, Q
from .forms import SignUpForm, LoginForm, ProfileForm
from .models import CustomUser
from apps.board.models import Post, Comment


def signup(request):
    """회원가입"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '회원가입이 완료되었습니다. 환영합니다!')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """로그인"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.get(email=email)
            user.reset_login_fail()  # 로그인 성공 시 실패 카운트 초기화
            login(request, user)
            messages.success(request, f'{user.nickname}님 환영합니다!')
            return redirect('home')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """로그아웃"""
    logout(request)
    messages.success(request, '로그아웃되었습니다.')
    return redirect('home')


@login_required(login_url='accounts:login')
def profile(request):
    """내 프로필 - 활동 통계 포함"""
    user = request.user

    # 사용자의 게시글 (삭제되지 않은 것만)
    user_posts = Post.objects.filter(
        author=user,
        is_deleted=False
    ).prefetch_related('likes')

    # 통계 계산
    post_count = user_posts.count()

    # 총 좋아요 수 (모든 게시글이 받은 좋아요)
    total_likes = sum(post.likes.count() for post in user_posts)

    # 총 댓글 수 (자신의 게시글에 달린 댓글)
    total_comments = Comment.objects.filter(
        post__author=user,
        post__is_deleted=False,
        is_deleted=False
    ).count()

    # 총 조회수
    total_views = sum(post.views for post in user_posts)

    return render(request, 'accounts/profile.html', {
        'user': user,
        'post_count': post_count,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_views': total_views,
    })


@login_required(login_url='accounts:login')
def profile_edit(request):
    """프로필 수정"""
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필이 수정되었습니다.')
            return redirect('accounts:user_profile', nickname=user.nickname)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'accounts/profile_edit.html', {'form': form})


def user_profile(request, nickname):
    """사용자 프로필 페이지 - 활동 통계 포함"""
    user = get_object_or_404(CustomUser, nickname=nickname, is_deleted=False)

    # 사용자가 작성한 게시글 (최신순, 삭제되지 않은 것만)
    user_posts = Post.objects.filter(
        author=user,
        is_deleted=False
    ).select_related('author').prefetch_related('comments', 'likes').order_by('-created_at')

    # 현재 로그인한 사용자가 자신의 프로필을 보고 있는지 확인
    is_own_profile = request.user == user and request.user.is_authenticated

    # 통계 계산 (최적화된 쿼리)
    post_count = user_posts.count()

    # 총 좋아요 수 (각 게시글의 좋아요 개수 합산)
    total_likes = 0
    for post in user_posts:
        total_likes += post.likes.count()

    # 총 댓글 수 (삭제되지 않은 댓글만)
    total_comments = Comment.objects.filter(
        post__author=user,
        post__is_deleted=False,
        is_deleted=False
    ).count()

    # 총 조회수
    total_views = sum(post.views for post in user_posts)

    context = {
        'profile_user': user,
        'user_posts': user_posts,
        'is_own_profile': is_own_profile,
        'post_count': post_count,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_views': total_views,
    }

    return render(request, 'accounts/user_profile.html', context)
