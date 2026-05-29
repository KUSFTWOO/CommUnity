# Render에서 PostgreSQL 수동으로 생성하기

render.yaml의 자동 생성이 작동하지 않으므로, 수동으로 직접 생성

## Step 1: Render 대시보드에서 PostgreSQL 생성

**경로:**
```
https://dashboard.render.com
  ↓
우측 상단 [+ New] 버튼 클릭
  ↓
[PostgreSQL] 선택 (목록에서 찾기)
```

## Step 2: PostgreSQL 설정 입력

**입력할 정보:**

| 항목 | 값 |
|------|-----|
| **Name** | community-db |
| **Database** | community |
| **User** | postgres |
| **Password** | [자동 생성됨 - 그대로 사용] |
| **Region** | Ohio (또는 가장 가까운 지역) |
| **Plan** | Free |

**입력 방법:**
```
1. Name 필드 → "community-db" 입력
2. Database 필드 → "community" 입력
3. User 필드 → "postgres" (기본값 사용)
4. Password 필드 → [자동 생성됨 - 그대로 둠]
5. Region 선택 → "Ohio" 선택
6. Plan 선택 → "Free" 선택
```

## Step 3: 데이터베이스 생성

```
모든 정보 입력 완료 후:
[Create Database] 버튼 클릭

약 2-3분 대기 (데이터베이스 생성 중)
```

## Step 4: External Database URL 확인

```
생성 완료 후:
community-db 페이지에서 다음을 찾기:

┌──────────────────────────────┐
│ Connections                  │
├──────────────────────────────┤
│ External Database URL        │
│                              │
│ postgresql://postgres:...    │
│ abc123xyz@oregon-...         │
└──────────────────────────────┘

또는

┌──────────────────────────────┐
│ Database URL                 │
│                              │
│ postgresql://postgres:...    │
└──────────────────────────────┘
```

**전체 URL 복사 (중요!):**
```
예시:
postgresql://postgres:MyPassword123@oregon-postgres.render.com:5432/community
```

## Step 5: community-web에 DATABASE_URL 추가

```
Render Dashboard
  ↓
Services → community-web
  ↓
Settings → Environment Variables
  ↓
[+ Add Environment Variable] 클릭
```

**입력:**
```
Key:   DATABASE_URL
Value: [Step 4에서 복사한 postgresql://... 전체]
```

**[Add] 클릭**

## Step 6: 다른 Environment Variables도 확인

```
다음이 모두 설정되어 있는지 확인:

✅ RENDER = true
✅ DEBUG = false
✅ SECRET_KEY = [값]
✅ DATABASE_URL = postgresql://... ← 방금 추가!
✅ ALLOWED_HOSTS = community-web.onrender.com
✅ CSRF_TRUSTED_ORIGINS = https://community-web.onrender.com
✅ DB_SSLMODE = require

없으면 모두 [+ Add Environment Variable]로 추가
```

## Step 7: 저장 및 재배포

```
1. [Save] 또는 [Update] 클릭
2. [Redeploy] 또는 [Retry Deploy] 클릭
3. Logs 탭에서 배포 진행 상황 확인
4. 약 5분 후 배포 완료
```

## ✅ 배포 성공 확인

```
https://community-web-xxxxx.onrender.com 접속

✅ 홈페이지 로드
✅ CSS/JavaScript 정상
✅ 로그인 가능
✅ DATABASE_URL 연결 성공
```

---

## 📋 체크리스트

```
□ [+ New] → [PostgreSQL] 클릭
□ Name: community-db 입력
□ Database: community 입력
□ Region: Ohio 선택
□ Plan: Free 선택
□ [Create Database] 클릭
□ 2-3분 대기
□ External Database URL 복사
□ community-web Settings에서 DATABASE_URL 추가
□ [Save] → [Redeploy] 클릭
□ 배포 완료 (5분 대기)
□ 웹사이트 접속 확인 ✅
```

**이 방법이면 100% 성공합니다!**
