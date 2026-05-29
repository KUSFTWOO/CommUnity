# Render Logs 확인하는 방법

400 Bad Request 실제 원인을 찾기 위해 Render 로그를 봐야 합니다.

## Step 1: Render Dashboard 접속
```
https://dashboard.render.com
```

## Step 2: community-web 서비스 클릭
```
Services → community-web
```

## Step 3: 로그 확인
```
상단 탭 중에서 [Logs] 탭 클릭
```

## Step 4: 에러 메시지 찾기
```
빨간색 텍스트 또는 ERROR 메시지 찾기

예시들:

❌ "ImproperlyConfigured: ..."
❌ "ALLOWED_HOSTS"
❌ "ModuleNotFoundError"
❌ "ValueError: "
❌ "KeyError: "
❌ "The host is invalid"
등등
```

## Step 5: 에러 메시지 복사
```
전체 에러 스택 트레이스 복사
(Traceback부터 마지막 줄까지)

이것을 Claude에 전달
```

---

## 가능한 400 에러 원인

### 원인 1: ALLOWED_HOSTS 설정 오류
```
에러 메시지:
"Invalid HTTP_HOST header: 'community-web-xxxx.onrender.com'. 
You may need to add 'community-web-xxxx.onrender.com' to ALLOWED_HOSTS."

해결: settings.py의 ALLOWED_HOSTS 수정
```

### 원인 2: DEBUG = False일 때 정적 파일 오류
```
에러 메시지:
"A 'text/html' Content-Type was returned"
또는 정적 파일 관련 오류

해결: WhiteNoise 설정 확인
```

### 원인 3: SECRET_KEY 미설정
```
에러 메시지:
"ImproperlyConfigured: The SECRET_KEY setting must not be empty."

해결: Environment Variables에 SECRET_KEY 추가
```

### 원인 4: DATABASE_URL 오류
```
에러 메시지:
"DATABASE_URL is required"
또는 "could not translate host name"

해결: DATABASE_URL 확인 및 다시 설정
```

---

## 빠른 진단 체크리스트

Render Logs를 확인하면서 다음을 살펴보세요:

```
□ "Starting server" 또는 "Application startup complete" 보임?
   → 예: Django 정상 시작
   → 아니오: 시작 단계에서 오류

□ "ALLOWED_HOSTS" 관련 오류?
   → settings.py의 ALLOWED_HOSTS 확인

□ "SECRET_KEY" 관련 오류?
   → Environment Variables의 SECRET_KEY 확인

□ "DATABASE_URL" 관련 오류?
   → Environment Variables의 DATABASE_URL 확인

□ "ModuleNotFoundError" 또는 import 오류?
   → 패키지 설치 확인

□ "StaticFiles" 또는 정적 파일 오류?
   → WhiteNoise 설정 확인
```

---

## 다음 단계

1. Render Logs 에서 **전체 에러 메시지 복사**
2. Claude에 전달: "이런 에러가 발생했습니다: [에러 내용]"
3. Claude가 정확한 원인 파악 및 해결

**로그 없이는 정확한 원인을 찾을 수 없습니다!**
