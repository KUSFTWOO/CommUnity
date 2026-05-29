# [2026-05-29] 설문조사 시스템 구현 일기

## 오전 5:27 - 프로젝트 분석

research.md 파일을 읽고 설문조사 시스템의 요구사항을 파악했다.

**요구사항 핵심:**
- 5가지 질문 타입 (TEXT, TEXTAREA, CHOICE, MULTIPLE, SCALE)
- 동적 질문 추가/삭제 JavaScript
- 진행중/완료 설문 구분
- 질문별 통계 분석 (막대그래프, 평균, 텍스트 목록)
- 관리자만 설문 생성/결과 조회

기존의 투표 시스템(FBV + Tailwind)과 동일한 패턴으로 구현하기로 결정.

## 오전 5:30 - 계획 수립

기존 코드 패턴을 분석했다:
- CustomUser: email/nickname unique, 설문에서 respondent 추적
- views.py: FBV 100% 사용, @login_required + is_staff 조합
- forms.py: ModelForm + Tailwind attrs 주입
- templates: 투표와 유사한 Tailwind 클래스 패턴

구현 순서:
1. 앱 생성 + models.py
2. settings.py, config/urls.py 수정
3. makemigrations + migrate
4. views.py, forms.py, urls.py
5. 5개 템플릿
6. navbar 수정
7. admin.py 등록

## 오전 5:35 - 앱 생성 및 모델 구현

surveys 앱을 생성하고 모델을 작성했다.

**모델 구조:**
```
Survey (제목, 설명, 익명여부, 마감일, 작성자)
├── Question (질문, 타입, 필수여부, 선택지, 순서)
│   └── Answer (응답, 질문, 답변텍스트)
└── Response (설문, 응답자, 제출시간) [unique_together]
```

중요한 설계 결정:
- `Response.unique_together = [['survey', 'respondent']]`: 한 사람당 한 번만 응답
- 익명 설문: `is_anonymous=True`일 때 respondent=null
- Answer의 answer_text: MULTIPLE도 '|'로 구분하여 텍스트로 저장

## 오전 5:40 - 설정 및 마이그레이션

config/settings.py, config/urls.py를 수정하고 마이그레이션을 생성했다.

**이슈:**
1. apps.py의 name이 "surveys"였음 → "apps.surveys"로 수정
2. urls.py가 먼저 필요했음 → urls.py 먼저 생성 후 makemigrations

모든 마이그레이션이 성공적으로 적용되었다.

## 오전 5:50 - Views 구현

5개 뷰를 구현했다:

### list_view
- 모든 사람 접근 가능
- 진행중/완료 설문 구분
- 인증 사용자: 응답 여부 표시

### respond_view
- 로그인 필수
- GET: 모든 질문을 한 페이지에 표시
- POST: 중복 체크 → Response 생성 → Answer 배열 저장
- MULTIPLE: `request.POST.getlist()`로 배열 처리

### create_view
- @login_required + is_staff
- 동적 질문 저장 (POST data에서 question_N_* 형식으로 파싱)

### results_view
- 관리자만 접근
- 질문별 분석:
  - CHOICE/MULTIPLE: Counter로 득표 집계
  - SCALE: sum() / len()으로 평균 계산
  - TEXT/TEXTAREA: 답변 리스트 그대로

### delete_view
- 관리자만 접근
- 확인 후 설문 삭제

## 오전 6:00 - Forms 및 Admin

SurveyForm과 admin.py를 구현했다.

**SurveyForm:**
- title, description, is_anonymous, expires_at
- Tailwind CSS 클래스 직접 주입
- 마감일시 validation (현재보다 미래)

**Admin:**
- Survey, Question, Response, Answer 등록
- list_display로 핵심 정보 표시
- readonly_fields로 자동 계산 필드 보호

## 오전 6:15 - 템플릿 (1) - list.html

설문 목록 템플릿을 구현했다.

**특징:**
- 진행중/마감 설문 섹션 분리
- 각 설문: 제목, 설명, 질문수, 응답자수, 마감일
- 응답 완료 표시 (진행중 설문)
- 관리자: 결과/삭제 버튼

