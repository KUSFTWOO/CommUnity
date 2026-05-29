작업을 시작하기 전에 @docs/START.md을 읽자. 이전에 구현한 작업들을 메모리에 기억시키고 업무를 시작하자. 
분석이 완벽하게 끝나면 아래 작업을 시작해.
관리자만 작성할 수 있는 공지사항 시스템을 구현해줘.
Notice 모델:- title (제목)- content (내용)- author (작성자- 관리자만)- is_important (중요 공지 여부)
created_at, updated_at
기능:
1. 공지사항 목록(/notices)- 최신순 정렬- 중요 공지는 상단 고정- 페이지네이션(10개씩)
2. 공지사항 상세(/notices/<id>)- 제목, 내용, 작성일표시- 관리자만 수정/삭제버튼
3. 공지사항 작성(/notices/new)- 관리자만 접근가능- 제목, 내용, 중요도선택
권한:- 누구나 공지사항 조회 가능- 관리자만 작성/수정/삭제
비관리자 접근 시 403 에러
UI:- 카드 형태 공지사항 목록- 중요 공지는 빨간 배지 표시
깔끔한 작성 폼
notices 앱의 모든 파일을 생성해줘:- models.py, views.py, forms.py, urls.py
템플릿들(목록, 상세, 작성)
쓰기@logs/YYYYMMDD_tasks.md : 개발이 끝나면 업무보고서를 작성할 것
쓰기@logs/YYYYMMDD_logs.md: 업무 일기장을 작성할 것