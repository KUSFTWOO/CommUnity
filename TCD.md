# TCD — Technical Context Document
## 코딩 철학과 패턴

> 버전: 1.0.0
> AI가 코드를 생성할 때 반드시 이 문서의 원칙을 따릅니다.

---

## 1. 핵심 코딩 철학

### 1.1 단순함이 최선이다 (Simplicity First)

> "Make it work, make it right, make it fast" — 이 순서를 지킨다.

- 기능이 동작하는 것이 먼저, 최적화는 그 다음
- 영리한 코드(clever code)보다 읽기 쉬운 코드를 우선
- 추상화는 반복이 3번 이상 발생할 때만 도입 (Rule of Three)
- 바이브코딩 특성상 AI가 나중에 수정할 수 있는 코드가 좋은 코드

### 1.2 Django의 방식을 따른다 (The Django Way)

- Django가 제공하는 내장 기능을 최대한 활용
- 바퀴를 재발명하지 않는다 (인증, 폼, Admin 등)
- **"Fat Models, Thin Views, Stupid Templates"** 패턴 준수
- ORM을 통하지 않는 Raw SQL은 절대 사용 금지

### 1.3 보안은 선택이 아닌 기본 (Security by Default)

- 모든 뷰는 기본적으로 `@login_required` 또는 권한 검사를 포함
- 사용자 입력은 항상 Django Form을 통해 검증
- 파일 업로드는 항상 타입·크기 검증 후 저장
- 환경변수는 `.env` 파일로 분리, 코드에 직접 작성 금지

---

## 2. Django 아키텍처 패턴

### 2.1 App 분리 원칙

```
하나의 App = 하나의 도메인 책임

accounts/      사용자 인증·프로필에 관한 모든 것
notices/       공지사항에 관한 모든 것
board/         게시판·댓글·좋아요에 관한 모든 것
calendar_app/  일정에 관한 모든 것
votes/         투표·설문에 관한 모든 것
dashboard/     관리자 통계·운영에 관한 모든 것
```

App 간 직접 import는 최소화. 필요하다면 단방향으로만 (순환 참조 금지).

---

### 2.2 Model 작성 패턴

```python
# ✅ 권장 패턴
class Post(models.Model):
    # 1. 일반 필드
    title   = models.CharField(max_length=200)
    content = models.TextField()

    # 2. 관계 필드
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts'
    )

    # 3. 메타 정보 필드 (항상 마지막)
    view_count = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)  # 소프트 삭제
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return f"[{self.pk}] {self.title}"

    # 비즈니스 로직은 Model 메서드로 (Fat Model)
    def soft_delete(self):
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])

    def increment_view(self):
        # F() 사용으로 레이스 컨디션 방지
        Post.objects.filter(pk=self.pk).update(
            view_count=models.F('view_count') + 1
        )
```

---

### 2.3 View 작성 패턴

```python
# ✅ 함수형 뷰(FBV) 기본 사용 — 가독성·명시성 우선
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.exceptions import PermissionDenied

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '게시글이 등록되었습니다.')
            return redirect('board:detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'board/post_form.html', {'form': form})
```

> **CBV는 언제?** ListView, DetailView 등 단순 CRUD가 반복될 때만.
> 복잡한 로직이 있는 뷰는 무조건 FBV로 명시적으로 작성.

---

### 2.4 URL 패턴

```python
# apps/board/urls.py
from django.urls import path
from . import views

app_name = 'board'  # 반드시 네임스페이스 지정

urlpatterns = [
    path('',            views.post_list,   name='list'),
    path('new/',        views.post_create, name='create'),
    path('<int:pk>/',   views.post_detail, name='detail'),
    path('<int:pk>/edit/',   views.post_edit,   name='edit'),
    path('<int:pk>/delete/', views.post_delete, name='delete'),
    path('<int:pk>/like/',   views.post_like,   name='like'),
]
```

템플릿에서는 항상 `{% url 'board:list' %}` 형태로 참조. 경로 하드코딩 금지.

