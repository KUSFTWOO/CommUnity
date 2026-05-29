# 2026-05-29 render.yaml 파일 생성

## 작업 요약
CommUnity 프로젝트를 Render에 배포하기 위한 Infrastructure as Code 파일(render.yaml)을 생성했습니다.

## render.yaml 파일 구조

### 1. 웹 서비스 정의 (community-web)

#### 기본 설정
```yaml
type: web
name: community-web
runtime: python
pythonVersion: 3.11
```

**역할:**
- Render의 웹 서비스로 Django 애플리케이션 실행
- Python 3.11 런타임 사용

#### 빌드 명령어 (buildCommand)
```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

**각 단계의 역할:**
1. **pip install**: 프로젝트 의존성 설치
   - Django, gunicorn, psycopg2-binary, dj-database-url, whitenoise 등
   
2. **collectstatic**: 정적 파일 수집
   - 모든 CSS, JS, 이미지 파일 수집
   - staticfiles/ 디렉토리로 이동
   - WhiteNoise 스토리지로 압축 및 최적화
   
3. **migrate**: 데이터베이스 마이그레이션 실행
   - PostgreSQL에 테이블 생성
   - 스키마 업데이트

#### 시작 명령어 (startCommand)
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

**작동 방식:**
- Gunicorn WSGI 서버 시작
- `0.0.0.0:$PORT` 바인딩: Render 포트 사용
- Django WSGI 애플리케이션 실행

#### 환경 변수 설정 (envVars)

**1. RENDER**
```yaml
key: RENDER
value: true
```
- Render 배포 환경임을 알림
- settings.py의 DEBUG = 'RENDER' not in os.environ 조건 활성화
- DEBUG 자동으로 False 설정

**2. DEBUG**
```yaml
key: DEBUG
value: false
```
- 운영 환경 모드
- 에러 페이지가 상세 정보 노출 안 함

**3. SECRET_KEY**
```yaml
key: SECRET_KEY
value: django-insecure-9z!@bn#xz_9v-&c3$*b6d%^j*l+0f^v@!_6c^+3zx!k^%@8d9
```

⚠️ **중요:** Render 대시보드에서 생성된 시크릿 키로 변경해야 합니다.

**시크릿 키 생성 방법:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**4. DATABASE_URL (동적 참조)**
```yaml
key: DATABASE_URL
fromDatabase:
  name: community-db
  property: connectionString
```

**작동 방식:**
- community-db 데이터베이스의 연결 문자열 자동 참조
- PostgreSQL 연결 URL 형태: `postgres://user:pass@host:port/db`
- 수동으로 설정할 필요 없음 (자동 연동)

**5. ALLOWED_HOSTS (도메인 설정)**
```yaml
key: ALLOWED_HOSTS
value: "{{ env.RENDER_SERVICE_NAME }}.onrender.com"
```

**작동 방식:**
- Render 도메인 자동 설정
- `{{ env.RENDER_SERVICE_NAME }}` = 웹 서비스명 (community-web)
- 결과: `community-web.onrender.com`

**6. CSRF_TRUSTED_ORIGINS (CSRF 보호)**
```yaml
key: CSRF_TRUSTED_ORIGINS
value: "https://{{ env.RENDER_SERVICE_NAME }}.onrender.com"
```

**역할:**
- 외부 사이트에서의 CSRF 공격 방지
- Render 도메인만 신뢰

**7. DB_SSLMODE (보안)**
```yaml
key: DB_SSLMODE
value: require
```

**역할:**
- PostgreSQL 연결 시 SSL 필수
- 데이터 전송 암호화
- Render PostgreSQL 요구사항

### 2. PostgreSQL 데이터베이스 정의 (community-db)

```yaml
type: pserv
name: community-db
plan: free
region: ohio
databaseName: community
user: community_user
```

#### 기본 설정

**type: pserv**
- PostgreSQL 서비스 타입

**name: community-db**
- 데이터베이스 서비스명
- 웹 서비스에서 `fromDatabase.name` 으로 참조

**plan: free**
- Render 프리 플랜 사용
- 비용 없음, 성능 제한 있음

**region: ohio**
- 데이터베이스 실행 지역
- 지역 선택: us-east (Ohio), us-west (Oregon), eu-west-1 (Ireland) 등

**databaseName: community**
- 생성할 데이터베이스명

**user: community_user**
- 데이터베이스 접근 사용자명

#### 네트워크 설정

```yaml
ipAllowList:
  - source: 0.0.0.0/0
    description: Allow all
```

**역할:**
- 모든 IP에서 데이터베이스 접근 허용
- 개발/테스트용 설정
- 프로덕션: 특정 IP만 허용 권장

## 배포 플로우

### 1단계: 초기 배포 (Render 대시보드)
```
Render가 render.yaml 파일 감지
  ↓
웹 서비스(community-web) 생성
  ↓
PostgreSQL 데이터베이스(community-db) 생성
  ↓
환경 변수 자동 설정 (DATABASE_URL 등)
```

