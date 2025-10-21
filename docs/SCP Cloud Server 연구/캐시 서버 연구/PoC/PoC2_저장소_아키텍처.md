# PoC #2: 저장소 아키텍처 검증

## Project Name

로컬 캐시 서버 데이터 저장소 설계 및 검증

## Date

2025-10-21 (예정)

## Submitter Info

Raymond

## Project Description

치과 클리닉용 로컬 캐시 서버의 저장소 아키텍처를 검증한다. **기술 검증 목적**: 파일시스템, PostgreSQL, Redis, RocksDB 등 다양한 저장소 옵션의 성능을 비교 측정하여 최적 조합을 선정하고, 향후 프로덕션 개발 시 저장소 기술 스택을 확정한다.

## Business and Marketing Justification

**PoC 검증 가치:**

- 저장소 옵션별 성능 비교 (I/O 처리량, 지연시간, 메모리 사용량)
- 치과 이미지 특성에 맞는 최적 저장소 조합 도출
- 향후 프로덕션 개발 시 저장소 기술 스택 확정

**핵심 요구사항:**

- 치과 이미지 파일: 중소용량(1-50MB), 높은 압축률, 순차 읽기 중심
  - X-ray: 1-5MB (자주 참조)
  - CT: 10-50MB (치료 계획용)
  - 구강 스캔: 5-20MB (임시 데이터)
  - 썸네일: 50-200KB
- 메타데이터: 소용량(KB), 빈번한 조회/갱신, 치과 전용 쿼리 기능
- 캐시 정책: LRU/SLRU 제거, TTL 관리, 치료 단계별 무효화
- **Windows 설치 호환성**: 바이너리 배포, 의존성 관리, 서비스 등록

**성공 기준:**

- 치과 이미지 조회 지연: 95p < 50ms
- 메타데이터 조회: 95p < 10ms
- 디스크 사용 효율: 200GB에 환자 200명 이상 캐싱 (치과 이미지는 상대적으로 작음)

## Risk Assessment

**기술 리스크:**

- 파일시스템: inode 제한, 디렉터리 구조 복잡도, 메타데이터 관리 오버헤드
- SQLite: 동시 쓰기 제한, 파일 잠금 이슈
- RocksDB: 학습 곡선, 압축 튜닝 필요
- Redis: 메모리 제약, 영속성 설정
- **Windows 설치 리스크**: SQLite/Redis/RocksDB Windows 바이너리 안정성, 의존성 관리

**성능 리스크:**

- 대용량 파일 I/O가 메타데이터 조회에 영향
- 캐시 제거 시 디스크 단편화
- 동시 접속 시 락 경합

**완화 전략:**

- 미디어와 메타를 별도 저장소로 분리
- 핫 데이터는 인메모리 캐시 활용
- 비동기 I/O 및 버퍼링 적용

## Resource and Scheduling Details

