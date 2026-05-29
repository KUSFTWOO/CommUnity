# DD — Database Design
## 데이터베이스 스키마, 관계, 인덱스 설계

> 버전: 1.0.0
> ORM: Django ORM (내장)
> DB: SQLite (개발) → PostgreSQL (프로덕션)
> 참고: 이 프로젝트는 Django ORM을 사용합니다.
>       Prisma 문법이 아닌 Django models.py 형식으로 스키마를 정의합니다.

---

## 1. ERD 개요 (엔티티 관계 다이어그램)

```
CustomUser ──< Post ──< PostImage
           ──< Comment (자기 참조 — 대댓글)
           ──< PostLike
           ──< VoteResponse

Post ──< Comment
     ──< PostLike

Notice (단독)

Event (단독)

Vote ──< VoteOption ──< VoteResponse
```

---

## 2. 테이블 상세 설계

### 2.1 CustomUser (회원)

> `django.contrib.auth.AbstractUser` 확장

```python
class CustomUser(AbstractUser):
    # AbstractUser가 제공하는 기본 필드
    # username, email, password, first_name, last_name
    # is_staff, is_active, is_superuser, date_joined, last_login

    # 추가 필드
    nickname     = CharField(max_length=30, unique=True)
    bio          = CharField(max_length=150, blank=True)
    profile_image = ImageField(upload_to='profiles/%Y/%m/', blank=True, null=True)
    login_fail_count = PositiveSmallIntegerField(default=0)
    locked_until    = DateTimeField(null=True, blank=True)
    is_deleted      = BooleanField(default=False)   # 소프트 삭제

    USERNAME_FIELD  = 'email'   # 이메일로 로그인
    REQUIRED_FIELDS = ['username', 'nickname']

    class Meta:
        db_table = 'accounts_customuser'
        indexes = [
            Index(fields=['email']),
            Index(fields=['nickname']),
        ]
```

**필드 설명**

| 필드 | 타입 | 설명 |
|------|------|------|
| id | AutoField (PK) | 자동 증가 기본키 |
| email | EmailField UNIQUE | 로그인 식별자 |
| nickname | CharField(30) UNIQUE | 표시 이름 |
| bio | CharField(150) | 한 줄 소개 |
| profile_image | ImageField | 프로필 사진 |
| login_fail_count | SmallInt | 연속 로그인 실패 횟수 |
| locked_until | DateTime NULL | 계정 잠금 해제 시각 |
| is_staff | Boolean | 관리자 여부 |
| is_active | Boolean | 활성 계정 여부 |
| is_deleted | Boolean | 소프트 삭제 여부 |
| date_joined | DateTime | 가입일시 |

---

### 2.2 Notice (공지사항)

```python
class Notice(models.Model):
    title      = CharField(max_length=200)
    content    = TextField()
    author     = ForeignKey(CustomUser, on_delete=SET_NULL, null=True, related_name='notices')
    is_pinned  = BooleanField(default=False)    # 상단 고정
    is_deleted = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']
        indexes  = [Index(fields=['-is_pinned', '-created_at'])]
```

**필드 설명**

| 필드 | 타입 | 설명 |
|------|------|------|
| id | AutoField (PK) | |
| title | CharField(200) | 공지 제목 |
| content | TextField | 공지 내용 |
| author | FK → CustomUser | 작성자 |
| is_pinned | Boolean | 상단 고정 여부 |
| is_deleted | Boolean | 소프트 삭제 |
| created_at | DateTime | 작성일시 |
| updated_at | DateTime | 수정일시 |

---

### 2.3 NoticeFile (공지 첨부파일)

```python
class NoticeFile(models.Model):
    notice    = ForeignKey(Notice, on_delete=CASCADE, related_name='files')
    file      = FileField(upload_to='notices/%Y/%m/%d/')
    filename  = CharField(max_length=255)   # 원본 파일명
    file_size = PositiveIntegerField()      # bytes
    created_at = DateTimeField(auto_now_add=True)
```

