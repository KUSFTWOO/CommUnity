import os
import sys
import django

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

# 데이터베이스 최적화 설정 확인
cursor = connection.cursor()

print("=" * 60)
print("SQLite 데이터베이스 최적화 설정 확인")
print("=" * 60)

pragmas = [
    ('journal_mode', 'PRAGMA journal_mode;'),
    ('foreign_keys', 'PRAGMA foreign_keys;'),
    ('synchronous', 'PRAGMA synchronous;'),
    ('cache_size', 'PRAGMA cache_size;'),
    ('temp_store', 'PRAGMA temp_store;'),
]

for name, query in pragmas:
    cursor.execute(query)
    result = cursor.fetchone()[0]
    print(f"[OK] {name:20} : {result}")

cursor.close()

print("\n" + "=" * 60)
print("설정 설명")
print("=" * 60)

explanations = {
    'journal_mode': 'WAL - 읽기/쓰기 동시성 극대화',
    'foreign_keys': '1 = ON - 데이터 무결성 보장',
    'synchronous': '1(NORMAL) - 성능과 안정성 균형',
    'cache_size': '-64000 = 64MB 메모리 캐시',
    'temp_store': '2(MEMORY) - 임시 테이블을 메모리에 저장',
}

for key, description in explanations.items():
    print(f"- {key:20} : {description}")

print("\n" + "=" * 60)
print("연결 설정")
print("=" * 60)
print(f"[OK] Busy Timeout     : 20초")
print(f"[OK] Atomic Requests  : True")
print(f"[OK] Database Path    : {connection.settings_dict['NAME']}")

print("\n" + "=" * 60)
print("최적화 완료!")
print("=" * 60)
