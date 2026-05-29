[데이터베이스성능개선]
작업을시작하기전에@docs/START.md을읽자. 이전에구현한작업들을메모리에기억시키고업무를시작하자. 분석이완벽하게끝나면아래작업을시작해.
프로젝트의설정을최적화할거야. 내장고프로젝트의`settings.py` 파일을수정해서, SQLite 데이터베이스가프로덕션환경에서최고의성능과안정성, 데이터무결성을갖도록만들어줘.
아래세가지요구사항을모두반영해서코드를수정해야해.
• WAL(Write-Ahead Logging) 모드 활성화: 읽기/쓰기 동시성을 극대화하기 위해데이터베이스연결시`PRAGMA journal_mode=WAL;` 명령이실행되도록설정해줘.
• Busy Timeout 설정: 동시 쓰기 요청 시 발생하는`Database is locked` 에러를 방지하기위해타임아웃값을20초로설정해줘.
• 외래 키(Foreign Key) 제약 조건 활성화: 데이터무결성을보장하기위해SQLite에서기본적으로비활성화된외래키제약조건을활성화해줘. (`PRAGMA foreign_keys=ON;`)
기존`settings.py` 파일의 `DATABASES` 설정을 아래 예시처럼 변경하거나개선해줘.
# 기존코드예시
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': BASE_DIR / 'db.sqlite3',
}
}
쓰기@logs/YYYYMMDD_tasks.md : 개발이 끝나면업무보고서를작성할것
쓰기@logs/YYYYMMDD_logs.md: 업무 일기장을 작성할것