from django.shortcuts import render
from django.db.models import Q
from apps.notices.models import Notice
from apps.board.models import Post


def search_view(request):
    """통합 검색 - 공지사항과 게시판에서 키워드 검색"""
    keyword = request.GET.get('q', '').strip()
    results = []
    result_count = 0

    if keyword:
        # 공지사항 검색
        notices = Notice.objects.filter(
            Q(title__icontains=keyword) | Q(content__icontains=keyword)
        ).select_related('author').order_by('-created_at')

        # 게시판 검색
        posts = Post.objects.filter(
            Q(title__icontains=keyword) | Q(content__icontains=keyword)
        ).select_related('author').order_by('-created_at')

        # 결과 통합
        for notice in notices:
            results.append({
                'type': 'notice',
                'title': notice.title,
                'content': notice.content,
                'author': notice.author.nickname if notice.author else '관리자',
                'created_at': notice.created_at,
                'url': f'/notices/{notice.pk}/',
                'snippet': notice.content[:100] + '...' if len(notice.content) > 100 else notice.content,
            })

        for post in posts:
            results.append({
                'type': 'post',
                'title': post.title,
                'content': post.content,
                'author': post.author.nickname if post.author else '익명',
                'created_at': post.created_at,
                'url': f'/board/{post.pk}/',
                'snippet': post.content[:100] + '...' if len(post.content) > 100 else post.content,
            })

        # 최신순 정렬
        results.sort(key=lambda x: x['created_at'], reverse=True)
        result_count = len(results)

    context = {
        'keyword': keyword,
        'results': results,
        'result_count': result_count,
    }

    return render(request, 'search/search.html', context)
