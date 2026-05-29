# SA — System Architecture
## 전체 시스템 구조와 데이터 플로우

> 버전: 1.0.0

---

## 1. 아키텍처 개요

CommUnity는 **Django Monolith** 아키텍처를 채택합니다.
프론트엔드·백엔드가 분리되지 않고 Django 서버 하나에서 모든 것을 처리합니다.

```
┌──────────────────────────────────────────────────────────┐
│                  클라이언트 (브라우저)                     │
│           HTML + Tailwind CSS + Vanilla JS               │
└───────────────────────┬──────────────────────────────────┘
                        │  HTTP 요청 (GET / POST)
                        ▼
┌──────────────────────────────────────────────────────────┐
│                 Django 애플리케이션 서버                   │
│                                                          │
│  ┌───────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ accounts  │ │  board   │ │ notices  │ │  votes   │  │
│  └───────────┘ └──────────┘ └──────────┘ └──────────┘  │
│  ┌──────────────────────┐  ┌──────────────────────────┐  │
│  │    calendar_app      │  │       dashboard          │  │
│  └──────────────────────┘  └──────────────────────────┘  │
│                                                          │
│               Django ORM (DB 추상화 레이어)               │
└───────────────────────┬──────────────────────────────────┘
                        │
            ┌───────────┴──────────┐
            ▼                      ▼
┌─────────────────┐     ┌──────────────────────────────┐
│  SQLite (개발)  │     │   로컬 파일시스템 (media/)    │
│  PostgreSQL(운영)│     │   → 추후 AWS S3 전환 가능    │
└─────────────────┘     └──────────────────────────────┘
```

---

## 2. 요청-응답 데이터 플로우

### 2.1 일반 페이지 요청 (GET)

```
브라우저  GET /board/
    │
    ▼
config/urls.py                    루트 URL 라우터
    │  path('board/', include('apps.board.urls'))
    ▼
apps/board/urls.py                App URL 매칭
    │  path('', views.post_list, name='list')
    ▼
apps/board/views.py               비즈니스 로직
    │  1. 인증 확인 (@login_required)
    │  2. DB 쿼리 실행
    │  3. 컨텍스트 딕셔너리 구성
    ▼
apps/board/templates/board/list.html   HTML 렌더링
    │  {{ posts }}, {% for %} 등 템플릿 태그 처리
    ▼
브라우저                          완성된 HTML 응답 수신
```

### 2.2 폼 제출 (POST)

```
브라우저  POST /board/new/
    │
    ▼
Django Middleware
    │  ✅ CSRF 토큰 검증
    │  ✅ 세션 확인 (로그인 여부)
    ▼
views.post_create()
    │  1. request.method == 'POST' 확인
    │  2. PostForm(request.POST, request.FILES) 생성
    │  3. form.is_valid() 호출
    │       ├── 성공: post.save() → messages → redirect()
    │       └── 실패: 오류와 함께 폼 재렌더링 (200)
    ▼
DB 저장 또는 오류 응답
```

### 2.3 이미지 업로드 플로우

```
브라우저  파일 선택 → POST 전송
    │
    ▼
Form 유효성 검사
    │  ✅ 확장자 검증 (jpg, png, gif, webp)
    │  ✅ MIME 타입 검증 (확장자 위변조 방지)
    │  ✅ 파일 크기 검증 (≤ 5MB)
    │  ✅ 파일 개수 검증 (≤ 5장)
    ▼
Pillow 처리
    │  - 이미지 리사이즈 (max 1200px)
    │  - EXIF 메타데이터 제거 (개인정보 보호)
    ▼
파일 저장
    media/posts/YYYY/MM/DD/파일명.jpg
    ▼
DB에 파일 경로 저장
    PostImage.image = 'posts/2025/05/15/파일명.jpg'
```

---

## 3. 인증 흐름

### 3.1 로그인 세션 관리

