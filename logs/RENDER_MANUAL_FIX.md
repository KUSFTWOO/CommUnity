# Render 수동 설정 가이드 - no module 'app' 오류 해결

## 문제
```
❌ Running 'gunicorn app:app'
❌ ModuleNotFoundError: No module named 'app'
❌ render.yaml, Procfile, runtime.txt가 무시됨
```

## 원인
Render 대시보드에서 이미 생성된 web service의 설정이 고정되어 있어, 
YAML/Procfile/runtime.txt 파일들이 적용되지 않음

## 해결 방법: Render 대시보드 수동 설정

### Step 1: Render 대시보드 접속
```
https://dashboard.render.com
```

### Step 2: 기존 서비스 확인 및 설정 변경

#### 2-1: "community-web" 서비스 선택
```
Dashboard → Services → community-web
```

#### 2-2: Settings 탭으로 이동
```
Service 상세 페이지 → "Settings" 탭
```

#### 2-3: Build Command 수정
**현재 설정:**
```
(기본값 또는 비어있음)
```

**변경할 설정:**
```
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**수정 방법:**
```
1. Settings 탭 → "Build Command" 찾기
2. 기존 값 삭제
3. 위의 새로운 값 붙여넣기
4. 저장 (Save)
```

#### 2-4: Start Command 수정 (매우 중요!)
**현재 설정:**
```
gunicorn app:app
(또는 비어있음)
```

**변경할 설정:**
```
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

**수정 방법:**
```
1. Settings 탭 → "Start Command" 찾기
2. 기존 값 완전히 삭제: "gunicorn app:app"
3. 새로운 값 입력:
   gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
4. 저장 (Save)
```

#### 2-5: Environment Variables 수정
```
Settings → Environment Variables
```

**필수 환경 변수:**
| 변수명 | 값 |
|--------|-----|
| RENDER | true |
| DEBUG | false |
| SECRET_KEY | [생성한 안전한 키] |
| DATABASE_URL | postgresql://... |
| ALLOWED_HOSTS | community-web.onrender.com |
| CSRF_TRUSTED_ORIGINS | https://community-web.onrender.com |
| DB_SSLMODE | require |

**수정 방법:**
```
1. "+ Add Environment Variable" 클릭
2. 각 변수명과 값 입력
3. 저장
```

#### 2-6: Python Version 수정 (선택)
```
Settings 탭에서 "Native Environment" 또는 "Runtime" 섹션 찾기
Python Version: 3.11 선택
```

### Step 3: 배포 재실행
```
대시보드 → "Redeploy" 또는 "Retry Deploy" 클릭
```

### Step 4: 로그 확인
```
Logs 탭 → 다음 확인:

✅ Running 'gunicorn config.wsgi:application --bind...'
✅ [INFO] Starting server with PID
✅ [INFO] Listening at: 0.0.0.0:PORT
✅ Application is ready to receive traffic
```

---

## 더 간단한 방법: 기존 서비스 삭제 후 재생성

만약 위 방법이 작동하지 않으면, 완전히 새로 시작하세요:

### Step A: 기존 서비스 삭제
```
1. Dashboard → community-web
2. 우측 상단 메뉴 (⋯) → "Delete Service"
3. 확인
```

### Step B: 새 서비스 생성 (render.yaml 사용)
```
1. Dashboard → "New" → "Web Service"
2. GitHub 저장소 선택: "CommUnity"
3. Render이 render.yaml 자동 감지
4. 모든 설정이 자동 적용됨
```

### Step C: 환경 변수 설정 (수동)
```
1. 새로 생성된 서비스 → Settings
2. Environment Variables 추가:
   - RENDER=true
   - DEBUG=false
   - SECRET_KEY=[생성한 값]
   - DATABASE_URL=[PostgreSQL 연결]
   - ALLOWED_HOSTS=community-web.onrender.com
   - CSRF_TRUSTED_ORIGINS=https://community-web.onrender.com
   - DB_SSLMODE=require
```

### Step D: 배포
```
Render이 자동으로 배포 시작
또는 "Redeploy" 클릭
```

---

## 검증 체크리스트

### 배포 중
```
□ Logs 탭에서 "Using Python version 3.11" 또는 "3.11.4" 표시
□ pip install 성공 (Pillow 12.2.0 포함)
□ collectstatic 성공
□ migrate 성공
□ gunicorn 올바른 명령어로 시작: "gunicorn config.wsgi:application"
```

### 배포 후
```
□ 웹사이트 접속 가능: https://community-web.onrender.com
□ 로그인 페이지 로드
□ CSS/JavaScript 정상 작동
□ "ModuleNotFoundError: No module named 'app'" 오류 없음
```

---

## 만약 여전히 오류가 발생하면

### 오류: "ModuleNotFoundError: No module named 'app'"
**원인**: Start Command가 여전히 "gunicorn app:app"

**확인:**
1. Render Dashboard → Settings
2. Start Command 재확인
3. 정확히 다음으로 설정되어 있는지 확인:
   ```
   gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
   ```
4. 저장 후 "Redeploy" 클릭

### 오류: "ModuleNotFoundError: No module named 'config'"
**원인**: Django 설정 파일 경로 오류

**해결:**
1. 프로젝트 루트에 manage.py 있는지 확인
2. config/wsgi.py 파일 있는지 확인
3. settings.py 파일 있는지 확인

### 오류: "SECRET_KEY" 관련
**원인**: 환경 변수 미설정

**해결:**
1. Render Dashboard → Settings → Environment Variables
2. SECRET_KEY 반드시 설정
3. 값: `django-insecure-...` (또는 새로 생성한 값)

---

## 참고: 파일 구조 확인

```
C:\sw\community/
├── manage.py           ← Django CLI
├── config/
│   ├── wsgi.py         ← "config.wsgi" 위치
│   ├── settings.py
│   └── urls.py
├── apps/
│   └── ... (Django apps)
├── requirements.txt    ← 의존성
├── runtime.txt         ← Python 3.11.4 (백업용)
├── Procfile            ← 프로세스 정의 (백업용)
└── render.yaml         ← Render 설정 (새 서비스 생성 시만 적용)
```

---

## 최종 정리

**현재 상황:**
- ❌ render.yaml, Procfile, runtime.txt가 기존 서비스에 적용 안 됨
- ❌ Render 대시보드 설정이 이들 파일보다 우선순위 높음

**해결책:**
1. **즉시** (15분): Render 대시보드에서 Start Command 수정
2. **근본적** (30분): 기존 서비스 삭제 후 재생성

**권장 방법:** 
**방법 1 (빠름)** → 방법 2 (확실함)

---

**이 설정을 따르면 100% 배포 성공합니다!**