투표 시스템과 유사한 구조지만, 설문의 특성상 간단하게 구현했다.

## 오전 6:30 - 템플릿 (2) - respond.html

설문 응답 템플릿을 구현했다.

**특징:**
- 모든 질문을 한 페이지에 표시
- 질문 타입별 폼 위젯:
  - TEXT: input[type=text]
  - TEXTAREA: textarea
  - CHOICE: 라디오 버튼
  - MULTIPLE: 체크박스
  - SCALE: 1-5 라디오 + 좌측(부정)~우측(긍정) 라벨
- 필수/선택 표시
- 로그인 안 함: 로그인 유도 메시지

## 오전 6:50 - 템플릿 (3) - form.html + JavaScript

가장 복잡한 템플릿: 설문 생성 + 동적 질문 관리

**HTML:**
- 기본정보: 제목, 설명, 익명여부, 마감일시
- 질문 섹션: 동적으로 추가/제거

**JavaScript:**
- `addQuestion()`: 새 질문 블록 추가
- `removeQuestion()`: 질문 삭제
- `updateQuestionNumbers()`: 질문 번호 재계산
- `updateOptionsVisibility()`: 질문 타입에 따라 options 필드 show/hide
- 폼 제출 시 `question_count` hidden input 추가

처음엔 질문 타입별로 options 필드가 자동으로 show/hide되지 않아 JavaScript 조정이 필요했다.

## 오전 7:10 - 템플릿 (4) - results.html

결과 시각화 템플릿을 구현했다.

**특징:**
- 전체 응답자 수 표시
- 질문별 분석:
  - CHOICE/MULTIPLE: 막대그래프 + 비율 (투표 시스템과 동일)
  - SCALE: 평균점수 + 응답자 수
  - TEXT/TEXTAREA: 답변 텍스트 목록 (max-h-96 스크롤)

**스타일:**
- 각 질문을 card로 구분
- 인색 배경으로 섹션 분리
- 막대그래프는 Tailwind width로 동적 표현

## 오전 7:25 - 템플릿 (5) - confirm_delete.html

삭제 확인 템플릿을 구현했다.

투표 시스템과 동일한 패턴이지만, 설문 제목과 응답자 수를 표시한다.

## 오전 7:35 - navbar 수정 및 최종 검증

navbar.html에 📋 설문 링크를 추가했다.

**추가 위치:**
```html
<a href="{% url 'surveys:list' %}" class="...">
    📋 설문
</a>
```

`python manage.py check` → 성공

## 오전 7:45 - 로그 작성

tasks.md와 logs.md를 작성했다.

## 최종 상태

**구현 완료:**
- ✅ 4개 모델 (Survey, Question, Response, Answer)
- ✅ 5개 뷰 (list, respond, create, results, delete)
- ✅ SurveyForm
- ✅ 5개 템플릿
- ✅ Admin 등록
- ✅ navbar 수정

**코드 품질:**
- FBV + Tailwind 패턴 일관성 유지
- 권한 검사 완벽함
- 중복 응답 방지 구현
- 질문 타입별 폼 위젯 다양함
- JavaScript로 동적 질문 관리

**다음 단계:**
- 테스트 데이터로 실제 동작 확인
- Phase 2-5: 게시글 이미지, HTMX
- Phase 3: 대시보드

## 흥미로웠던 부분

1. **unique_together 활용**: Response 모델에서 한 사람당 한 번만 응답하도록 DB 제약 설정
2. **JavaScript 동적 폼**: 질문 추가/삭제와 타입별 필드 show/hide
3. **다양한 결과 분석**: Counter로 CHOICE/MULTIPLE, 평균으로 SCALE, 목록으로 TEXT
4. **Property 메서드**: `is_expired`, `total_responses` 등으로 계산 로직 캡슐화

## 아쉬운 부분

1. 응답 엑셀 export 미구현 (Phase 3에서 고려)
2. 질문 순서 변경 UI 미구현 (현재는 order로 저장만 함)
3. 질문 수정 UI 미구현 (현재는 create만 지원)

그래도 핵심 기능은 모두 구현되었고, 확장 가능한 구조로 설계되었다.
