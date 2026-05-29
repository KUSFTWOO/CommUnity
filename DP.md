# DP — Design Principles
## UI/UX 철학 및 제약사항

> 버전: 1.0.0
> 모든 UI 구현 시 이 문서를 먼저 확인하고 원칙을 지킵니다.

---

## 1. 디자인 철학

### 1.1 핵심 원칙 3가지

```
1. 명확함 (Clarity)     사용자가 다음에 무엇을 해야 할지 항상 알 수 있어야 한다.
2. 일관성 (Consistency) 같은 요소는 같은 방식으로 표현한다.
3. 친근함 (Warmth)      딱딱한 시스템이 아닌, 사람 냄새 나는 공간처럼 느껴져야 한다.
```

### 1.2 UX 원칙

- **클릭 최소화** — 핵심 행동(글쓰기, 댓글 달기)은 3클릭 이내에 도달
- **즉각 피드백** — 모든 사용자 액션에 즉각적인 시각적·텍스트 피드백
- **오류 친화적** — 오류 메시지는 원인과 해결 방법을 함께 제공
- **빈 화면 방지** — 데이터가 없는 화면은 안내 문구 + CTA 버튼으로 채움

---

## 2. 컬러 시스템

### 2.1 메인 팔레트 (Tailwind CSS 기준)

```
Primary (신뢰감 — 인디고 계열)
  기본:    indigo-600  (#4F46E5)
  호버:    indigo-700  (#4338CA)
  연한:    indigo-50   (#EEF2FF)

Neutral (가독성 중심)
  본문:    gray-900    (#111827)
  보조:    gray-500    (#6B7280)
  테두리:  gray-200    (#E5E7EB)
  배경:    gray-50     (#F9FAFB)
  카드:    white       (#FFFFFF)

Semantic (상태 표현)
  성공:    emerald-500 (#10B981)
  경고:    amber-500   (#F59E0B)
  오류:    red-500     (#EF4444)
  정보:    blue-500    (#3B82F6)
```

### 2.2 컬러 사용 규칙

- Primary 색상은 **주요 CTA 버튼, 링크, 활성 상태**에만 사용
- 배경 `gray-50`, 카드 `white`로 구분하여 깊이감 표현
- 오류·경고·성공 색상은 해당 상황에서만 사용
- 색상만으로 상태를 표현하지 않음 (아이콘 병행 필수)

---

## 3. 타이포그래피

### 3.1 폰트 설정

```html
<!-- base.html <head>에 포함 -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
```

기본 폰트: `font-family: 'Noto Sans KR', sans-serif;`

### 3.2 텍스트 스케일

| 용도 | Tailwind 클래스 | 크기 |
|------|----------------|------|
| 페이지 제목 | `text-2xl font-bold` | 24px |
| 섹션 제목 | `text-xl font-semibold` | 20px |
| 게시글 제목 | `text-lg font-medium` | 18px |
| 본문 | `text-base` | 16px |
| 보조 텍스트 | `text-sm text-gray-500` | 14px |
| 메타 정보 | `text-xs text-gray-400` | 12px |

---

## 4. 컴포넌트 디자인 가이드

### 4.1 버튼

```html
<!-- Primary — 주요 행동 -->
<button class="bg-indigo-600 hover:bg-indigo-700 text-white
               font-medium px-4 py-2 rounded-lg transition-colors">
  게시글 작성
</button>

<!-- Secondary — 보조 행동 -->
<button class="border border-gray-300 hover:bg-gray-50 text-gray-700
               font-medium px-4 py-2 rounded-lg transition-colors">
  취소
</button>

<!-- Danger — 삭제·취소 -->
<button class="bg-red-500 hover:bg-red-600 text-white
               font-medium px-4 py-2 rounded-lg transition-colors">
  삭제
</button>

<!-- 비활성 상태 공통 추가 클래스 -->
<!-- opacity-50 cursor-not-allowed pointer-events-none -->
```

### 4.2 카드

```html
<!-- 게시글·공지 카드 -->
<div class="bg-white border border-gray-200 rounded-xl p-5
            hover:shadow-md transition-shadow cursor-pointer">
  <!-- 내용 -->
</div>
```

### 4.3 입력 필드

