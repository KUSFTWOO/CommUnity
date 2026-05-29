이제깃허브에커밋및푸시를진행
• 터미널을열고아래명령어를순서대로진행
git add .
git commit –m “Configure project for Render deployment”
git push origin main
1. Render 대시보드로이동하여[+New] 버튼을누르고[Blueprint]를선택
2. GitHub 저장소목록에서community 프로젝트가설정된깃헙계정을선택하고연결
3. 연결이완료되면아래로내려가community 리포지토리와[connect]를클릭해서연결
4. 다음화면에서결제정보를입력. 국가, 주소, 카드정보등을입력하고아래쪽의[Add Cad] 버튼을클릭
5. 이름을입력하고[Retry] 버튼을클릭.  비용을확인하고[Deploy Blueprint]를 클릭
6. Render가 render.yaml 파일을 자동으로 읽어서비스이름(community-web) 과데이터베이스(communitydb)설정을화면에보여준다

7. 배포가성공적으로완료되면, 고유한.onrender.com 주소가생성.‒ 이주소로접속하여웹사이트가잘작동하는지확인‒ 왼쪽메뉴에서[Resources]를클릭하면, community-web (Web Service)과 community-db(PostgreSQL) 두 항목이 보임‒ community-web을 클릭해서웹서비스의상세페이지로이동‒ 페이지상단에
https://community-web-xxxxx.onrender.com과 같은 형태의 주소가 보임‒ 이것이바로배포된웹사이트의주소
8. (최초1회) 배포된사이트의관리자계정을설정‒ 대시보드의웹서비스페이지에서[Shell] 탭을열고, python manage.py createsuperuser명령어를실행하여관리자계정을생성‒ 이제깃허브에푸시하면자동으로Render에배포가진행‒ 만약배포에문제가생겼다면[Render] 대시보드[Events]로이동해서에러사항을복사해서클로드코드에전달달