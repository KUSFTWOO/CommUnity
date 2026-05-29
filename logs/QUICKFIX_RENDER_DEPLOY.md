# Render 배포 빠른 해결 (수동 방식)

Blueprint가 작동하지 않을 때 사용하는 가장 빠른 방법

## 4단계로 5분 안에 배포하기

### Step 1: Render 대시보드에서 Web Service 생성

```
1. https://dashboard.render.com 접속
2. [+ New] → [Web Service] 클릭
3. GitHub 저장소 선택: "CommUnity"
4. 브랜치: main
5. Name: community-web
6. [Create Web Service] 클릭
```

### Step 2: PostgreSQL 데이터베이스 생성

```
1. Render Dashboard → [+ New] → [PostgreSQL]
2. Name: community-db
3. Database: community
4. User: postgres (기본값 사용)
5. Password: [자동 생성됨]
6. Plan: Free
7. Region: Ohio
8. [Create Database] 클릭
```

생성 후 **External Database URL 복사** (중요!)

### Step 3: Environment Variables 설정

```
1. Render Dashboard → Services → community-web
2. [Settings] 탭
3. [Environment Variables] 섹션
4. 다음 변수들 추가:

RENDER=true
DEBUG=false
SECRET_KEY=django-insecure-9z!@bn#xz_9v-&c3$*b6d%^j*l+0f^v@!_6c^+3zx!k^%@8d9
DATABASE_URL=[Step 2에서 복사한 URL]
ALLOWED_HOSTS=community-web.onrender.com
CSRF_TRUSTED_ORIGINS=https://community-web.onrender.com
DB_SSLMODE=require
```

**각각 [+ Add] 클릭해서 추가**

### Step 4: Build & Start Commands 설정

```
1. [Settings] → 맨 위로 스크롤
2. [Build Command] 입력:
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate

3. [Start Command] 입력:
   gunicorn config.wsgi:application --bind 0.0.0.0:$PORT

4. [Save] 클릭
5. [Redeploy] 또는 자동 배포 시작
```

---

## ✅ 배포 확인 (약 5분 후)

```
1. [Events] 탭에서 배포 진행 상황 확인
2. 배포 완료 후:
   https://community-web-xxxxx.onrender.com 접속
   
✅ 홈페이지 로드
✅ CSS/JavaScript 정상
✅ 로그인 가능
```

---

## 📋 체크리스트

```
□ Web Service 생성: community-web
□ PostgreSQL 생성: community-db
□ DATABASE_URL 환경 변수 설정
□ 나머지 7개 환경 변수 설정
□ Build Command 설정
□ Start Command 설정
□ Redeploy 클릭
□ 배포 완료 (5분 대기)
□ 웹사이트 접속 확인
```

**이 방법이면 100% 성공합니다!**