```html
<!-- 기본 상태 -->
<input class="w-full border border-gray-300 rounded-lg px-3 py-2
              focus:outline-none focus:ring-2 focus:ring-indigo-500
              focus:border-transparent text-gray-900 placeholder-gray-400">

<!-- 오류 상태 -->
<input class="w-full border border-red-400 rounded-lg px-3 py-2
              focus:outline-none focus:ring-2 focus:ring-red-400">
<p class="text-sm text-red-500 mt-1">오류 메시지를 여기에 표시</p>
```

### 4.4 알림 메시지 (Django messages 연동)

```html
<!-- 성공 -->
<div class="bg-emerald-50 border border-emerald-200 text-emerald-800
            rounded-lg px-4 py-3 flex items-center gap-2">
  ✅ 성공적으로 처리되었습니다.
</div>

<!-- 오류 -->
<div class="bg-red-50 border border-red-200 text-red-800
            rounded-lg px-4 py-3 flex items-center gap-2">
  ❌ 오류가 발생했습니다.
</div>
```

### 4.5 뱃지·태그

```html
<!-- 공지 핀 -->
<span class="bg-indigo-100 text-indigo-700 text-xs font-medium px-2 py-0.5 rounded">
  📌 공지
</span>

<!-- 조회수 -->
<span class="text-gray-400 text-sm flex items-center gap-1">👁 128</span>

<!-- 좋아요 -->
<span class="text-gray-400 text-sm flex items-center gap-1">❤️ 24</span>
```

---

## 5. 레이아웃 시스템

### 5.1 전체 페이지 구조

```
┌────────────────────────────────────────────┐
│           Navbar (sticky top, h-16)         │
├────────────────────────────────────────────┤
│                                            │
│          Main Content                      │
│          max-w-4xl mx-auto px-4 py-8      │
│                                            │
├────────────────────────────────────────────┤
│           Footer (py-8)                    │
└────────────────────────────────────────────┘
```

### 5.2 콘텐츠 최대 너비

| 영역 | Tailwind 클래스 |
|------|----------------|
| 일반 페이지 | `max-w-4xl mx-auto px-4` |
| 게시글 상세 | `max-w-3xl mx-auto px-4` |
| 관리자 대시보드 | `max-w-6xl mx-auto px-4` |
| 인증 폼 | `max-w-md mx-auto px-4` |

### 5.3 반응형 브레이크포인트

```
기본 (모바일)   375px~   단일 컬럼, 전체 너비
md:            768px~   여백 증가, 일부 2컬럼
lg:           1024px~   최대 너비 제한, 사이드바 가능
```

---

## 6. 네비게이션 바 구조

```
[CommUnity 로고]  공지사항  게시판  캘린더  투표     [로그인] or [닉네임 ▼]
```

- 현재 페이지: `text-indigo-600 font-semibold border-b-2 border-indigo-600`
- 모바일: 햄버거 메뉴로 전환
- 로그인 상태: 닉네임 드롭다운 → 내 프로필 / 로그아웃
- 관리자 로그인: 드롭다운에 '관리자 대시보드' 추가

---

## 7. 빈 상태 (Empty State) 필수 패턴

데이터가 없는 화면에는 반드시 아래 형태로 안내한다.

```html
<div class="text-center py-16">
  <div class="text-5xl mb-4">📭</div>
  <h3 class="text-lg font-medium text-gray-900 mb-2">아직 게시글이 없어요</h3>
  <p class="text-gray-500 mb-6">첫 번째 글을 작성해보세요!</p>
  <a href="{% url 'board:create' %}"
     class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors">
    글쓰기
  </a>
</div>
```

---

## 8. 접근성 체크리스트

```
✅ 모든 이미지에 alt 속성 필수
✅ 버튼·링크에 명확한 텍스트 또는 aria-label
✅ 폼 입력 필드와 label 연결 (for/id 쌍)
✅ 색상만으로 상태를 표현하지 않음 (아이콘 병행)
✅ 키보드 탭 순서가 논리적
✅ 텍스트 색상 대비 4.5:1 이상 (WCAG 2.1 AA)
```

---

## 9. 금지 사항

```
❌ 인라인 style="" 속성 (Tailwind 클래스로 대체)
❌ 팔레트 밖의 임의 색상 지정
❌ px 단위 폰트 크기 직접 지정 (Tailwind 스케일 사용)
❌ 테이블을 레이아웃 목적으로 사용 (flex/grid 사용)
❌ 빈 화면을 안내 없이 방치
❌ 오류 메시지 없는 폼 제출 실패 화면
❌ 모바일 미지원 레이아웃
```
