# Render 배포 체크리스트 (2026-05-29)

## ✅ 완료된 작업
1. ✅ Render 필수 패키지 설치
   - gunicorn
   - psycopg2-binary
   - dj-database-url
   - whitenoise

2. ✅ requirements.txt 업데이트
   - pip freeze로 모든 의존성 저장

3. ✅ settings.py 배포 환경 설정
   - SECRET_KEY: 환경 변수에서 읽음
   - DEBUG: RENDER 환경 변수로 자동 설정
   - ALLOWED_HOSTS: .onrender.com 포함
   - DATABASES: PostgreSQL 지원
   - MIDDLEWARE: WhiteNoiseMiddleware 추가
   - STATIC_ROOT / STATICFILES_STORAGE 설정

## ⚠️ 500 에러 원인 분석

### 가능한 원인들:
1. **DATABASE_URL 미설정**
   - Render 콘솔에서 PostgreSQL 데이터베이스 연결 필요
   - Environment Variables에 DATABASE_URL 설정 필수

2. **SECRET_KEY 미설정**
   - render.yaml에 기본값이 있지만, 프로덕션에서는 환경 변수 권장

3. **마이그레이션 미실행**
   - buildCommand에 `python manage.py migrate` 포함되어 있음
   - build 로그에서 실행 확인 필요

4. **create_admin 실패**
   - buildCommand에 `python manage.py create_admin` 포함
   - build 로그 확인

## 🔧 Render 배포 해결 단계

### 1단계: Render 환경 변수 확인
```
SERVICE NAME: community-web
ENVIRONMENT VARIABLES:
- RENDER: "true"
- DEBUG: "false"
- SECRET_KEY: [보안상 주의]
- DATABASE_URL: [PostgreSQL 연결 문자열]
- ALLOWED_HOSTS: "community-web.onrender.com"
- CSRF_TRUSTED_ORIGINS: "https://community-web.onrender.com"
- DB_SSLMODE: "require"
```

### 2단계: 배포 로그 확인
1. Render 콘솔 로그인
2. Service: community-web 선택
3. Logs 탭에서 build 및 deploy 로그 확인
4. 에러 메시지 확인

### 3단계: PostgreSQL 데이터베이스 확인
1. Database 생성 확인
2. DATABASE_URL 올바른지 확인
3. 데이터베이스 연결 테스트

### 4단계: 정적 파일 수집
- buildCommand에 `collectstatic` 포함
- STATIC_ROOT 설정 확인

## 📋 다음 액션 아이템
- [ ] Render 환경 변수 설정 확인
- [ ] 배포 로그 분석
- [ ] 데이터베이스 연결 상태 확인
- [ ] 마이그레이션 상태 확인
- [ ] 로그인/회원가입 테스트

## 현재 설정 상태
- render.yaml: ✅ 설정 완료
- settings.py: ✅ 배포 환경 맞춤 설정
- requirements.txt: ✅ 업데이트 완료
- 관리자 계정: ✅ 자동 생성 설정
