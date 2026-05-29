# Render 배포 가이드 및 체크리스트

## 배포 준비 상태 ✅

**GitHub 푸시 완료:**
- ✅ 커밋 ID: 5f6e652
- ✅ 모든 파일 push 완료
- ✅ render.yaml 파일 포함됨
- ✅ settings.py 배포 환경 설정 포함
- ✅ requirements.txt 포함

**필요한 구성 요소:**
- ✅ render.yaml (인프라 정의)
- ✅ requirements.txt (Python 의존성)
- ✅ config/settings.py (환경 변수 대응)
- ✅ manage.py (Django CLI)
- ✅ config/wsgi.py (WSGI 애플리케이션)

---

## Render 배포 단계별 가이드

### 1단계: Render 계정 및 GitHub 연동

#### 1-1. Render 대시보드 접속
```
https://dashboard.render.com
```

#### 1-2. GitHub 인증 (첫 사용자)
```
1. "Connect with GitHub" 버튼 클릭
2. GitHub 계정 인증
3. Render에 저장소 접근 권한 부여
```

#### 1-3. 기존 Render 사용자인 경우
```
1. 대시보드 로그인
2. 좌측 메뉴 "New" → "Web Service" 클릭
```

---

### 2단계: render.yaml로 자동 배포 설정

#### 2-1. Web Service 생성 (자동)
```
Render이 GitHub의 render.yaml 자동 감지
  ↓
다음 정보가 자동으로 설정됨:
  - 서비스명: community-web
  - 런타임: Python 3.11
  - 빌드 명령어
  - 시작 명령어
  - 환경 변수 일부
```

#### 2-2 수동으로 배포하는 경우 (render.yaml 미지원)
```
1. "Connect Repository" 버튼 클릭
2. GitHub 저장소 선택: "CommUnity"
3. 브랜치: main
4. 환경: Python 3.11
5. "Build Command" 입력:
   pip install -r requirements.txt
   python manage.py collectstatic --noinput
   python manage.py migrate

6. "Start Command" 입력:
   gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

---

### 3단계: PostgreSQL 데이터베이스 생성 (옵션)

#### 3-1. render.yaml로 자동 생성되는 경우
```
Render이 다음 자동 생성:
  - 데이터베이스명: community-db
  - 타입: PostgreSQL
  - 플랜: Free
  - 사용자: community_user
```

#### 3-2. 수동으로 생성하는 경우
```
1. 대시보드 좌측 메뉴 "New" → "PostgreSQL" 클릭
2. 데이터베이스명: community-db
3. 플랜: Free
4. 지역: Ohio (또는 가까운 지역)
5. "Create Database" 클릭
6. 자동 생성되는 connectionString 복사 (DATABASE_URL로 사용)
```

---

### 4단계: 환경 변수 설정

#### 4-1. Render 대시보드에서 환경 변수 설정
```
Web Service 생성 후 → Settings 탭 → Environment Variables
```

#### 4-2. 설정할 환경 변수

| 변수명 | 값 | 설명 |
|--------|-----|------|
| **RENDER** | true | Render 환경 감지 |
| **DEBUG** | false | 운영 환경 모드 |
| **SECRET_KEY** | [생성된 값] | Django 시크릿 키 (필수 변경) |
| **DATABASE_URL** | [자동 또는 수동] | PostgreSQL 연결 문자열 |
| **ALLOWED_HOSTS** | community-web.onrender.com | 도메인 (자동 설정됨) |
| **CSRF_TRUSTED_ORIGINS** | https://community-web.onrender.com | CSRF 보호 |
| **DB_SSLMODE** | require | PostgreSQL SSL 필수 |

#### 4-3. SECRET_KEY 생성

**방법 1: Django에서 생성**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**방법 2: 온라인 생성기**
```
https://djecrety.ir/
```

**생성 예시:**
```
django-insecure-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

#### 4-4. DATABASE_URL 값

render.yaml로 자동 생성되는 경우:
```
postgresql://[username]:[password]@[host]:[port]/[databasename]

예시:
postgresql://community_user:xxxxxxxxxxxx@oregon-postgres.render.com:5432/community
```

수동으로 설정하는 경우:
```
1. PostgreSQL 데이터베이스 생성 후
2. 데이터베이스 정보 페이지에서 "External Database URL" 복사
3. Render 환경 변수에 설정
```

---

### 5단계: 배포 실행

#### 5-1. 자동 배포 (권장)
```
GitHub에 push된 후 자동으로 배포 시작
  ↓
"Builds" 탭에서 빌드 로그 확인
  ↓
완료 시 "https://community-web.onrender.com" URL 생성
```

#### 5-2. 수동 배포
```
대시보드 → Web Service → "Manual Deploy" → "Latest Commit" 선택
```

---

## 배포 중 발생 가능한 오류 및 해결

### 오류 1: "MODULE_NOT_FOUND: django"
**원인:** requirements.txt가 없거나 경로 오류

**해결:**
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add requirements.txt"
git push origin main
```

### 오류 2: "No such table: auth_user"
**원인:** 데이터베이스 마이그레이션 미실행

**해결:** Build Command 확인
```
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate  ← 반드시 포함
```

### 오류 3: "DEBUG=True 에러 또는 정적 파일 미로드"
**원인:** SECRET_KEY 또는 ALLOWED_HOSTS 미설정

**해결:**
```
환경 변수 설정 재확인:
- SECRET_KEY: 반드시 설정
- ALLOWED_HOSTS: community-web.onrender.com
- DEBUG: false
```

### 오류 4: "STATIC_ROOT 또는 STATICFILES 오류"
**원인:** WhiteNoise 설정 오류

**해결:** settings.py 확인
```python
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

