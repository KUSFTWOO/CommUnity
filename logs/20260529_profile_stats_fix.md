# 2026-05-29 내 프로필 통계 실시간 업데이트 수정

## 문제
- "내 프로필" 페이지의 게시글 수가 항상 "0"으로 표시됨
- 게시글을 작성해도 숫자가 변하지 않음

## 원인
**profile.html에서 통계가 하드코딩되어 있었음**:
```html
<div class="text-2xl font-bold text-indigo-600">0</div>
<p class="text-sm text-gray-600">작성한 게시글</p>
```

**views.py의 profile 뷰에서 통계 데이터를 계산하지 않음**:
```python
def profile(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })
```

## 해결 방법

### 1. views.py 개선

#### user_profile 뷰와 동일하게 통계 계산 추가
```python
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
    total_likes = sum(post.likes.count() for post in user_posts)
    total_comments = Comment.objects.filter(
        post__author=user,
        post__is_deleted=False,
        is_deleted=False
    ).count()
    total_views = sum(post.views for post in user_posts)

    return render(request, 'accounts/profile.html', {
        'user': user,
        'post_count': post_count,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_views': total_views,
    })
```

### 2. profile.html 개선

#### 기존 코드 (하드코딩)
```html
<div class="grid grid-cols-2 gap-4 mb-8 p-4 bg-gray-50 rounded-lg">
    <div class="text-center">
        <div class="text-2xl font-bold text-indigo-600">0</div>
        <p class="text-sm text-gray-600">작성한 게시글</p>
    </div>
    <div class="text-center">
        <div class="text-2xl font-bold text-indigo-600">0</div>
        <p class="text-sm text-gray-600">받은 좋아요</p>
    </div>
</div>
```

#### 개선된 코드 (동적 + 확장)
```html
<div class="grid grid-cols-4 gap-4 mb-8 p-4 bg-gray-50 rounded-lg">
    <div class="text-center">
        <div class="text-2xl font-bold text-indigo-600">{{ post_count }}</div>
        <p class="text-sm text-gray-600">게시글</p>
    </div>
    <div class="text-center">
        <div class="text-2xl font-bold text-indigo-600">{{ total_views }}</div>
        <p class="text-sm text-gray-600">조회수</p>
    </div>
    <div class="text-center">
        <div class="text-2xl font-bold text-indigo-600">{{ total_comments }}</div>
        <p class="text-sm text-gray-600">댓글</p>
    </div>
    <div class="text-center">
        <div class="text-2xl font-bold text-indigo-600">{{ total_likes }}</div>
        <p class="text-sm text-gray-600">좋아요</p>
    </div>
</div>
```

## 개선 사항

| 항목 | 이전 | 이후 | 효과 |
|------|------|------|------|
| 게시글 수 | 하드코딩 (0) | 동적 | ✅ 실시간 업데이트 |
| 조회수 | 없음 | 추가됨 | ✅ 새로운 통계 |
| 댓글 수 | 없음 | 추가됨 | ✅ 새로운 통계 |
| 좋아요 수 | 하드코딩 (0) | 동적 | ✅ 실시간 업데이트 |
| 레이아웃 | 2열 | 4열 | ✅ 더 나은 UI |

## 테스트 결과

### ✅ "내 프로필" 페이지 통계 확인
```
게시글: 2개
조회수: 4회
댓글: 4개
좋아요: 0명
```

결과: 모든 통계가 정상 표시됨 ✅

## 코드 일관성

이제 두 프로필 페이지의 통계 로직이 일관성 있게 구현되었습니다:

| 페이지 | URL | 뷰 함수 | 통계 |
|--------|-----|---------|------|
| 내 프로필 | `/accounts/profile/` | profile() | ✅ 동적 |
| 다른 사용자 프로필 | `/accounts/profile/[nickname]/` | user_profile() | ✅ 동적 |

## 성능 고려사항

### 쿼리 최적화
```python
# N+1 쿼리 방지
user_posts = Post.objects.filter(...).prefetch_related('likes')

# 댓글은 별도 쿼리로 최적화
Comment.objects.filter(...).count()
```

### 캐싱 권장사항 (향후)
```python
# 통계를 자주 조회하는 경우
from django.views.decorators.cache import cache_page

@cache_page(60)  # 60초마다 새로 계산
def profile(request):
    ...
```

## 결론

"내 프로필" 페이지의 통계가 완벽하게 작동하도록 수정되었습니다.
- 게시글 수가 실시간으로 업데이트됨 ✅
- 조회수, 댓글, 좋아요 수 모두 표시됨 ✅
- 더 나은 레이아웃 (4열) ✅
- user_profile 페이지와 일관성 있게 구현됨 ✅

---

**문제 해결됨**: ✅
**테스트 완료**: ✅
**배포 준비**: 준비 완료
