# TR — Test Report
## 현재 테스트 커버리지 및 테스트 철학

> 버전: 1.0.0 | 최종 업데이트: 2025-05-15
> 개발 진행에 따라 지속 업데이트됩니다.

---

## 1. 현재 테스트 상태

> ⚠️ 프로젝트 초기 설계 단계 — 코드가 아직 작성되지 않았습니다.
> 아래는 달성할 테스트 계획과 기준을 정의합니다.

```
전체 커버리지   0%   (개발 미착수)
작성된 테스트   0개
```

---

## 2. 테스트 철학

### 2.1 접근 방식

> "모든 것을 테스트하려다 아무것도 못 하는 것보다,
>  중요한 것을 확실히 테스트하는 것이 낫다."

바이브코딩 특성상 빠른 개발을 우선하되,
**보안과 데이터 무결성에 관련된 기능은 반드시 테스트를 작성합니다.**

### 2.2 테스트의 3가지 목적

```
1. 회귀 방지    새 기능 추가가 기존 기능을 망가뜨리지 않도록
2. 보안 검증    권한 없는 접근이 차단되는지 확인
3. 개발 신뢰도  "이 코드는 동작한다"는 근거 확보
```

---

## 3. 커버리지 목표

### 3.1 App별 목표 커버리지

| App | 목표 | 이유 |
|-----|------|------|
| `accounts` | 80% 이상 | 인증·보안 핵심 |
| `board` | 70% 이상 | 주요 기능 |
| `notices` | 60% 이상 | 중요 기능 |
| `votes` | 60% 이상 | 중요 기능 |
| `calendar_app` | 50% 이상 | 부가 기능 |
| `dashboard` | 50% 이상 | 운영 기능 |

### 3.2 전체 목표

```
MVP 출시 전   전체 60% 이상
안정화 단계   전체 70% 이상
```

---

## 4. 테스트 종류별 계획

### 4.1 Model 테스트 — 단위 테스트

```python
# accounts/tests/test_models.py
class CustomUserModelTest(TestCase):
    - test_사용자_생성_성공
    - test_비밀번호가_해싱되어_저장된다
    - test_소프트_삭제_후_is_active가_False가_된다
    - test_닉네임은_유일해야_한다

# board/tests/test_models.py
class PostModelTest(TestCase):
    - test_게시글_생성_성공
    - test_조회수_증가가_원자적으로_동작한다
    - test_소프트_삭제된_게시글은_목록에서_제외된다
    - test_좋아요_중복_방지

class CommentModelTest(TestCase):
    - test_댓글_생성_성공
    - test_대댓글은_1단계까지만_허용된다
```

### 4.2 View 테스트 — 통합 테스트

```python
# 인증 관련
class AuthViewTest(TestCase):
    - test_회원가입_성공
    - test_중복_이메일로_회원가입_실패
    - test_로그인_성공
    - test_틀린_비밀번호로_로그인_실패
    - test_로그인_5회_실패_시_계정_잠금
    - test_로그아웃_성공

# 권한 관련 (보안 경계 테스트 — 최우선)
class PermissionTest(TestCase):
    - test_비로그인_사용자는_글쓰기_접근_불가
    - test_비로그인_사용자는_댓글_작성_불가
    - test_타인의_게시글을_수정할_수_없다
    - test_타인의_게시글을_삭제할_수_없다
    - test_일반_회원은_관리자_대시보드_접근_불가
    - test_공지사항은_관리자만_작성할_수_있다
    - test_투표는_관리자만_생성할_수_있다

# 게시판
class BoardViewTest(TestCase):
    - test_게시글_목록_페이지_200_응답
    - test_게시글_작성_성공_후_상세_페이지_리다이렉트
    - test_게시글_수정_성공
    - test_게시글_삭제_성공_소프트_삭제_확인
    - test_좋아요_추가_및_중복_방지
    - test_댓글_작성_성공
    - test_대댓글_작성_성공
```

### 4.3 Form 테스트

```python
class PostFormTest(TestCase):
    - test_정상_데이터로_폼_유효성_통과
    - test_빈_제목으로_유효성_실패
    - test_제목_200자_초과_시_유효성_실패
    - test_허용되지_않는_이미지_형식_차단
    - test_5MB_초과_이미지_차단
    - test_이미지_5장_초과_차단

class SignupFormTest(TestCase):
    - test_정상_회원가입_폼_유효성_통과
    - test_비밀번호_불일치_시_실패
    - test_비밀번호_8자_미만_시_실패
    - test_이메일_형식_오류_시_실패
```

---

## 5. Phase별 테스트 작성 계획

| Phase | 기능 | 테스트 대상 | 상태 |
|-------|------|------------|------|
| Phase 1 | 인증 시스템 | 인증 View·Form·Model | 🔲 미착수 |
| Phase 2 | 공지사항·게시판 | CRUD·권한·이미지 업로드 | 🔲 미착수 |
| Phase 3 | 댓글·좋아요 | 댓글 CRUD·좋아요 중복 방지 | 🔲 미착수 |
| Phase 4 | 캘린더·투표 | 투표 참여·중복 방지 | 🔲 미착수 |
| Phase 5 | 관리자 대시보드 | 관리자 권한·접근 제어 | 🔲 미착수 |
| Phase 6 | 전체 회귀 | 커버리지 측정 및 보완 | 🔲 미착수 |

---

## 6. 테스트 실행 현황 (최신)

```
마지막 실행일   -
총 테스트 수    0개
통과           0개
실패           0개
오류           0개
커버리지        0%
```

---

## 7. CI 자동화 계획 (GitHub Actions)

```yaml
# .github/workflows/test.yml (계획)
name: Django Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - run: python manage.py test
      - run: |
          pip install coverage
          coverage run manage.py test
          coverage report --fail-under=60
```

> 전체 커버리지 60% 미만이면 CI가 실패하고 배포를 차단합니다.

---

## 8. 버그 추적

| ID | 발견일 | 내용 | 상태 | 해결일 |
|----|--------|------|------|--------|
| — | — | 아직 발견된 버그 없음 (개발 미착수) | — | — |

> 버그 발견 시 이 표에 기록, 커밋 메시지에 `fix: #버그ID` 형태로 참조합니다.