```
POST /accounts/login/
    │
    ▼
django.contrib.auth.authenticate()
    │  이메일 → CustomUser 조회
    │  입력 비밀번호 bcrypt 해싱 비교
    ├── 실패 → 오류 메시지 + 실패 횟수 기록
    └── 성공 ▼
              │
              ▼
           login(request, user)
              │  Session ID 생성 → HttpOnly 쿠키 설정
              │  세션 데이터 DB 저장 (django_session 테이블)
              ▼
           로그인 완료
           (이후 모든 요청에 쿠키 자동 첨부)
```

### 3.2 권한 계층

```
비회원          공지사항·게시글 읽기만 가능
회원            게시글·댓글 작성, 좋아요, 투표 참여
관리자(staff)   공지 작성·삭제, 일정 관리, 투표 생성, 대시보드 접근
슈퍼관리자      Django Admin 전체 접근 권한
```

---

## 4. 레이어 책임 분리

```
┌─────────────────────────────────────────────────┐
│  Templates  (View Layer)                        │
│  HTML 렌더링만 담당                              │
│  비즈니스 로직 없음 (조건 분기 최소화)            │
│  Tailwind CSS 스타일링                          │
└────────────────────┬────────────────────────────┘
                     │ 컨텍스트 데이터 전달
┌────────────────────▼────────────────────────────┐
│  Views  (Controller Layer)                      │
│  HTTP 요청·응답 처리                             │
│  인증·권한 검사                                  │
│  Form 유효성 검사 위임                           │
│  Model 메서드 호출                               │
│  가능한 한 얇게(thin) 유지                       │
└────────────────────┬────────────────────────────┘
                     │ 비즈니스 로직 호출
┌────────────────────▼────────────────────────────┐
│  Models  (Business Logic Layer)                 │
│  데이터 구조 정의                                │
│  비즈니스 로직 메서드 (Fat Model)               │
│  DB 제약 조건 및 인덱스                          │
│  소프트 삭제, 조회수 증가 등                     │
└────────────────────┬────────────────────────────┘
                     │ ORM 쿼리
┌────────────────────▼────────────────────────────┐
│  Database  (SQLite / PostgreSQL)                │
│  데이터 영속성                                   │
│  인덱스로 쿼리 성능 최적화                       │
└─────────────────────────────────────────────────┘
```

---

## 5. 배포 아키텍처 (프로덕션)

```
인터넷
    │  HTTPS (443)
    ▼
[Nginx]                리버스 프록시, SSL 종료, 정적 파일 서빙
    │
    ├── /static/  →  로컬 파일 직접 서빙 (빠름)
    ├── /media/   →  로컬 파일 직접 서빙
    │
    └── /         →  [Gunicorn]  WSGI 서버 (Django 앱 실행)
                          │
                          └── Django Application
```

### Nginx 핵심 설정 예시

```nginx
server {
    listen 443 ssl;
    server_name example.com;

    location /static/ { alias /srv/community/staticfiles/; }
    location /media/  { alias /srv/community/media/; }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 6. 보안 아키텍처

```
레이어          보안 조치
──────────────────────────────────────────────
네트워크        HTTPS 필수 (Let's Encrypt SSL)
Django          CSRF 미들웨어, 세션 관리
인증            bcrypt 해싱, 로그인 실패 제한 (5회/30분)
권한            @login_required, is_staff 검사
입력            Django Form 유효성 검사
파일            확장자 + MIME 타입 이중 검증, Pillow 재처리
DB              ORM으로 SQL Injection 완전 방어
템플릿          Django 자동 XSS 이스케이프
환경변수        .env 파일로 비밀키 분리
```

---

## 7. 확장 경로

```
현재 (v1.0)                     미래 (v2.0+)
──────────────────────────────────────────────────
SQLite              →  PostgreSQL
로컬 파일 저장       →  AWS S3
이메일 없음          →  SMTP (Gmail/SendGrid)
단일 서버            →  Docker 컨테이너
수동 배포            →  GitHub Actions CI/CD
소셜 로그인 없음     →  Google/Kakao OAuth (django-allauth)
실시간 없음          →  Django Channels (WebSocket)
```
