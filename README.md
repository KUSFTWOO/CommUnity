# CommUnity — 커뮤니티 웹사이트

> **"복잡하지 않게, 하지만 충분하게"**
> 소규모 커뮤니티가 필요로 하는 모든 것을 하나의 플랫폼에서.

---

## 📌 프로젝트 비전

CommUnity는 소규모 그룹이 온라인에서 **공지를 전달하고, 자유롭게 소통하며,
일정을 공유하고, 의견을 모을 수 있는** 올인원 커뮤니티 플랫폼입니다.

기술적 복잡도는 최소화하되, 실제로 필요한 기능은 견고하게 구현합니다.
바이브코딩(Vibe Coding) 방식으로 AI가 리딩하며 단계적으로 구축합니다.

---

## 🗂️ 주요 기능 현황

| 기능 | 설명 | 상태 |
|------|------|------|
| 📢 공지사항 | 관리자 공지, 핀 고정, 파일 첨부 | 🔲 미개발 |
| 💬 자유게시판 | 게시글·댓글·대댓글·좋아요·이미지 업로드 | 🔲 미개발 |
| 📅 캘린더 | 월별 일정 뷰, 일정 생성·관리 | 🔲 미개발 |
| 🗳️ 투표/설문 | 단일/복수 선택, 익명 투표, 결과 시각화 | 🔲 미개발 |
| 👤 회원 시스템 | 가입·로그인·세션·프로필 | 🔲 미개발 |
| 🛠️ 관리자 대시보드 | 회원 관리, 게시글 통제, 지표 확인 | 🔲 미개발 |

---

## 🏗️ 기술 스택

```
Backend    Django 5.x (Python 3.11+)
Frontend   Django Templates + Tailwind CSS (CDN)
Database   SQLite (개발) → PostgreSQL (프로덕션)
Auth       django.contrib.auth (내장)
Admin      django.contrib.admin (내장) + 커스텀 뷰
Image      Pillow (리사이즈·검증)
Deploy     gunicorn + nginx (예정)
```

### 왜 이 스택인가?

| 선택 | 이유 |
|------|------|
| **Django Monolith** | 백엔드·프론트가 분리되지 않아 AI 바이브코딩 시 컨텍스트 분산 없음 |
| **내장 Admin** | 관리자 대시보드를 별도 구현 없이 즉시 사용 가능 |
| **내장 Auth** | 로그인·세션·권한 시스템이 검증된 형태로 내장 |
| **SQLite** | 초기 개발에 서버 설정 없이 바로 사용, 추후 PostgreSQL 전환 용이 |
| **Tailwind CDN** | 빌드 도구 없이 클래스 기반으로 빠른 UI 구성 |
| **Next.js 미선택** | 상태 관리 복잡도·분리된 API 레이어가 바이브코딩에 불리 |

---

## 📁 프로젝트 구조

```
community/                          ← Django 프로젝트 루트
├── manage.py
├── requirements.txt
├── .env                            ← 환경변수 (git 제외)
├── db.sqlite3                      ← 개발용 DB (git 제외)
│
├── config/                         ← 프로젝트 설정
│   ├── settings/
│   │   ├── base.py                 ← 공통 설정
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py                     ← 루트 URL 라우터
│   └── wsgi.py
│
├── apps/                           ← 기능별 Django App
│   ├── accounts/                   ← 회원 시스템
│   ├── notices/                    ← 공지사항
│   ├── board/                      ← 자유게시판
│   ├── calendar_app/               ← 일정 관리
│   ├── votes/                      ← 투표/설문
│   └── dashboard/                  ← 관리자 대시보드
│
├── templates/                      ← 공통 템플릿
│   ├── base.html                   ← 전체 레이아웃
│   ├── navbar.html
│   └── footer.html
│
├── static/                         ← 정적 파일 (CSS, JS, 이미지)
└── media/                          ← 업로드 파일 (git 제외)
    ├── profiles/
    ├── posts/
    └── notices/
```

---

## 🔄 URL 구조

```
/                        메인 페이지 (공지 + 최근 게시글)
/accounts/signup/        회원가입
/accounts/login/         로그인
/accounts/logout/        로그아웃
/accounts/profile/       내 프로필

/notices/                공지사항 목록
/notices/<id>/           공지사항 상세

/board/                  게시판 목록
/board/new/              글쓰기
/board/<id>/             게시글 상세
/board/<id>/edit/        게시글 수정

/calendar/               캘린더 뷰
/votes/                  투표 목록
/votes/<id>/             투표 참여

/admin/                  Django 내장 Admin
/dashboard/              커스텀 관리자 대시보드
```

---

## 🚀 로컬 개발 환경 시작

```bash
# 1. 저장소 클론
git clone <repo-url>
cd community

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 환경변수 설정
cp .env.example .env
# .env 파일에서 SECRET_KEY 등 설정

# 5. DB 마이그레이션
python manage.py migrate

# 6. 관리자 계정 생성
python manage.py createsuperuser

# 7. 개발 서버 실행
python manage.py runserver
# → http://localhost:8000
```

---

## 📊 현재 개발 진행도

```
Phase 1  환경 세팅 + 인증       ░░░░░░░░░░  0%
Phase 2  공지사항 + 게시판       ░░░░░░░░░░  0%
Phase 3  댓글 + 좋아요           ░░░░░░░░░░  0%
Phase 4  캘린더 + 투표           ░░░░░░░░░░  0%
Phase 5  관리자 대시보드         ░░░░░░░░░░  0%
Phase 6  보안 + 배포             ░░░░░░░░░░  0%

전체 진행도                      ░░░░░░░░░░  0%  (초기 설계 단계)
```

---

## 👥 개발 방식 — 바이브코딩 (Vibe Coding)

이 프로젝트는 **바이브코딩** 방식으로 진행됩니다.

- 코딩 지식 없이 AI(Claude)가 코드 작성을 전담
- 사용자는 방향과 요구사항을 제시
- AI는 단계별로 코드 생성·설명·검증을 수행
- 문서(PRD, TCD, DP 등)가 AI의 판단 기준이 됨

---

## 📝 라이선스

MIT License — 자유롭게 사용·수정·배포 가능