### 오류 5: "DATABASE_URL 파싱 오류"
**원인:** 데이터베이스 연결 문자열 형식 오류

**해결:** DATABASE_URL 형식 확인
```
✅ 올바른 형식:
postgresql://user:password@host:5432/dbname

❌ 잘못된 형식:
postgres://...  (deprecated)
mysql://...     (지원 안 함)
```

---

## 배포 후 검증 체크리스트

### 1. 웹 서비스 상태 확인
```
✅ 서비스 상태: "Live"
✅ 로그에 오류 없음
✅ 응답 시간: <500ms
```

### 2. 데이터베이스 연결 확인
```
✅ DATABASE_URL 환경 변수 설정됨
✅ PostgreSQL 연결 가능 (SSL)
✅ 마이그레이션 완료 (테이블 생성됨)
```

### 3. 정적 파일 확인
```
✅ CSS/JS 파일 로드됨
✅ 이미지 표시됨
✅ WhiteNoise 미들웨어 작동 중
```

### 4. 애플리케이션 기능 테스트
```
✅ 홈페이지 접속 가능
✅ 로그인 페이지 접속 가능
✅ 대시보드 접속 가능 (로그인 후)
✅ 게시글 작성/조회 가능
✅ 프로필 통계 정상 표시
```

### 5. 보안 검증
```
✅ HTTPS 사용 중 (자동)
✅ CSRF 보호 활성화
✅ 보안 헤더 설정됨 (Render 기본)
```

---

## 배포 후 성능 모니터링

### Render 대시보드 확인
```
1. Metrics 탭
   - CPU 사용률: 정상 (10-30%)
   - 메모리: 정상 (100-200MB)
   - 응답 시간: <500ms

2. Logs 탭
   - 에러 메시지 없음
   - 정상 요청 처리 중

3. Events 탭
   - 배포 기록
   - 오류 이벤트 모니터링
```

---

## 커스텀 도메인 연결 (선택)

### 1. 도메인 구입
```
Namecheap, GoDaddy, Google Domains 등에서 구입
예시: community-app.com
```

### 2. Render 대시보드 설정
```
1. Web Service → Custom Domain
2. 도메인 입력: community-app.com
3. "Add Domain" 클릭
4. DNS 레코드 설정 가이드 표시
```

### 3. DNS 레코드 설정
```
도메인 DNS 관리 페이지에서:

1. CNAME 레코드 추가:
   Name: @
   Value: community-web.onrender.com

2. 또는 A 레코드:
   Name: @
   Value: Render이 제공하는 IP
```

### 4. SSL 인증서 (자동)
```
Render이 Let's Encrypt로 자동 발급
배포 후 ~5분 내 https 사용 가능
```

---

## 트러블슈팅 팁

### 배포 시간 확인
```
초기 배포: 3-5분 (의존성 설치 + 마이그레이션)
이후 배포: 1-2분 (캐시됨)
```

### 로그 확인
```
1. Render 대시보드 → Logs 탭
2. 최근 배포 로그 확인
3. 빌드 단계별 에러 메시지 확인

예시:
[OK] Starting build...
[OK] Installing requirements...
[OK] Collecting static files...
[OK] Running migrations...
[OK] Build complete!
```

### 재배포
```
1. GitHub에 새 커밋 push
2. Render이 자동으로 감지 및 배포
   또는
3. Render 대시보드 → Manual Deploy → "Latest Commit"
```

### 환경 변수 변경 후
```
환경 변수 변경 → "Restart Services" 필수
(자동 배포되지 않음)
```

---

## 배포 후 다음 단계

### 1. 정상 작동 확인 (1시간)
```
- 웹페이지 로드 확인
- 기본 기능 테스트
- 에러 로그 모니터링
```

### 2. 성능 모니터링 (1일)
```
- Render 메트릭 확인
- 응답 시간 확인
- 리소스 사용률 확인
```

### 3. 사용자 반응 수집
```
- 버그 리포트 수집
- 성능 피드백
- UX 개선 사항
```

### 4. 향후 개선사항
```
Phase 2:
- 캐싱 (Redis) 추가
- CDN (이미지 최적화)
- 모니터링 (Sentry, New Relic)

Phase 3:
- 이메일 알림
- 파일 업로드
- 검색 최적화
```

---

## 빠른 참조

| 항목 | 값 |
|------|-----|
| 배포 플랫폼 | Render |
| Git 저장소 | https://github.com/KUSFTWOO/CommUnity |
| Git 브랜치 | main |
| 마지막 커밋 | 5f6e652 |
| 런타임 | Python 3.11 |
| 데이터베이스 | PostgreSQL Free |
| WSGI 서버 | Gunicorn |
| 정적 파일 | WhiteNoise |
| 도메인 | *.onrender.com (자동) |
| SSL | Let's Encrypt (자동) |

---

## 배포 완료 후 최종 확인

```
✅ 배포 완료
✅ 웹 서비스 Live
✅ 데이터베이스 연결
✅ 정적 파일 로드
✅ 기본 기능 작동
✅ HTTPS 활성화
✅ 모니터링 시작
✅ 에러 로깅 설정

→ 프로덕션 배포 완료!
```

---

**작업 날짜**: 2026-05-29
**상태**: 배포 가이드 완성
**다음 단계**: Render 대시보드에서 실제 배포 실행
