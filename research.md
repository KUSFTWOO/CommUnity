작업을 시작하기 전에 @docs/START.md을 읽자. 이전에 구현한 작업들을 메모리에 기억시키고 업무를 시작하자. 
분석이 완벽하게 끝나면 아래 작업을 시작해.
다양한 질문 타입을 지원하는 설문조사 시스템을 구현해줘
설문조사 모델:
1. Survey 모델 (title, description, is_anonymous, expires_at, created_by)
2. Question 모델 (survey, text, question_type, required, options)
3. Response 모델 (survey, respondent, submitted_at)
4. Answer 모델(response, question, answer_text)
질문타입:
- TEXT (주관식-짧은답변)
- TEXTAREA (주관식-긴답변)
- CHOICE (객관식-단일선택)
- MULTIPLE (객관식- 복수선택)

SCALE (척도1-5)
설문조사기능:
1. 설문목록(/surveys)
- 진행중/완료된 설문 구분
- 제목, 질문수, 응답자수
2. 설문응답(/surveys/<id>/respond)
- 질문별순차적표시
- 질문타입별적절한입력폼
- 필수질문체크

3. 설문 생성(/surveys/new)
- 관리자만접근
- 설문기본정보+ 질문들추가
- 동적질문추가/삭제(JavaScript)
4. 설문결과(/surveys/<id>/results)
- 관리자만접근
- 질문별통계
- 개별응답목록(실명인경우)
결과분석:
- 객관식: 선택지별비율
- 주관식: 답변목록
- 척도: 평균점수
총응답자수
권한:
- 누구나설문목록조회
- 로그인사용자만응답
관리자만생성/결과조회
UI:
- 단계별설문진행
- 진행률표시
- 질문별적절한폼
결과차트
surveys 앱의 모든파일을생성해줘:- models.py, views.py, forms.py, urls.py- 템플릿들(목록, 설문, 결과)
JavaScript (동적 질문 관리)
쓰기@logs/YYYYMMDD_tasks.md : 개발이끝나면업무보고서를작성할것
쓰기@logs/YYYYMMDD_logs.md: 업무 일기장을작성할것