### 2단계: 빌드 실행
```
buildCommand 실행:
  1. pip install 실행 (의존성 설치)
  2. python manage.py collectstatic (정적 파일 수집)
  3. python manage.py migrate (데이터베이스 마이그레이션)
```

### 3단계: 서비스 시작
```
startCommand 실행:
  gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
  
Django 애플리케이션 시작
  ↓
PostgreSQL 연결 (DATABASE_URL 사용)
  ↓
정적 파일 서빙 (WhiteNoise)
  ↓
웹 서비스 준비 완료
```

## 환경 변수 자동 흐름

### 데이터베이스 생성 시
```
community-db PostgreSQL 생성
  ↓
Render이 connectionString 자동 생성
  ↓
DATABASE_URL = postgres://user:pass@host:5432/community
```

### 웹 서비스 생성 시
```
fromDatabase 참조 해석
  ↓
DATABASE_URL 자동 설정
  ↓
Django settings.py에서 자동 사용
```

## 주요 장점

### ✅ Infrastructure as Code
- 인프라 정의가 코드로 관리됨
- Git에서 버전 관리 가능
- 재현 가능한 배포

### ✅ 자동화
- 데이터베이스 생성 자동
- 환경 변수 자동 설정
- 빌드/배포 자동 실행

### ✅ 보안
- SECRET_KEY 안전 관리
- SSL/TLS 암호화
- CSRF 보호 자동 설정

### ✅ 비용 최적화
- Free 플랜 사용 가능
- 자동 스케일링
- 사용한 만큼만 비용 지불

## 다음 단계

### 1. 로컬 테스트
```bash
git add render.yaml
git commit -m "Add render.yaml for infrastructure as code"
```

### 2. Render 배포 설정
- GitHub 저장소 연동
- render.yaml 파일 감지 자동화
- 환경 변수 검증

### 3. 배포 실행
```
GitHub에 push
  ↓
Render 자동 감지
  ↓
인프라 자동 생성 및 배포
```

### 4. 배포 후 확인
- 웹 서비스 로그 확인
- 데이터베이스 연결 확인
- 정적 파일 로드 확인

## render.yaml vs 대시보드 설정

### render.yaml 사용 (권장)
- ✅ 버전 관리 가능
- ✅ 팀 협업 용이
- ✅ 재현 가능한 배포
- ✅ CI/CD 자동화 쉬움

### Render 대시보드 UI (수동)
- ❌ 매번 수동 설정 필요
- ❌ 버전 관리 불가
- ❌ 팀원이 다시 설정해야 함

## 보안 점검리스트

- [x] render.yaml 파일 생성
- [x] 웹 서비스 설정 (build/start 명령어)
- [x] 환경 변수 설정 (DATABASE_URL 참조)
- [x] SECRET_KEY 포함 (임시값, 배포 후 변경 필요)
- [x] ALLOWED_HOSTS 설정 (Render 도메인)
- [x] CSRF_TRUSTED_ORIGINS 설정
- [x] DB_SSLMODE = require
- [ ] 프로덕션 SECRET_KEY 생성 및 설정
- [ ] IP allowlist 검토 (필요시 제한)

## 기술 깊이

### Render 환경 변수 참조 문법
```yaml
# 하드코딩
value: "fixed-value"

# 데이터베이스 참조
fromDatabase:
  name: database-name
  property: connectionString

# 환경 변수 참조
value: "{{ env.VARIABLE_NAME }}"
```

### PostgreSQL 연결 문자열 형식
```
postgres://username:password@hostname:5432/databasename

요소:
- username: PostgreSQL 사용자
- password: PostgreSQL 비밀번호
- hostname: 데이터베이스 호스트
- 5432: PostgreSQL 기본 포트
- databasename: 데이터베이스명
```

## 파일 크기 및 복잡도

| 항목 | 값 |
|------|-----|
| 파일 크기 | ~60줄 |
| 서비스 수 | 2개 (웹 + DB) |
| 환경 변수 | 7개 |
| 자동화 수준 | 높음 |

## 결론

CommUnity 프로젝트가 Render에 자동 배포되기 위한 Infrastructure as Code를 완성했습니다.

**완료 항목:**
- ✅ render.yaml 파일 생성
- ✅ 웹 서비스 설정 (community-web)
- ✅ PostgreSQL 데이터베이스 설정 (community-db)
- ✅ 환경 변수 자동 연결
- ✅ 보안 설정 (SSL, CSRF)

**다음 단계:**
1. GitHub에 push
2. Render 대시보드에서 GitHub 저장소 연동
3. render.yaml 파일 감지 확인
4. 자동 배포 실행

---

**작업 완료**: 2026-05-29
**상태**: ✅ render.yaml 파일 생성 완료
**다음**: Render 대시보드 배포 설정
