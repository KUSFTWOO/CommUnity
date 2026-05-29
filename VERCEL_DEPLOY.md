# CommUnity Vercel 배포 가이드

## 배포 URL

- **프로덕션**: https://community-wine-iota.vercel.app
- **Vercel 대시보드**: https://vercel.com/twoo00-5507s-projects/community

## 현재 상태

배포는 완료되었으나, **PostgreSQL(`DATABASE_URL`)이 없어** 런타임에서 SQLite를 열지 못해 **500 오류**가 발생합니다.  
(Vercel 서버리스는 로컬 `db.sqlite3` 파일을 사용할 수 없습니다.)

## PostgreSQL 연결 (필수)

### 방법 A: Vercel + Neon (권장)

1. 브라우저에서 약관 동의:  
   https://vercel.com/twoo00-5507s-projects/~/integrations/accept-terms/neon?source=cli
2. 터미널에서:
   ```powershell
   cd c:\sw\community
   vercel integration add neon
   ```
3. Vercel 대시보드 → **Storage** → Neon DB를 `community` 프로젝트에 연결
4. `DATABASE_URL` 환경 변수가 자동으로 추가되면 재배포:
   ```powershell
   vercel deploy --prod --yes
   ```

### 방법 B: 기존 PostgreSQL URL 직접 등록

```powershell
vercel env add DATABASE_URL production
# postgres://user:pass@host:5432/dbname 형식으로 입력
vercel deploy --prod --yes
```

## 환경 변수 (Production)

| 변수 | 설명 |
|------|------|
| `SECRET_KEY` | Django 시크릿 (설정됨) |
| `DEBUG` | `False` 권장 (설정됨) |
| `ALLOWED_HOSTS` | `.vercel.app` 포함 (설정됨) |
| `CSRF_TRUSTED_ORIGINS` | `https://*.vercel.app` (설정됨) |
| `DATABASE_URL` | **PostgreSQL 연결 문자열 (필수, 미설정)** |

## 로컬에서 Vercel 환경 동기화

```powershell
vercel env pull .env.local
```

## 재배포

```powershell
.\deploy-vercel.ps1
# 또는
vercel deploy --prod --yes
```

## 빌드 시 마이그레이션

`DATABASE_URL`이 설정되면 `build.py`가 배포 시 `migrate`를 자동 실행합니다.

## 미디어 업로드

프로필/게시글 이미지는 Vercel 서버리스 디스크에 영구 저장되지 않습니다.  
프로덕션에서는 S3/Supabase Storage 등 외부 스토리지 연동이 필요합니다.
