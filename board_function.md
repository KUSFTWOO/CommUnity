작업을 시작하기전 에 @docs/START.md을 읽자. 이전에 구현한 작업들을 메모리에 기억시키고 업무를 시작하자. 
분석이 완벽하게 끝나면 아래 작업을 시작해.
좋아요, 조회수, 댓글, 대댓글이 있는 자유게시판을 구현해줘.
모델설계:
1. Post 모델(title, content, author, views, created_at)
2. Comment 모델(content, author, post, parent, created_at)
3. Like 모델 (user, post, created_at)
자유게시판 기능:
1. 게시글 목록(/posts)- 제목, 작성자, 좋아요수, 댓글수, 조회수, 작성일- 페이지네이션(15개씩)- 검색기능(제목+내용)
2. 게시글 상세(/posts/<id>)- 조회수 자동 증가(중복방지)- 좋아요 버튼(HTMX로실시간)- 댓글 목록 및 작성 폼- 대댓글 들여쓰기 표시
3. 게시글 작성(/posts/new)- 로그인 필수- 제목, 내용입력- 간단한 에디터
댓글시스템:- 댓글작성(HTMX로새로고침없이)- 대댓글(parent 필드사용)- 작성자만 삭제 가능
댓글 계층 구조 표시
좋아요 시스템:- 중복 좋아요 방지- HTMX로 즉시 반영
좋아요 취소 가능
권한:- 로그인한 사용자만 작성/댓글/좋아요- 작성자만 자신의 글/댓글 수정/삭제
관리자는 모든 권한
UI/UX:- 게시글 카드 레이아웃- 좋아요 버튼 애니메이션- 댓글 인라인 작성
모바일 최적화
posts 앱의 모든 파일을 생성해줘:- models.py (Post, Comment, Like)- views.py (HTMX 뷰 포함)- forms.py- urls.py-템플릿들
쓰기@logs/YYYYMMDD_tasks.md : 개발이 끝나면 업무보고서를 작성할 것
쓰기@logs/YYYYMMDD_logs.md: 업무 일기장을 작성할 것