**기간:** 2주 (Week 1-2, PoC #1과 병렬)

**인력:**

- 개발자 1명 (Raymond) - 저장소 구현, 테스트 및 성능 분석

**일정:**

- Day 1-2: 요구사항 분석 및 옵션 정리
- Day 3-5: 미디어 저장소 옵션 구현
  - 파일시스템 (해시 기반 디렉터리 구조)
  - RocksDB (키-값 저장)
- Day 6-8: 메타데이터 저장소 옵션 구현
  - SQLite (관계형 스키마)
  - RocksDB (JSON 직렬화)
  - Redis (인메모리 + AOF)
- Day 9-11: 성능 벤치마크 및 비교
- Day 12: 최종 아키텍처 결정 및 문서화

**리소스:**

- 개발 서버 1대 (다양한 디스크 타입 테스트)
- 실제 데이터셋 (CT 100건, 환자 50명)
- 벤치마크 도구 (fio, sysbench)

## Technical Description

### 검증 대상

#### 1. 미디어 파일 저장소

**옵션 A: 파일시스템 (해시 기반 디렉터리)**

```
/var/cache/media/
  ├── thumb/
  │   ├── 00/
  │   │   ├── 00/
  │   │   │   └── {clinicId}_{studyId}_{hash}.jpg
  │   └── ff/
  └── preview/
      └── ...
```

- 장점: 단순, OS 캐시 활용, 백업 용이
- 단점: 파일 수 제한(inode), 메타 관리 별도 필요

**옵션 B: RocksDB**

```
Key:   clinic:{clinicId}:study:{studyId}:thumb
Value: <binary data>
```

- 장점: 압축, 빠른 조회, 메타데이터 함께 저장
- 단점: 큰 파일 비효율, 압축 오버헤드

**평가 기준:**

- 쓰기 성능 (100MB 파일 저장)
- 읽기 성능 (랜덤/순차 조회)
- 디스크 사용량 (압축률)
- 캐시 제거 성능 (LRU)

#### 2. 메타데이터 저장소

**옵션 A: PostgreSQL (권장)**

```sql
CREATE TABLE cache_metadata (
  clinic_id VARCHAR(50),
  patient_id VARCHAR(50),
  study_id VARCHAR(50),
  cache_key VARCHAR(255) PRIMARY KEY,
  ttl BIGINT,
  last_access BIGINT,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_clinic_resource ON cache_metadata(clinic_id, last_access);
CREATE INDEX idx_ttl ON cache_metadata(ttl);
```

- 장점: SQL 쿼리, 트랜잭션, 범위 검색, 동시성 우수, JSONB 지원
- 단점: 별도 서버 필요, 메모리 사용량 높음
- **기존 인프라 활용**: 이미 사용 중인 PostgreSQL 서버 활용 가능

**옵션 B: SQLite (제외)**

```sql
CREATE TABLE cache_metadata (
  clinic_id TEXT,
  patient_id TEXT,
  study_id TEXT,
  cache_key TEXT PRIMARY KEY,
  ttl INTEGER,
  last_access INTEGER,
  metadata JSON
);
```

- 장점: SQL 쿼리, 트랜잭션, 범위 검색
- 단점: **동시 쓰기 제한, 파일 잠금, 데이터 손실 위험**
- **결론**: 프로덕션 환경에서 사용 부적합

**옵션 C: RocksDB**

```
Key:   cache:meta:{clinicId}:{patientId}:{studyId}
Value: {"ttl": ..., "lastAccess": ..., "data": {...}}
```

- 장점: 빠른 쓰기, 동시성 우수
- 단점: 쿼리 제한, 범위 검색 비효율

**옵션 D: Redis (인메모리)**

```
HSET cache:meta:{key} ttl 3600 lastAccess 1234567890 data {...}
```

- 장점: 초고속 조회, TTL 내장, Pub/Sub
- 단점: 메모리 제약, 영속성 설정 필요

**평가 기준:**

- 조회 성능 (10,000 req/s)
- 쓰기 성능 (무효화/갱신)
- 메모리 사용량
- TTL 만료 처리 효율

#### 3. 하이브리드 아키텍처

**권장 조합:**

- 미디어: 파일시스템 (단순성, OS 캐시)
- 메타: PostgreSQL (쿼리 기능, 기존 인프라 활용) + Redis (핫 데이터 인메모리)

```
[Request] → [Redis (Hot)] → [PostgreSQL (Warm)] → [파일시스템 (Cold)]
```

### 성능 테스트 시나리오

**시나리오 1: 미디어 쓰기**

- 100개의 10MB 썸네일 순차 저장
- 측정: 쓰기 처리량(MB/s), 지연시간

**시나리오 2: 미디어 읽기**

- 1,000번의 랜덤 파일 조회
- 측정: 캐시 히트율, 읽기 지연(50/95/99p)

**시나리오 3: 메타데이터 조회**

- 10,000 req/s로 환자 요약 조회
- 측정: 처리량, 지연시간, CPU/메모리

**시나리오 4: 혼합 워크로드**

- 읽기 80% + 쓰기 15% + 무효화 5%
- 측정: 종합 성능 및 안정성

**시나리오 5: 캐시 제거**

- LRU 정책으로 50GB 데이터 제거
- 측정: 제거 속도, 디스크 단편화

### 스키마 설계

#### PostgreSQL 스키마 (메타데이터)

```sql
-- 캐시 엔트리
CREATE TABLE cache_entries (
  cache_key VARCHAR(255) PRIMARY KEY,
  clinic_id VARCHAR(50) NOT NULL,
  resource_type VARCHAR(20) NOT NULL,  -- 'thumb', 'preview', 'meta'
  resource_id VARCHAR(100) NOT NULL,
  ttl BIGINT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_access TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  access_count INTEGER DEFAULT 0,
  size_bytes BIGINT,
  metadata JSONB
);

CREATE INDEX idx_clinic_resource ON cache_entries(clinic_id, resource_type, last_access);
CREATE INDEX idx_ttl ON cache_entries(ttl);
CREATE INDEX idx_metadata_gin ON cache_entries USING GIN (metadata);

-- 무효화 로그
CREATE TABLE invalidation_log (
  id SERIAL PRIMARY KEY,
  pattern VARCHAR(255) NOT NULL,
  invalidated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  reason TEXT
);

-- 스풀 큐 (write-back)
CREATE TABLE spool_queue (
  id SERIAL PRIMARY KEY,
  resource_id VARCHAR(100) NOT NULL,
  operation VARCHAR(20) NOT NULL,  -- 'upload', 'delete'
  payload BYTEA,
  retry_count INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(20) DEFAULT 'pending'  -- 'pending', 'processing', 'done', 'failed'
);
```

#### 파일시스템 구조 (미디어)

```
/var/cache/scp/
  ├── media/
  │   ├── thumb/
  │   │   └── {hash[0:2]}/{hash[2:4]}/{clinicId}_{studyId}_{hash}.jpg
  │   ├── preview/
  │   │   └── {hash[0:2]}/{hash[2:4]}/{clinicId}_{studyId}_{hash}.jp2
  │   └── raw/
  │       └── {hash[0:2]}/{hash[2:4]}/{clinicId}_{studyId}_{hash}.dcm
  ├── meta/
  │   └── cache.db  (PostgreSQL 연결 정보)
  └── spool/
      └── {resourceId}.tmp
```

### 구현 샘플

#### 파일시스템 + PostgreSQL 조합

```python
import psycopg2
import hashlib
from pathlib import Path

class CacheStorage:
    def __init__(self, base_path="/var/cache/scp", db_config=None):
        self.base_path = Path(base_path)
        # PostgreSQL 연결 (기존 서버 활용)
        self.db = psycopg2.connect(
            host=db_config.get('host', 'localhost'),
            database=db_config.get('database', 'scp_cache'),
            user=db_config.get('user', 'scp_user'),
            password=db_config.get('password')
        )

    def store_media(self, clinic_id, study_id, data, media_type="thumb"):
        # 파일 경로 생성
        hash_key = hashlib.sha256(f"{clinic_id}:{study_id}".encode()).hexdigest()
        file_path = self._get_file_path(hash_key, media_type)

        # 파일 저장
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(data)

        # 메타데이터 저장
        cache_key = f"{clinic_id}:{study_id}:{media_type}"
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO cache_entries
            (cache_key, clinic_id, resource_type, resource_id, ttl, last_access, size_bytes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (cache_key, clinic_id, media_type, study_id,
              int(time.time()) + 2592000,  # 30일 TTL
              int(time.time()), len(data)))
        self.db.commit()

    def get_media(self, clinic_id, study_id, media_type="thumb"):
        # 메타데이터 조회
        cache_key = f"{clinic_id}:{study_id}:{media_type}"
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT * FROM cache_entries WHERE cache_key = %s",
            (cache_key,)
        )
        row = cursor.fetchone()

        if not row or row[4] < int(time.time()):  # ttl 컬럼
            return None  # MISS or Expired

        # 파일 조회
        hash_key = hashlib.sha256(f"{clinic_id}:{study_id}".encode()).hexdigest()
        file_path = self._get_file_path(hash_key, media_type)

        if not file_path.exists():
            return None

        # 접근 시간 업데이트
        cursor.execute(
            "UPDATE cache_entries SET last_access = %s, access_count = access_count + 1 WHERE cache_key = %s",
            (int(time.time()), cache_key)
        )
        self.db.commit()

        return file_path.read_bytes()

    def _get_file_path(self, hash_key, media_type):
        return self.base_path / "media" / media_type / hash_key[0:2] / hash_key[2:4] / f"{hash_key}.bin"
```

#### Redis 예시 (핫 데이터 캐시)

```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def set_hot_cache(clinic_id, uri, data, ttl_seconds):
    key = f"hot:{clinic_id}:{uri}"
    value = json.dumps(data)
    r.setex(key, ttl_seconds, value)

def get_hot_cache(clinic_id, uri):
    key = f"hot:{clinic_id}:{uri}"
    value = r.get(key)
    return json.loads(value) if value else None

# PostgreSQL과 연동하여 핫 데이터만 Redis에 캐시
def get_meta_with_cache(clinic_id, uri):
    # 1. Redis에서 먼저 확인
    hot_data = get_hot_cache(clinic_id, uri)
    if hot_data:
        return hot_data

    # 2. PostgreSQL에서 조회
    pg_data = get_from_postgresql(clinic_id, uri)
    if pg_data:
        # 3. Redis에 캐시 (5분 TTL)
        set_hot_cache(clinic_id, uri, pg_data, 300)

    return pg_data
```

### 벤치마크 결과 템플릿

| 저장소 조합             | 쓰기 (MB/s) | 읽기 (ms, 95p) | 메타 조회 (ms) | 디스크 효율 | 점수 |
| ----------------------- | ----------- | -------------- | -------------- | ----------- | ---- |
| FS + PostgreSQL         | ?           | ?              | ?              | ?           | ?    |
| FS + PostgreSQL + Redis | ?           | ?              | ?              | ?           | ?    |
| RocksDB                 | ?           | ?              | ?              | ?           | ?    |
| FS + RocksDB            | ?           | ?              | ?              | ?           | ?    |

### PoC 검증 결과 및 의사결정 기준

**검증 목표:**

- 각 저장소 옵션별 성능 측정 (쓰기/읽기 속도, 메모리 사용량)
- 치과 이미지 특성에 맞는 최적화 효과 검증
- 운영 복잡도 및 유지보수성 평가

**PoC 성공 기준:**

- 명확한 성능 차이 측정 (20% 이상 차이 시 의미 있음)
- 저장소 조합별 장단점 정량화
- 기술적 의사결정 근거 문서화
- 프로덕션 개발 시 저장소 선택 가이드라인 제시

**의사결정:**

- PoC 결과 기반 저장소 조합 선정
- 치과 이미지 특성에 최적화된 아키텍처 도출
- 향후 프로덕션 개발 시 고려사항 정리

## 5. 개발 언어 고려사항

### 5.1 저장소 인터페이스 구현 언어

**Go (권장):**

- **장점**: PostgreSQL 드라이버 우수, 고성능 I/O
- **적합성**: 파일 시스템 조작, 데이터베이스 연동
- **라이브러리**: github.com/lib/pq (PostgreSQL), filepath, os

**Python (대안):**

- **장점**: 풍부한 PostgreSQL 라이브러리, 빠른 개발
- **라이브러리**: psycopg2 (PostgreSQL), pathlib, os
- **단점**: 성능 제한, 의존성 관리

### 5.2 캐시 관리 로직 구현 언어

**Go (권장):**

- **장점**: 고루틴으로 동시 처리, 메모리 효율성
- **적합성**: LRU/LFU 알고리즘, 캐시 정책 관리

**C++ (고성능):**

- **장점**: 최고 성능, 메모리 직접 제어
- **단점**: 개발 복잡성, 디버깅 어려움

### 5.3 라이선스 고려사항

**PostgreSQL:**

- **라이선스**: PostgreSQL License (MIT-style)
- **상업적 사용**: ✅ 허용 (제약 없음)
- **수정/배포**: ✅ 허용 (제약 없음)
- **고지 의무**: ❌ 없음

**Redis:**

- **라이선스**: BSD 3-clause License
- **상업적 사용**: ✅ 허용
- **수정/배포**: ✅ 허용
- **고지 의무**: ✅ 저작권 고지 유지

**RocksDB:**

- **라이선스**: Apache License 2.0
- **상업적 사용**: ✅ 허용
- **수정/배포**: ✅ 허용
- **고지 의무**: ✅ 라이선스 파일 포함

**Go 언어:**

- **라이선스**: BSD 3-clause License
- **상업적 사용**: ✅ 허용
- **수정/배포**: ✅ 허용
- **고지 의무**: ✅ 저작권 고지 유지

### 5.4 Windows 설치 호환성 고려사항

**PostgreSQL Windows 배포:**

- **연결**: 기존 PostgreSQL 서버에 연결
- **의존성**: PostgreSQL 클라이언트 라이브러리 (libpq)
- **설치**: 클라이언트 라이브러리만 포함
- **서비스**: 별도 서비스 불필요 (클라이언트 연결)

**Redis Windows 배포:**

- **바이너리**: 공식 Windows 바이너리 제공
- **의존성**: Visual C++ Redistributable 필요
- **서비스 등록**: redis-server.exe를 Windows 서비스로 등록 가능
- **설정 파일**: redis.conf Windows 경로 지원

**RocksDB Windows 배포:**

- **바이너리**: 정적 링크 또는 DLL 형태
- **의존성**: Visual C++ Redistributable 필요
- **설치**: 라이브러리 형태로 애플리케이션에 포함
- **서비스**: 별도 서비스 불필요 (라이브러리 형태)

**Go 애플리케이션 Windows 배포:**

- **바이너리**: 단일 실행 파일로 컴파일 가능
- **의존성**: PostgreSQL 클라이언트 라이브러리 (libpq.dll)
- **서비스 등록**: go-svc 라이브러리로 Windows 서비스 구현
- **설정 파일**: JSON/YAML 설정 파일 지원

### 다음 단계

선정된 저장소 구조로 PoC #4 통합 프로토타입에 적용
