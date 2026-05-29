# CBP — Coding Best Practices
## 개발 표준, TDD 워크플로우 및 테스트 관행

> 버전: 1.0.0
> 모든 코드 생성 및 수정 시 이 문서의 기준을 따릅니다.

---

## 1. 코드 품질 기준

### 1.1 Python 코딩 스타일

- **PEP 8** 준수: 들여쓰기 4칸, 줄 최대 길이 88자
- 변수명: `snake_case` / 클래스명: `PascalCase` / 상수: `UPPER_SNAKE_CASE`
- 함수·뷰 이름은 행동을 명시: `post_create`, `comment_delete`, `vote_submit`
- 한국어 주석 허용 (한국어 커뮤니티 대상 프로젝트)

```python
# ✅ 좋은 예
def get_active_votes():
    """진행 중인 투표 목록을 반환합니다."""
    from django.utils import timezone
    return Vote.objects.filter(
        start_at__lte=timezone.now(),
        end_at__gte=timezone.now(),
        is_active=True
    )

# ❌ 나쁜 예
def votes(x):
    return Vote.objects.filter(is_active=x)
```

### 1.2 HTML 템플릿 스타일

- 들여쓰기 2칸
- 주석으로 섹션 구분: `<!-- 게시글 목록 시작 -->`
- `{% block %}` 이름은 목적 명시: `content`, `extra_css`, `extra_js`
- Tailwind 클래스 순서: 레이아웃 → 크기 → 색상 → 상태(hover/focus)

---

## 2. Git 워크플로우

### 2.1 브랜치 전략 (바이브코딩 단순화)

```
main           배포 가능한 안정 코드
  └── dev      개발 통합 브랜치
        └── feature/기능명   기능 개발 브랜치
```

바이브코딩 초기 단계에서는 `main` 직접 작업도 허용.

### 2.2 커밋 메시지 규칙

```
feat:     공지사항 작성 기능 추가
fix:      댓글 삭제 후 리다이렉트 오류 수정
style:    게시판 목록 UI 개선
refactor: PostForm 유효성 검사 로직 분리
test:     로그인 기능 테스트 케이스 추가
docs:     README 설치 방법 업데이트
chore:    requirements.txt 의존성 추가
```

### 2.3 .gitignore 필수 항목

```
*.pyc
__pycache__/
.env
db.sqlite3
media/
venv/
.DS_Store
*.log
staticfiles/
```

---

## 3. 기능 개발 워크플로우

새 기능을 추가할 때 항상 이 순서를 따릅니다.

```
Step 1   Model 작성
Step 2   Migration 생성 및 적용
Step 3   Admin 등록 (즉시 확인 가능하도록)
Step 4   Form 작성
Step 5   View 작성
Step 6   URL 등록
Step 7   Template 작성
Step 8   수동 테스트 (브라우저 확인)
Step 9   자동화 테스트 작성
```

### 3.1 Model 변경 시 필수 명령어 순서

```bash
python manage.py makemigrations   # 변경 감지
python manage.py migrate          # DB 반영
python manage.py runserver        # 동작 확인
```

### 3.2 새 App 추가 체크리스트

```
✅ python manage.py startapp 앱이름
✅ apps/ 폴더 아래로 이동
✅ config/settings/base.py → INSTALLED_APPS에 추가
✅ config/urls.py → include()로 URL 연결
✅ 앱 내부에 urls.py 생성 (app_name 지정 필수)
✅ templates/앱이름/ 폴더 생성
✅ Admin에 Model 등록
```

---

## 4. TDD 워크플로우

### 4.1 기본 사이클 (Red → Green → Refactor)

```
1. Red      실패하는 테스트 먼저 작성
2. Green    테스트를 통과하는 최소한의 코드 작성
3. Refactor 코드 정리 (테스트는 여전히 통과)
```

바이브코딩 맥락에서의 현실적 적용:
- P0 기능(인증·권한)은 TDD 적용 필수
- P1 이하 기능은 구현 후 테스트 작성 허용
- 버그 수정 시: 버그를 재현하는 테스트 먼저 작성

### 4.2 테스트 우선순위