---

### 2.5 Form 작성 패턴

```python
class PostForm(forms.ModelForm):
    class Meta:
        model  = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'placeholder': '제목을 입력하세요',
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'rows': 10,
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 2:
            raise forms.ValidationError('제목은 2자 이상이어야 합니다.')
        return title
```

---

## 3. 템플릿 패턴

### 3.1 상속 구조

```
templates/
├── base.html              전체 레이아웃 (head, navbar, footer)
├── components/
│   ├── post_card.html     재사용 컴포넌트
│   ├── pagination.html
│   └── alert.html
└── board/
    ├── list.html          {% extends "base.html" %}
    └── detail.html
```

### 3.2 모든 페이지 템플릿 기본 구조

```html
{% extends "base.html" %}
{% load static %}

{% block title %}게시판 — CommUnity{% endblock %}

{% block content %}
  <!-- 페이지 고유 콘텐츠 -->
{% endblock %}
```

### 3.3 Tailwind CSS 사용 규칙

- Tailwind CSS CDN 사용 (빌드 도구 없음)
- 반복 클래스 묶음은 `{% include %}` 컴포넌트로 분리
- 인라인 `style=""` 속성 사용 금지
- 반응형 클래스 작성 순서: `기본 → sm: → md: → lg:`

---

## 4. 보안 패턴

### 4.1 인증·권한 체크

```python
# 쓰기 뷰 — login_required 필수
@login_required
def post_create(request): ...

# 본인 확인 — 직접 비교
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, is_deleted=False)
    if post.author != request.user and not request.user.is_staff:
        raise PermissionDenied
    ...

# 관리자 전용 뷰
def admin_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        raise PermissionDenied
    ...
```

### 4.2 파일 업로드 검증

```python
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

def validate_image(image):
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValidationError('허용되지 않는 파일 형식입니다.')
    if image.size > MAX_IMAGE_SIZE:
        raise ValidationError('파일 크기는 5MB를 초과할 수 없습니다.')
```

### 4.3 환경변수 관리

```python
# ✅ settings/base.py
import os
SECRET_KEY    = os.environ.get('SECRET_KEY')
DEBUG         = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# ❌ 절대 금지
SECRET_KEY = 'my-hardcoded-secret-key-12345'
```

---

## 5. 데이터 접근 패턴

```python
# ✅ N+1 방지 — 관계 필드는 항상 prefetch
posts = Post.objects.select_related('author') \
                    .prefetch_related('comments', 'likes') \
                    .filter(is_deleted=False) \
                    .order_by('-created_at')

# ✅ 조회수 증가 — F() 사용
Post.objects.filter(pk=pk).update(view_count=F('view_count') + 1)

# ❌ 금지: 루프 안에서 DB 쿼리 (N+1)
for post in posts:
    print(post.author.username)  # 쿼리 N번 발생!

# ✅ 소프트 삭제 — 조회 시 항상 필터 포함
Post.objects.filter(is_deleted=False)
```

---

## 6. 에러 처리 패턴

```python
# 존재하지 않는 객체
post = get_object_or_404(Post, pk=pk, is_deleted=False)

# 사용자 피드백
messages.success(request, '성공적으로 처리되었습니다.')
messages.error(request, '오류가 발생했습니다.')

# 커스텀 에러 페이지 (config/urls.py)
handler404 = 'config.views.page_not_found'
handler500 = 'config.views.server_error'
```

---

## 7. 절대 금지 사항

```
❌ Raw SQL 직접 작성
❌ 사용자 입력을 Form 없이 직접 사용
❌ settings.py에 비밀키·패스워드 하드코딩
❌ 템플릿에서 비즈니스 로직 처리
❌ 루프 안에서 DB 쿼리 실행 (N+1)
❌ is_deleted 필터 없이 전체 조회
❌ 권한 검사 없는 쓰기 뷰
❌ 파일 확장자만 검사하는 업로드 검증
❌ URL 경로 하드코딩 ({% url %} 태그 사용)
```
