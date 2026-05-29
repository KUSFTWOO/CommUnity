[운영 환경용 패키지 설치]
작업을 시작하기 전에 @docs/START.md을 읽자. 이전에 구현한 작업들을 메모리에 기억시키고 업무를 시작하자. 분석이 완벽하게 끝나면 아래 작업을 시작해.
현재 프로젝트의 가상환경에 Render 배포에 필요한 Python 패키지들을 설치해줘. 설치할 패키지는 gunicorn, psycopg2-binary, dj-database-url, whitenoise 야. 아래의 작업을 순서대로 진행해 줘.
requirements.txt 업데이트
패키지 설치가 완료되면 설치한 패키지들을 포함해서 현재 가상환경의 모든 패키지 목록을 requirements.txt 파일에 갱신해줘.
settings.py를 배포 환경에 맞게 수정
config/settings.py 파일을 수정해서 로컬 개발 환경(SQLite)은 그대로 유지하면서, Render의 운영 환경(PostgreSQL)에서도 작동할수 있도록 유연하게 만들어 줘.
수정 조건:
1. os와 dj_database_url을 임포트해줘.
2. SECRET_KEY는 환경 변수에서 읽어오도록 수정하고, 환경 변수가 없을 때를 대비한 기본값도 설정해줘. (보안상 실제 키는 나중에 Render에서 설정할거야)
3. DEBUG 모드는 'RENDER' in os.environ 코드를 사용해서 Render 환경에서는 자동으로 False가 되도록 설정해 줘.
4. ALLOWED_HOSTS는 Render의 도메인을 자동으로 허용하도록 설정해줘.
5. DATABASES 설정은DATABASE_URL 환경 변수가 있으면 PostgreSQL을 사용하고, 없으면기존의db.sqlite3를 사용하도록 dj_database_url.config()를 이용해 수정해 줘.
6. MIDDLEWARE 목록에서 'django.middleware.security.SecurityMiddleware' 바로 아래에 'whitenoise.middleware.WhiteNoiseMiddleware'를 추가해 줘.
7. 정적 파일(STATICFILES) 관련 설정은 운영환경(if not DEBUG:)에서만 STATIC_ROOT와 Whitenoise용 STATICFILES_STORAGE를 사용하도록 추가해 줘.
쓰기@logs/YYYYMMDD_tasks.md : 개발이 끝나면 업무 보고서를 작성할 것
쓰기@logs/YYYYMMDD_logs.md: 업무 일기장을 작성할 것
