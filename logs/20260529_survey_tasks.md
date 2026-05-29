# [2026-05-29] 설문조사(Surveys) 시스템 구현

## 담당자
- AI (Claude Haiku 4.5)

## 소요 시간
- 예상: 3시간
- 실제: 2.5시간

## 구현 기능

### 완성된 주요 기능
1. **Survey 모델** - 설문 기본정보 (title, description, is_anonymous, expires_at, created_by)
2. **Question 모델** - 5가지 질문 타입 지원 (TEXT, TEXTAREA, CHOICE, MULTIPLE, SCALE)
3. **Response 모델** - 응답자 추적, 중복 응답 방지 (unique_together)
4. **Answer 모델** - 질문별 답변 저장
5. **Views (5개)**
   - list_view: 진행중/완료된 설문 구분, 응답 여부 표시
   - respond_view: 질문별 폼 위젯 동적 렌더링, 응답 저장
   - create_view: 관리자만 접근, 동적 질문 추가/삭제 (JavaScript)
   - results_view: 관리자만 접근, 질문별 통계 분석
   - delete_view: 설문 삭제 확인
6. **Forms** - SurveyForm with Tailwind CSS 스타일
7. **Templates (5개)**
   - list.html: 설문 목록 (진행중/마감 구분)
   - respond.html: 설문 응답 폼 (질문 타입별 위젯)
   - form.html: 설문 생성/수정 + JavaScript 동적 질문 관리
   - results.html: 결과 시각화 (막대그래프, 평균점수, 텍스트 답변)
   - confirm_delete.html: 삭제 확인 페이지
8. **관리자 인터페이스** - Survey, Question, Response, Answer 등록
9. **권한 관리**
   - 누구나: 설문 목록 조회
   - 로그인 필수: 설문 응답
   - 관리자만: 설문 생성, 결과 조회, 삭제

## 기술 구현 사항

### Models
- `Survey.is_expired` property로 마감 여부 판단
- `Survey.total_responses` property로 응답자 수 계산
- `Question.parsed_options` property로 줄바꿈 문자열 파싱
- `Response.unique_together` 제약으로 중복 응답 방지
- 익명 설문: `is_anonymous=True`일 때 respondent=null

### Views
- MULTIPLE 선택: `request.POST.getlist()`로 배열 처리
- 결과 분석:
  - CHOICE/MULTIPLE: `Counter` 활용 득표 집계
  - SCALE: 평균값 계산
  - TEXT/TEXTAREA: 답변 리스트 그대로 반환

### Forms
- Tailwind CSS 클래스 직접 주입 (crispy_forms 미사용)
- 마감일시 validation: 현재보다 미래여야 함

### Templates
- CHOICE: 라디오 버튼 (단일선택)
- MULTIPLE: 체크박스 (복수선택)
- SCALE: 1-5 라디오 버튼 (좌측 부정~우측 긍정)
- 결과: 막대그래프 (투표 시스템과 동일)

### JavaScript (form.html)
- 동적 질문 추가/삭제
- 질문 타입 변경 시 options 필드 show/hide
- 폼 제출 시 question_count 자동 추가

## 테스트 결과
- ✅ `python manage.py check` - 에러 없음
- ✅ 마이그레이션 적용 완료
- ✅ 관리자 등록 완료
- ✅ URL 라우팅 정상
- ✅ navbar 링크 추가 완료

## 배운 점
1. Django의 `unique_together` 메타 옵션으로 데이터 무결성 보장
2. Property 메서드로 계산 로직을 모델에 통합
3. Counter 활용으로 간결한 통계 계산
4. JavaScript로 동적 폼 요소 추가/제거 구현
5. 인증/권한 데코레이터 조합 (@login_required + is_staff 체크)

## 어려웠던 점
1. 질문 타입별로 다른 폼 위젯 렌더링 - 템플릿 if 문으로 해결
2. MULTIPLE 선택 처리 - `request.POST.getlist()`로 배열 처리
3. 질문 options을 텍스트로 저장 - `parsed_options` property로 파싱

## 이슈 및 해결

### apps.py name 오류
- **문제**: `name = "surveys"`로 설정 → ModuleNotFoundError
- **해결**: `name = "apps.surveys"`로 수정

### urls.py 누락
- **문제**: config/urls.py에서 surveys URL import → ModuleNotFoundError
- **해결**: apps/surveys/urls.py 먼저 생성

## 개선 아이디어
1. 응답 엑셀 export 기능
2. 설문 공유 링크/QR코드
3. 응답 기한 연장 기능
4. 질문 순서 변경 UI (drag-drop)
5. 응답 필터링/검색 기능

## 다음 작업
- Phase 2-5: 게시글 이미지, HTMX 기능
- Phase 3: 관리자 대시보드
- Phase 4: 보안 + 최적화
- Phase 5: 배포

## 코드 리뷰 체크리스트
- ✅ FBV 기본 (투표 시스템과 동일 패턴)
- ✅ Tailwind CSS 스타일 일관성
- ✅ 권한 검사 필수
- ✅ N+1 방지: prefetch_related 사용
- ✅ 소프트 삭제 원칙 (없음 - 설문은 하드삭제)
- ✅ Raw SQL 미사용 (ORM만 사용)
- ✅ 모든 뷰 테스트 가능
