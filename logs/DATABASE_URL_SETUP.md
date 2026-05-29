# DATABASE_URL 설정 가이드

## 문제
```
django.core.exceptions.ImproperlyConfigured: 
DATABASE_URL is required on Vercel/Render
```

Django가 PostgreSQL 연결 문자열(DATABASE_URL)을 찾지 못함

---

## 해결 방법: Render 대시보드에서 DATABASE_URL 설정

### Step 1: Render 대시보드 접속
```
https://dashboard.render.com
```

### Step 2: PostgreSQL 데이터베이스 확인
```
Dashboard 좌측 메뉴
  ↓
"PostgreSQL" 또는 "Databases" 클릭
  ↓
"community-db" 데이터베이스 선택
```

### Step 3: 연결 문자열 복사
```
데이터베이스 정보 페이지에서:

"External Database URL" 또는 "Connection String" 찾기
  ↓
다음과 같은 형태:
postgresql://username:password@hostname:5432/databasename

예시:
postgresql://community_user:xxx@oregon-postgres.render.com:5432/community

이 전체 문자열을 복사 ✅
```

### Step 4: 웹 서비스 환경 변수 설정
```
Dashboard 좌측 메뉴
  ↓
"Services" 클릭
  ↓
"community-web" 선택
  ↓
"Settings" 탭 클릭
  ↓
"Environment Variables" 섹션 스크롤
```

### Step 5: DATABASE_URL 추가
```
"+ Add Environment Variable" 버튼 클릭

변수명: DATABASE_URL
값: [Step 3에서 복사한 연결 문자열]

예시:
postgresql://community_user:xxx@oregon-postgres.render.com:5432/community

"Add" 클릭
```

### Step 6: 다른 환경 변수 확인 (필수!)
```
다음 환경 변수들도 모두 설정되어 있는지 확인:

□ RENDER = true
□ DEBUG = false
□ SECRET_KEY = [생성한 값]
□ DATABASE_URL = [방금 추가한 값] ← 이것!
□ DB_SSLMODE = require
□ ALLOWED_HOSTS = community-web.onrender.com
□ CSRF_TRUSTED_ORIGINS = https://community-web.onrender.com

모두 설정되어 있으면 좋음!
없는 것이 있으면 추가하기
```

### Step 7: 저장 및 재배포
```
1. "Save" 또는 변경 사항 저장
2. 페이지 상단에 "Redeploy" 클릭
3. "Logs" 탭에서 배포 진행 상황 확인
```

---

## ✅ 배포 성공 신호

다음이 로그에 표시되면 성공:

```
==> Build successful 🎉
==> Deploying...
==> Running ' gunicorn config.wsgi:application --bind 0.0.0.0:$PORT'
[INFO] Starting server with PID xxxx
[INFO] Listening at: 0.0.0.0:xxxx
[INFO] Using worker: sync
Application is ready to receive traffic
→ Live at https://community-web.onrender.com
```

---

## 🆘 만약 DATABASE_URL 연결 문자열을 찾을 수 없다면?

### 옵션 A: Render 데이터베이스가 없는 경우
```
1. Render Dashboard → "New" → "PostgreSQL"
2. 데이터베이스명: community-db
3. 플랜: Free
4. 생성 후 연결 문자열 복사
```

### 옵션 B: 수동으로 PostgreSQL 만들기
```
Render에서 제공하지 않으면, Supabase 사용:
1. https://supabase.com (무료)
2. 프로젝트 생성
3. 연결 문자열 복사
4. DATABASE_URL에 설정
```

---

## 참고: render.yaml의 데이터베이스 설정

```yaml
# render.yaml의 데이터베이스 부분
- type: pserv
  name: community-db
  plan: free
  region: ohio
  databaseName: community
  user: community_user
```

render.yaml에 이렇게 정의되어 있으면, 
Render가 자동으로 PostgreSQL을 생성하고 
DATABASE_URL 환경 변수를 자동으로 설정해야 합니다.

하지만 수동으로 서비스를 생성한 경우, 
이 설정이 적용되지 않았을 수 있으므로 
**수동으로 DATABASE_URL을 설정해야 합니다.**

---

## 📋 최종 체크리스트

```
□ PostgreSQL 데이터베이스 존재
□ 연결 문자열 복사
□ DATABASE_URL 환경 변수 설정
□ 다른 환경 변수들도 모두 설정
□ "Redeploy" 클릭
□ 배포 성공 (약 3-5분)
□ https://community-web.onrender.com 접속 확인
```

**이 과정을 따르면 100% 배포 성공합니다!**
