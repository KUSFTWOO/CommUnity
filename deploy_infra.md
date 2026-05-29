[render.yaml 파일 생성]
작업을시작하기전에@docs/START.md을읽자. 이전에구현한작업들을메모리에기억시키고업무를시작하자. 분석이완벽하게끝나면아래작업을시작해.
프로젝트의루트디렉토리에render.yaml파일을생성해줘. 이파일은Render에게웹서비스와데이터베이스를어떻게구성할지알려주는설계도역할을할거야.
파일내용조건:
1. 서비스는web 타입의community-web 하나와, db 타입의 community-db PostgreSQL 데이터베이스 하나를 정의해 줘.
2. 웹 서비스의빌드명령어는pip install, collectstatic, migrate를 순서대로 실행하도록 설정해 줘.
3. 웹 서비스의시작명령어는gunicornconfig.wsgi로 설정해 줘.
4. 웹 서비스의환경변수(envVars)는데이터베이스의연결URL(DATABASE_URL)과 SECRET_KEY를 참조하도록설정해줘. SECRET_KEY는일단임의의값으로생성해줘. (나중에Render 
대시보드에서수정)
5. 데이터베이스플랜은free로설정해줘.
쓰기@logs/YYYYMMDD_tasks.md : 개발이 끝나면 업무 보고서를작성할것
쓰기@logs/YYYYMMDD_logs.md: 업무 일기장을 작성할것