| 우선순위 | 대상 | 이유 |
|---------|------|------|
| P0 필수 | 인증·권한 | 보안의 핵심, 실패 시 치명적 |
| P0 필수 | 데이터 CRUD | 핵심 기능 |
| P1 중요 | 폼 유효성 검사 | 잘못된 데이터 차단 |
| P2 권장 | 뷰 상태코드 | HTTP 200/302/403/404 확인 |
| P3 선택 | 템플릿 렌더링 | 내용 표시 확인 |

---

## 5. 테스트 작성 기준

### 5.1 테스트 파일 구조

```
apps/
└── board/
    ├── models.py
    ├── views.py
    └── tests/
        ├── __init__.py
        ├── test_models.py      Model 단위 테스트
        ├── test_views.py       View 통합 테스트
        └── test_forms.py       Form 유효성 테스트
```

### 5.2 테스트 작성 패턴

```python
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.board.models import Post

User = get_user_model()


class PostCreateViewTest(TestCase):
    def setUp(self):
        """각 테스트 전 실행 — 공통 테스트 데이터 준비"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123!'
        )

    # 테스트 메서드명은 한국어로 — 의도를 명확하게
    def test_비로그인_사용자는_글쓰기_페이지에_접근할_수_없다(self):
        response = self.client.get(reverse('board:create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_로그인_사용자는_게시글을_작성할_수_있다(self):
        self.client.login(username='testuser', password='testpass123!')
        response = self.client.post(reverse('board:create'), {
            'title': '테스트 게시글',
            'content': '테스트 내용입니다.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='테스트 게시글').exists())

    def test_빈_제목으로는_게시글을_작성할_수_없다(self):
        self.client.login(username='testuser', password='testpass123!')
        response = self.client.post(reverse('board:create'), {
            'title': '',
            'content': '내용',
        })
        self.assertEqual(response.status_code, 200)  # 폼 재표시
        self.assertFalse(Post.objects.exists())
```

### 5.3 테스트 실행 명령어

```bash
# 전체 테스트 실행
python manage.py test

# 특정 앱만 테스트
python manage.py test apps.board

# 특정 파일만 테스트
python manage.py test apps.board.tests.test_views

# 커버리지 측정
pip install coverage
coverage run manage.py test
coverage report
coverage html    # htmlcov/index.html 에서 시각적 확인
```

---

## 6. 의존성 관리

### 6.1 requirements.txt 구조

```
# Django 코어
Django==5.1.x
Pillow==10.x.x         이미지 처리

# 환경변수
python-decouple==3.x   .env 파일 읽기

# 배포 시 추가 (production only)
# gunicorn==21.x.x
# psycopg2-binary==2.x.x
```

### 6.2 패키지 관리 원칙

- 새 패키지 추가 시 반드시 `requirements.txt` 업데이트
- 버전은 `==` 핀닝 (보안 취약점 방지)
- 불필요한 패키지는 즉시 제거

---

## 7. 디버깅 가이드

### 7.1 자주 쓰는 명령어

```bash
python manage.py shell        Django Shell (대화형 DB 조회·테스트)
python manage.py dbshell      DB 직접 접근
python manage.py check        설정 오류 사전 검사
python manage.py collectstatic 정적 파일 수집 (배포 시)
```

### 7.2 자주 발생하는 오류 해결

```
TemplateDoesNotExist   → templates/ 경로 확인, TEMPLATES 설정 확인
NoReverseMatch         → URL 이름(app_name:name) 확인
PermissionDenied       → 권한 로직 확인
IntegrityError         → null=True/blank=True 또는 unique 제약 확인
ImproperlyConfigured   → settings.py 환경변수 누락 확인
```

---

## 8. 코드 생성 후 체크리스트 (AI용)

AI가 코드를 생성한 후 반드시 자가 검토하는 항목:

```
✅ 모든 쓰기 뷰에 인증·권한 검사가 있는가?
✅ 사용자 입력은 Form을 통해 검증되는가?
✅ migration 파일이 생성되었는가?
✅ URL이 urls.py에 등록되었는가?
✅ Admin에 새 Model이 등록되었는가?
✅ 성공·실패 시 messages가 표시되는가?
✅ 리다이렉트 경로가 올바른가?
✅ N+1 쿼리 문제가 없는가?
✅ 환경변수가 하드코딩되어 있지 않은가?
✅ 소프트 삭제 필터가 적용되었는가?
```
