# [2026-05-29] 게시글 검색 기능 일기

## 오후 5:34 - 작업 시작

filtering.md 파일을 읽고 게시글 검색 기능의 요구사항을 확인했다.

**요구사항:**
- 검색 페이지: 검색창과 "검색" 버튼만 있는 UI
- 검색 로직: Notice와 Post 모델의 title/content에서 키워드 검색
- 결과 표시: /search 페이지 하단에 검색된 게시글 리스트

간단명료한 요구사항이므로 search 앱을 별도로 만들기로 결정.

## 오후 5:35 - search 앱 생성

```bash
python manage.py startapp search apps/search
```

앱 생성 후 apps.py의 name을 "apps.search"로 수정.

## 오후 5:40 - views.py 구현

`search_view` 함수를 작성했다.

**구현 상세:**
- GET 파라미터 'q'에서 키워드 받음
- Notice.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword))
- Post.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword))
- 두 QuerySet을 통합하여 리스트 생성
- created_at 기준으로 최신순 정렬

각 결과에는:
- type: 'notice' 또는 'post'
- title, content, author, created_at
- url: 해당 게시글로 이동하는 링크
- snippet: 본문의 처음 100자 + "..."

## 오후 5:45 - URLs 및 설정 수정

urls.py 작성:
```python
path('', views.search_view, name='search'),
```

config/settings.py에 "apps.search" 추가
config/urls.py에 "search/" URL 등록

## 오후 5:50 - 템플릿 구현

`search/search.html` 템플릿을 작성했다.

**구조:**
1. 검색 헤더
2. 검색 폼 (GET 방식, 단순함)
3. 검색 결과
   - 결과 요약: "키워드" 검색 결과 X건
   - 결과 카드 (반복)
   - 결과 없음 메시지

**스타일:**
- Tailwind CSS로 일관성 있는 디자인
- 타입 배지: 📢 공지사항 (파란색), 💬 게시판 (보라색)
- 호버 효과: 그림자 증가, 테두리색 변경
- line-clamp-2: 본문 요약을 2줄로 제한

## 오후 6:00 - navbar 수정

navbar.html에 🔍 검색 링크를 추가했다.

위치: 설문 링크 뒤 (가장 오른쪽)
```html
<a href="{% url 'search:search' %}">
    🔍 검색
</a>
```

## 오후 6:05 - 최종 검증

`python manage.py check` → 성공

## 특징

### 설계 결정

**왜 search 앱을 별도로 만들었나?**
- 검색은 여러 모델을 다루므로 단일 책임 원칙에 맞게 분리
- 향후 파일 검색, 댓글 검색 등 확장할 때 유리
- 점진적 기능 추가 가능

**왜 GET 방식인가?**
- URL에 검색어가 남아 북마크 가능
- /search/?q=파이썬 → 공유 가능한 링크
- 브라우저 뒤로가기로 이전 검색 복원
- SEO 친화적 (검색 인덱싱 가능)

**왜 icontains를 사용했나?**
- 대소문자 구분 없이 검색
- 사용자 경험 개선
- 한글 검색도 정확하게

**왜 Notice와 Post를 리스트로 통합했나?**
- 사용자가 모든 게시글을 한눈에 보고 싶어함
- 최신순 정렬로 중요한 글부터 노출
- 타입 배지로 구분 가능

## 개선 아이디어

추후 구현할 수 있는 기능:
1. **검색어 자동완성**: 입력 중 추천 키워드 표시
2. **페이지네이션**: 결과가 많을 때 분할
3. **필터링**: 타입별(공지/게시판), 날짜별, 작성자별
4. **검색 히스토리**: 최근 검색어 저장
5. **핫키워드**: 가장 많이 검색된 키워드
6. **고급 검색**: AND, OR, NOT 연산자
7. **Full-Text Search**: PostgreSQL의 전문 검색 지원

## 흥미로운 부분

1. **Q 객체의 힘**: 복잡한 쿼리를 간결하게 표현
2. **GET 파라미터의 활용**: 상태를 URL에 저장
3. **모델 통합**: 다른 모델의 결과를 하나의 리스트로 표현
4. **UX 고려**: 타입 배지, 호버 효과, 스니펫 표시

## 실제 동작 예상

```
사용자 → /search/?q=파이썬
→ Notice와 Post 모두에서 "파이썬" 검색
→ 결과: 공지사항 2개, 게시판 글 5개 총 7개
→ 최신순 정렬로 표시
```

## 성능 고려사항

- select_related 없음: Notice와 Post는 이미 created_by/author를 많이 사용
- 실제로는 `select_related('created_by')` / `select_related('author')` 추가 가능
- 검색 결과 대량일 때 페이지네이션 필요

## 최종 생각

간단하면서도 실용적인 기능을 구현했다.
filtering.md의 요구사항을 정확히 이행했으며,
사용자 경험도 고려했다.

다음 단계에서 더 많은 기능을 추가할 수 있는
확장 가능한 구조로 설계했다.
