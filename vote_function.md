작업을 시작하기 전에 @docs/START.md을 읽자. 이전에 구현한 작업들을 메모리에 기억시키고 업무를 시작하자. 분석이 완벽하게 끝나면 아래 작업을 시작해.

간단하고 직관적인 투표 시스템을 구현해 줘.

투표 모델:

Poll 모델 (question, created_by, expires_at, created_at)

PollOption 모델 (poll, text, votes_count)

Vote 모델 (poll, option, user, created_at)

투표 기능:

1. 투표 목록 (/polls)

진행중/완료된 투표 구분

투표 제목, 참여자 수, 마감일

2. 투표 참여 (/polls/)

투표 질문 및 선택지

라디오 버튼으로 선택

투표 후 결과 표시 (막대 그래프)

3. 투표 생성 (/polls/new)

관리자만 접근

질문, 선택지들, 마감일 입력

최소 2개, 최대 10개 선택지

투표 규칙:

로그인한 사용자만 참여

한 사람당 한 번만 투표

투표 후 결과 즉시 확인 가능

마감된 투표는 결과만 표시

결과 표시:

각 선택지별 득표율 (%)

총 참여자 수

CSS로 간단한 막대 그래프

권한:

누구나 투표 목록/결과 조회

로그인 사용자만 투표 참여

관리자만 투표 생성/관리

UI:

깔끔한 투표 카드

직관적인 선택지

결과 시각화

polls 앱의 모든 파일을 생성해줘:

models.py, views.py, forms.py, urls.py

템플릿들 (목록, 투표, 결과)

쓰기 @logs/YYYYMMDD_tasks.md : 개발이 끝나면 업무 보고서를 작성할 것
쓰기 @logs/YYYYMMDD_logs.md: 업무 일기장을 작성할 것