---

### 2.4 Post (게시글)

```python
class Post(models.Model):
    title      = CharField(max_length=200)
    content    = TextField()
    author     = ForeignKey(CustomUser, on_delete=SET_NULL, null=True, related_name='posts')
    view_count = PositiveIntegerField(default=0)
    is_deleted = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes  = [
            Index(fields=['-created_at']),
            Index(fields=['author']),
        ]

    # 좋아요 수 (역참조 집계)
    @property
    def like_count(self):
        return self.likes.count()

    # 댓글 수 (역참조 집계)
    @property
    def comment_count(self):
        return self.comments.filter(is_deleted=False).count()
```

**필드 설명**

| 필드 | 타입 | 설명 |
|------|------|------|
| id | AutoField (PK) | |
| title | CharField(200) | 게시글 제목 |
| content | TextField | 게시글 내용 |
| author | FK → CustomUser | 작성자 |
| view_count | PositiveInt | 조회수 |
| is_deleted | Boolean | 소프트 삭제 |
| created_at | DateTime | 작성일시 |
| updated_at | DateTime | 수정일시 |

---

### 2.5 PostImage (게시글 이미지)

```python
class PostImage(models.Model):
    post       = ForeignKey(Post, on_delete=CASCADE, related_name='images')
    image      = ImageField(upload_to='posts/%Y/%m/%d/')
    order      = PositiveSmallIntegerField(default=0)   # 표시 순서
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
```

---

### 2.6 Comment (댓글·대댓글)

```python
class Comment(models.Model):
    post       = ForeignKey(Post, on_delete=CASCADE, related_name='comments')
    author     = ForeignKey(CustomUser, on_delete=SET_NULL, null=True, related_name='comments')
    parent     = ForeignKey(
        'self', on_delete=CASCADE,
        null=True, blank=True,
        related_name='replies'
    )                                        # NULL이면 댓글, 값이 있으면 대댓글
    content    = TextField()
    is_deleted = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        indexes  = [
            Index(fields=['post', 'created_at']),
            Index(fields=['parent']),
        ]
```

**자기 참조 관계 설명**

```
Comment (id=1, parent=None)       ← 댓글
    └── Comment (id=3, parent=1)  ← 대댓글
    └── Comment (id=5, parent=1)  ← 대댓글

대댓글의 대댓글은 허용하지 않음 (parent가 None인 댓글만 parent가 될 수 있음)
```

---

### 2.7 PostLike (게시글 좋아요)

```python
class PostLike(models.Model):
    post       = ForeignKey(Post, on_delete=CASCADE, related_name='likes')
    user       = ForeignKey(CustomUser, on_delete=CASCADE, related_name='liked_posts')
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['post', 'user']]   # 중복 좋아요 방지
        indexes = [Index(fields=['post', 'user'])]
```

---

### 2.8 Event (캘린더 일정)

```python
class Event(models.Model):
    COLOR_CHOICES = [
        ('indigo', '인디고'),
        ('red',    '빨강'),
        ('green',  '초록'),
        ('yellow', '노랑'),
        ('purple', '보라'),
    ]

    title       = CharField(max_length=100)
    description = TextField(blank=True)
    start_date  = DateField()
    end_date    = DateField()
    color       = CharField(max_length=20, choices=COLOR_CHOICES, default='indigo')
    author      = ForeignKey(CustomUser, on_delete=SET_NULL, null=True, related_name='events')
    created_at  = DateTimeField(auto_now_add=True)
    updated_at  = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date']
        indexes  = [Index(fields=['start_date', 'end_date'])]
```

---

### 2.9 Vote (투표)

