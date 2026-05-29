from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from .models import Post, Comment, Like
from .forms import PostForm, CommentForm


def list_view(request):
    """게시글 목록 - 누구나 조회 가능"""
    posts = Post.objects.filter(is_deleted=False).select_related('author').prefetch_related('likes')

    # 검색 기능
    query = request.GET.get('q', '').strip()
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    # 페이지네이션 (15개씩)
    paginator = Paginator(posts, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'query': query,
    }
    return render(request, 'board/list.html', context)


def detail_view(request, pk):
    """게시글 상세 - 누구나 조회 가능"""
    post = get_object_or_404(Post, pk=pk, is_deleted=False)

    # 조회수 증가 (중복 방지 - IP 기반 간단 구현)
    session_key = f'viewed_post_{pk}'
    if session_key not in request.session:
        post.increment_views()
        request.session[session_key] = True

    # 댓글 조회 (삭제되지 않은 댓글만)
    comments = post.comments.filter(is_deleted=False).select_related('author')
    root_comments = comments.filter(parent__isnull=True)

    # 좋아요 여부 확인
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(post=post, user=request.user).exists()

    context = {
        'post': post,
        'root_comments': root_comments,
        'all_comments': comments,
        'is_liked': is_liked,
        'comment_form': CommentForm(),
    }
    return render(request, 'board/detail.html', context)


@login_required
def create_view(request):
    """게시글 작성 - 로그인 필수"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '게시글이 등록되었습니다.')
            return redirect('board:detail', pk=post.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = PostForm()

    context = {'form': form}
    return render(request, 'board/form.html', context)


@login_required
def delete_view(request, pk):
    """게시글 삭제 - 작성자만 가능"""
    post = get_object_or_404(Post, pk=pk, is_deleted=False)

    if post.author != request.user and not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        post.soft_delete()
        messages.success(request, '게시글이 삭제되었습니다.')
        return redirect('board:list')

    context = {'post': post}
    return render(request, 'board/confirm_delete.html', context)


@login_required
@require_http_methods(["POST"])
def comment_create_view(request, pk):
    """댓글 작성 - HTMX"""
    post = get_object_or_404(Post, pk=pk, is_deleted=False)
    parent_id = request.POST.get('parent_id')
    parent = None

    if parent_id:
        parent = get_object_or_404(Comment, pk=parent_id, post=post, is_deleted=False)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.parent = parent
        comment.save()
        messages.success(request, '댓글이 등록되었습니다.')

    # 댓글 리스트 재렌더링
    comments = post.comments.filter(is_deleted=False).select_related('author')
    root_comments = comments.filter(parent__isnull=True)

    context = {
        'root_comments': root_comments,
        'all_comments': comments,
        'post': post,
    }
    return render(request, 'board/components/comments_list.html', context)


@login_required
@require_http_methods(["POST"])
def comment_delete_view(request, pk):
    """댓글 삭제 - HTMX"""
    comment = get_object_or_404(Comment, pk=pk, is_deleted=False)

    if comment.author != request.user and not request.user.is_staff:
        raise PermissionDenied

    post_id = comment.post_id
    comment.soft_delete()

    # 댓글 리스트 재렌더링
    post = get_object_or_404(Post, pk=post_id, is_deleted=False)
    comments = post.comments.filter(is_deleted=False).select_related('author')
    root_comments = comments.filter(parent__isnull=True)

    context = {
        'root_comments': root_comments,
        'all_comments': comments,
        'post': post,
    }
    return render(request, 'board/components/comments_list.html', context)


@login_required
@require_http_methods(["POST"])
def like_toggle_view(request, pk):
    """좋아요 토글 - HTMX"""
    post = get_object_or_404(Post, pk=pk, is_deleted=False)

    like_obj, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like_obj.delete()

    # 좋아요 버튼 상태 재렌더링
    is_liked = Like.objects.filter(post=post, user=request.user).exists()
    like_count = post.likes.count()

    context = {
        'post': post,
        'is_liked': is_liked,
        'like_count': like_count,
    }
    return render(request, 'board/components/like_button.html', context)
