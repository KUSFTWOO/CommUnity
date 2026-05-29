"""
SQLite 데이터베이스 최적화 설정
- WAL(Write-Ahead Logging) 모드 활성화
- 외래 키(Foreign Key) 제약 조건 활성화
"""

from django.db.backends.signals import connection_created
from django.dispatch import receiver


@receiver(connection_created)
def setup_sqlite(sender, connection, **kwargs):
    """SQLite 연결 시 최적화 설정 적용"""
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()

        # WAL 모드 활성화: 읽기/쓰기 동시성 극대화
        cursor.execute('PRAGMA journal_mode=WAL;')

        # 외래 키 제약 조건 활성화: 데이터 무결성 보장
        cursor.execute('PRAGMA foreign_keys=ON;')

        # 추가 최적화 설정들
        # Synchronous 모드: NORMAL로 설정 (성능과 안정성 균형)
        cursor.execute('PRAGMA synchronous=NORMAL;')

        # Cache size 설정: 캐시 메모리 증가 (성능 향상)
        cursor.execute('PRAGMA cache_size=-64000;')  # 64MB

        # TEMP_STORE: 메모리에 임시 테이블 저장 (성능 향상)
        cursor.execute('PRAGMA temp_store=MEMORY;')

        cursor.close()