```python
class Vote(models.Model):
    VOTE_TYPE_CHOICES = [
        ('single',   '단일 선택'),
        ('multiple', '복수 선택'),
    ]

    title       = CharField(max_length=200)
    description = TextField(blank=True)
    vote_type   = CharField(max_length=10, choices=VOTE_TYPE_CHOICES, default='single')
    is_anonymous = BooleanField(default=False)
    is_active   = BooleanField(default=True)
    start_at    = DateTimeField()
    end_at      = DateTimeField()
    author      = ForeignKey(CustomUser, on_delete=SET_NULL, null=True, related_name='votes')
    created_at  = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes  = [Index(fields=['start_at', 'end_at'])]

    @property
    def is_ongoing(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_at <= now <= self.end_at and self.is_active
```

---

### 2.10 VoteOption (투표 선택지)

```python
class VoteOption(models.Model):
    vote  = ForeignKey(Vote, on_delete=CASCADE, related_name='options')
    text  = CharField(max_length=200)
    order = PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']
```

---

### 2.11 VoteResponse (투표 응답)

```python
class VoteResponse(models.Model):
    vote   = ForeignKey(Vote, on_delete=CASCADE, related_name='responses')
    option = ForeignKey(VoteOption, on_delete=CASCADE, related_name='responses')
    user   = ForeignKey(CustomUser, on_delete=CASCADE, related_name='vote_responses')
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        # 단일 선택: (vote, user) 유일
        # 복수 선택: (vote, user, option) 유일
        unique_together = [['vote', 'user', 'option']]
        indexes = [Index(fields=['vote', 'user'])]
```

---

## 3. 관계 요약

```
CustomUser  1 ── N  Post
CustomUser  1 ── N  Comment
CustomUser  1 ── N  PostLike
CustomUser  1 ── N  Notice
CustomUser  1 ── N  Event
CustomUser  1 ── N  Vote
CustomUser  1 ── N  VoteResponse

Post        1 ── N  PostImage
Post        1 ── N  Comment
Post        1 ── N  PostLike

Comment     1 ── N  Comment     (자기 참조, 대댓글)

Vote        1 ── N  VoteOption
VoteOption  1 ── N  VoteResponse

Notice      1 ── N  NoticeFile
```

---

## 4. 인덱스 설계

| 테이블 | 인덱스 컬럼 | 목적 |
|--------|------------|------|
| CustomUser | email | 로그인 조회 |
| CustomUser | nickname | 닉네임 중복 확인 |
| Post | -created_at | 최신순 목록 |
| Post | author | 사용자별 게시글 |
| Comment | post, created_at | 게시글별 댓글 목록 |
| Comment | parent | 대댓글 조회 |
| PostLike | post, user | 좋아요 중복 확인 (UNIQUE) |
| Event | start_date, end_date | 월별 일정 조회 |
| Vote | start_at, end_at | 진행 중인 투표 필터 |
| VoteResponse | vote, user | 투표 참여 여부 확인 |
| Notice | -is_pinned, -created_at | 핀 고정 + 최신순 정렬 |

---

## 5. 마이그레이션 전략

```bash
# 새 Model 또는 필드 추가 후
python manage.py makemigrations

# 마이그레이션 내용 미리 확인
python manage.py sqlmigrate 앱이름 0001

# 실제 DB 반영
python manage.py migrate
```

### SQLite → PostgreSQL 전환 시

settings.py에서 DATABASES 설정만 변경하면 됩니다.
ORM 코드나 마이그레이션 파일은 그대로 사용 가능합니다.

```python
# 개발 (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 프로덕션 (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

---

## 6. 소프트 삭제 정책

```
삭제 대상      처리 방법
─────────────────────────────────────────────
회원           is_active=False (Django 기본)
               is_deleted=True (추가 필드)
게시글         is_deleted=True
댓글           is_deleted=True
공지사항       is_deleted=True

모든 삭제는 소프트 삭제로 처리하여 데이터를 보존합니다.
조회 시 항상 is_deleted=False 필터를 포함해야 합니다.

Hard Delete(실제 삭제)는 관리자가 Django Admin에서만 수행 가능합니다.
```
