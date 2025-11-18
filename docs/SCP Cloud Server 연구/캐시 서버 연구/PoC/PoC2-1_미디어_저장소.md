# PoC #2-1: 미디어 저장소 아키텍처 검증

## Project Name

로컬 캐시 서버 미디어 저장소 설계 및 검증

## Date

2025-10-21 (예정)

## Submitter Info

Raymond

## Project Description

치과 클리닉용 로컬 캐시 서버의 **미디어 저장소** 아키텍처를 검증한다. **기술 검증 목적**: 파일시스템, RocksDB, MinIO 등 다양한 저장소 옵션의 성능을 비교 측정하여 최적 선택을 확정하고, 향후 프로덕션 개발 시 미디어 저장소 기술 스택을 확정한다.

## Business and Marketing Justification

**PoC 검증 가치:**

- 미디어 저장소 옵션별 성능 비교 (I/O 처리량, 지연시간, 메모리 사용량)
- 치과 이미지 특성에 맞는 최적 저장소 선택
- 향후 프로덕션 개발 시 미디어 저장소 기술 스택 확정

**핵심 요구사항:**

- 치과 이미지 파일: 중소용량(1-50MB), 높은 압축률, 순차 읽기 중심
  - X-ray: 1-5MB (자주 참조)
  - CT: 10-50MB (치료 계획용)
  - 구강 스캔: 5-20MB (임시 데이터)
  - 썸네일: 50-200KB
- **Windows 설치 호환성**: 바이너리 배포, 의존성 관리, 서비스 등록

**성공 기준:**

- 치과 이미지 조회 지연: 95p < 50ms
- 디스크 사용 효율: 200GB에 환자 200명 이상 캐싱

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

**체크리스트(작업 순서):**

**미디어 저장소 (완료):**

- [x] 요구사항 분석 및 후보 옵션 정리(미디어/메타 구분, 성능/운영 기준 정의)
- [x] Docker 환경 구성 (파일시스템, MinIO)
- [x] 미디어 저장소: 파일시스템(해시 디렉터리) 프로토타입 구현 및 벤치마크
- [ ] 미디어 저장소: RocksDB(키-값, 압축/블록 옵션) - 컴파일 실패로 제외
- [x] 미디어 저장소: MinIO(S3 API, 메타데이터, 라이프사이클) 프로토타입 구현 및 벤치마크
- [x] 성능 벤치마크 도구 개발 (Python - 미디어 저장소용)
- [x] 실제 성능 측정 및 비교(쓰기/읽기/메모리, 95/99p 지표 - 미디어 저장소)
- [x] 최종 미디어 저장소 선정 및 문서화(파일시스템 선정)

**메타데이터 저장소 (미완료 - PoC #3로 분리 예정):**

- [ ] 메타 저장소: PostgreSQL(JSONB/인덱스, 동시성) 기능 비교 및 적합성 검토
- [ ] 메타 저장소: MongoDB(BSON, TTL 내장, 유연한 스키마) 기능 비교 및 적합성 검토
- [ ] 메타 저장소: Redis(인메모리+TTL, AOF 스냅샷) 기능 비교 및 적합성 검토
- [ ] 로컬 캐시 요구사항 기반 기능 비교표 작성
- [ ] 필요 시 성능 측정 (기능 요구사항 충족 후)
- [ ] 최종 메타데이터 저장소 선정 및 문서화

**클라우드 호환성 (옵션 - 제외):**

- [ ] 클라우드 호환성 테스트(MinIO ↔ AWS S3 동기화) - 로컬 캐시 전용으로 제외

**참고:**

- 현재 PoC #2는 **미디어 저장소만** 실측 완료
- 메타데이터 저장소는 **코드 샘플만 작성**되었고 실측은 미완료
- PostgreSQL, Redis 외 NoSQL(MongoDB 등) 추가 검토 필요

**리소스:**

- 개발 서버 1대 (다양한 디스크 타입 테스트)
- 실제 데이터셋 (CT 100건, 환자 50명)
- 벤치마크 도구 (fio, sysbench)

## Technical Description

### 검증 대상

#### 0. Docker 환경 구성

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  # MinIO Object Storage
  minio:
    image: minio/minio:latest
    container_name: poc2-minio
    ports:
      - '9000:9000'
      - '9001:9001'
    environment:
      MINIO_ROOT_USER: admin
      MINIO_ROOT_PASSWORD: password123
    command: server /data --console-address ":9001"
    volumes:
      - ./data/minio:/data
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:9000/minio/health/live']
      interval: 30s
      timeout: 20s
      retries: 3

  # PostgreSQL (메타데이터 저장소)
  postgres:
    image: postgres:15-alpine
    container_name: poc2-postgres
    ports:
      - '5432:5432'
    environment:
      POSTGRES_USER: scp_user
      POSTGRES_PASSWORD: scp_password
      POSTGRES_DB: scp_cache
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U scp_user']
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis (핫 데이터 캐시)
  redis:
    image: redis:7-alpine
    container_name: poc2-redis
    ports:
      - '6379:6379'
    command: redis-server --appendonly yes
    volumes:
      - ./data/redis:/data
    healthcheck:
      test: ['CMD', 'redis-cli', 'ping']
      interval: 10s
      timeout: 3s
      retries: 3
```

**벤치마크 컨테이너:**

```yaml
benchmark:
  build: ./benchmark
  container_name: poc2-benchmark
  depends_on:
    - minio
    - postgres
    - redis
  volumes:
    - ./data/filesystem:/benchmark/cache
    - ./benchmark:/benchmark
    - ./results:/results
  environment:
    MINIO_ENDPOINT: minio:9000
    POSTGRES_HOST: postgres
    REDIS_HOST: redis
```

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

**옵션 C: MinIO (S3-Compatible Object Storage)**

```
Bucket: scp-cache-{clinicId}
Object: thumb/{studyId}/{hash}.jpg
Metadata: x-amz-meta-ttl, x-amz-meta-access-time
```

- 장점: S3 API 호환 (클라우드 연동), 자체 메타데이터 관리, 버전 관리/라이프사이클 정책 내장
- 단점: HTTP 오버헤드, 별도 프로세스 필요, 작은 파일에서는 비효율
- 적합 케이스: 멀티 클리닉 동기화, 클라우드 하이브리드 구조

**평가 기준:**

- 쓰기 성능 (100MB 파일 저장)
- 읽기 성능 (랜덤/순차 조회)
- 디스크 사용량 (압축률)
- 캐시 제거 성능 (LRU)
- 클라우드 호환성 (S3 API)

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

**권장 조합 A: 순수 로컬 캐시**

- 미디어: 파일시스템 (단순성, OS 캐시)
- 메타: PostgreSQL (쿼리 기능, 기존 인프라 활용) + Redis (핫 데이터 인메모리)

```
[Request] → [Redis (Hot)] → [PostgreSQL (Warm)] → [파일시스템 (Cold)]
```

**권장 조합 B: 클라우드 하이브리드 (MinIO 활용)**

- 미디어: MinIO (S3 API, 클라우드 동기화)
- 메타: PostgreSQL (쿼리 기능) + Redis (핫 데이터)

```
[Request] → [Redis (Hot)] → [PostgreSQL (Meta)] → [MinIO (Local)] ↔ [AWS S3 (Cloud)]
```

**조합 B 장점:**

1. **클라우드 연동**: MinIO ↔ S3 양방향 동기화 (mc mirror)
2. **멀티 사이트**: 여러 클리닉 간 데이터 복제 가능
3. **재해 복구**: S3 백업으로 자동 복구
4. **확장성**: 로컬 용량 부족 시 S3로 티어링

**조합 B 단점:**

1. **복잡도**: MinIO 서버 추가 운영 필요
2. **성능**: HTTP 오버헤드 (파일시스템 대비 10-20% 느림)
3. **메모리**: MinIO 프로세스 200-500MB 사용

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

**시나리오 6: MinIO S3 호환성 (추가)**

- MinIO → AWS S3 동기화 (mc mirror 사용)
- 로컬 캐시 히트 시 MinIO 조회, MISS 시 S3 폴백
- 측정: 동기화 속도, API 호환성, 메타데이터 일관성

**시나리오 7: MinIO 멀티테넌시 (추가)**

- 10개 클리닉별 버킷 분리
- 동시 접근 시 격리 성능
- 측정: 버킷 간 간섭 없음, IAM 정책 효과

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

#### MinIO 예시 (S3-Compatible 저장소)

```python
from minio import Minio
from minio.error import S3Error
import json
from datetime import timedelta

class MinIOStorage:
    def __init__(self, endpoint="localhost:9000", access_key=None, secret_key=None):
        # MinIO 클라이언트 초기화
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False  # 로컬 환경
        )

    def ensure_bucket(self, clinic_id):
        bucket_name = f"scp-cache-{clinic_id}"
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
            # 라이프사이클 정책 설정 (30일 TTL)
            lifecycle_config = {
                "Rules": [{
                    "ID": "expire-old-objects",
                    "Status": "Enabled",
                    "Expiration": {"Days": 30}
                }]
            }
            self.client.set_bucket_lifecycle(bucket_name, lifecycle_config)
        return bucket_name

    def store_media(self, clinic_id, study_id, data, media_type="thumb"):
        bucket_name = self.ensure_bucket(clinic_id)
        object_name = f"{media_type}/{study_id}/{hash(study_id)}.bin"

        # 메타데이터 설정
        metadata = {
            "x-amz-meta-clinic-id": clinic_id,
            "x-amz-meta-study-id": study_id,
            "x-amz-meta-ttl": str(int(time.time()) + 2592000),
            "x-amz-meta-access-time": str(int(time.time()))
        }

        # 업로드
        self.client.put_object(
            bucket_name,
            object_name,
            io.BytesIO(data),
            length=len(data),
            metadata=metadata
        )

    def get_media(self, clinic_id, study_id, media_type="thumb"):
        bucket_name = f"scp-cache-{clinic_id}"
        object_name = f"{media_type}/{study_id}/{hash(study_id)}.bin"

        try:
            # 메타데이터 조회
            stat = self.client.stat_object(bucket_name, object_name)

            # TTL 확인
            ttl = int(stat.metadata.get("x-amz-meta-ttl", 0))
            if ttl < int(time.time()):
                return None  # Expired

            # 객체 다운로드
            response = self.client.get_object(bucket_name, object_name)
            data = response.read()

            # 접근 시간 업데이트 (메타데이터 복사)
            metadata = stat.metadata.copy()
            metadata["x-amz-meta-access-time"] = str(int(time.time()))
            self.client.copy_object(
                bucket_name, object_name,
                f"{bucket_name}/{object_name}",
                metadata=metadata,
                metadata_directive="REPLACE"
            )

            return data
        except S3Error as e:
            if e.code == "NoSuchKey":
                return None
            raise

# PostgreSQL과 함께 사용
def get_media_with_minio(clinic_id, study_id, media_type="thumb"):
    # 1. PostgreSQL에서 메타데이터 조회 (빠른 TTL/권한 검증)
    meta = get_meta_from_postgresql(clinic_id, study_id, media_type)
    if not meta or meta['ttl'] < int(time.time()):
        return None

    # 2. MinIO에서 실제 파일 조회
    storage = MinIOStorage()
    return storage.get_media(clinic_id, study_id, media_type)
```

### 벤치마크 도구 구현

#### 벤치마크 스크립트 (Python)

**benchmark/benchmark.py:**

```python
#!/usr/bin/env python3
import time
import os
import hashlib
import statistics
from pathlib import Path
from minio import Minio
import psycopg2
import redis
import rocksdb

class StorageBenchmark:
    def __init__(self):
        self.test_data_sizes = [
            (200 * 1024, "thumb"),      # 200KB 썸네일
            (20 * 1024 * 1024, "ct")    # 20MB CT 이미지
        ]
        self.iterations = 1000

    def generate_test_data(self, size):
        """테스트 데이터 생성"""
        return os.urandom(size)

    def benchmark_filesystem(self, base_path="/benchmark/cache"):
        """파일시스템 벤치마크"""
        results = {"write": [], "read": []}

        for size, data_type in self.test_data_sizes:
            print(f"[FileSystem] Testing {data_type} ({size} bytes)...")

            # 쓰기 테스트
            write_times = []
            for i in range(self.iterations):
                data = self.generate_test_data(size)
                hash_key = hashlib.sha256(f"clinic123:study{i}".encode()).hexdigest()

                # 경로 생성
                dir_path = Path(base_path) / data_type / hash_key[0:2] / hash_key[2:4]
                dir_path.mkdir(parents=True, exist_ok=True)
                file_path = dir_path / f"{hash_key}.bin"

                # 쓰기 시간 측정
                start = time.perf_counter()
                file_path.write_bytes(data)
                elapsed = (time.perf_counter() - start) * 1000  # ms
                write_times.append(elapsed)

            # 읽기 테스트
            read_times = []
            for i in range(self.iterations):
                hash_key = hashlib.sha256(f"clinic123:study{i}".encode()).hexdigest()
                file_path = Path(base_path) / data_type / hash_key[0:2] / hash_key[2:4] / f"{hash_key}.bin"

                start = time.perf_counter()
                data = file_path.read_bytes()
                elapsed = (time.perf_counter() - start) * 1000
                read_times.append(elapsed)

            results[data_type] = {
                "write": self.calculate_stats(write_times),
                "read": self.calculate_stats(read_times)
            }

        return results

    def benchmark_minio(self, endpoint="minio:9000"):
        """MinIO 벤치마크"""
        client = Minio(
            endpoint,
            access_key="admin",
            secret_key="password123",
            secure=False
        )

        # 버킷 생성
        bucket_name = "poc2-benchmark"
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)

        results = {}

        for size, data_type in self.test_data_sizes:
            print(f"[MinIO] Testing {data_type} ({size} bytes)...")

            # 쓰기 테스트
            write_times = []
            for i in range(self.iterations):
                data = self.generate_test_data(size)
                object_name = f"{data_type}/study{i}.bin"

                from io import BytesIO
                start = time.perf_counter()
                client.put_object(
                    bucket_name,
                    object_name,
                    BytesIO(data),
                    length=size
                )
                elapsed = (time.perf_counter() - start) * 1000
                write_times.append(elapsed)

            # 읽기 테스트
            read_times = []
            for i in range(self.iterations):
                object_name = f"{data_type}/study{i}.bin"

                start = time.perf_counter()
                response = client.get_object(bucket_name, object_name)
                data = response.read()
                response.close()
                response.release_conn()
                elapsed = (time.perf_counter() - start) * 1000
                read_times.append(elapsed)

            results[data_type] = {
                "write": self.calculate_stats(write_times),
                "read": self.calculate_stats(read_times)
            }

        return results

    def benchmark_rocksdb(self, db_path="/benchmark/cache/rocksdb"):
        """RocksDB 벤치마크"""
        opts = rocksdb.Options()
        opts.create_if_missing = True
        opts.compression = rocksdb.CompressionType.lz4_compression

        db = rocksdb.DB(db_path, opts)
        results = {}

        for size, data_type in self.test_data_sizes:
            print(f"[RocksDB] Testing {data_type} ({size} bytes)...")

            # 쓰기 테스트
            write_times = []
            for i in range(self.iterations):
                data = self.generate_test_data(size)
                key = f"clinic123:study{i}:{data_type}".encode()

                start = time.perf_counter()
                db.put(key, data)
                elapsed = (time.perf_counter() - start) * 1000
                write_times.append(elapsed)

            # 읽기 테스트
            read_times = []
            for i in range(self.iterations):
                key = f"clinic123:study{i}:{data_type}".encode()

                start = time.perf_counter()
                data = db.get(key)
                elapsed = (time.perf_counter() - start) * 1000
                read_times.append(elapsed)

            results[data_type] = {
                "write": self.calculate_stats(write_times),
                "read": self.calculate_stats(read_times)
            }

        return results

    def calculate_stats(self, times):
        """통계 계산"""
        times_sorted = sorted(times)
        return {
            "mean": statistics.mean(times),
            "median": statistics.median(times),
            "p50": times_sorted[int(len(times) * 0.50)],
            "p95": times_sorted[int(len(times) * 0.95)],
            "p99": times_sorted[int(len(times) * 0.99)],
            "min": min(times),
            "max": max(times)
        }

    def run_all(self):
        """모든 벤치마크 실행"""
        print("=" * 60)
        print("PoC #2 저장소 벤치마크 시작")
        print("=" * 60)

        results = {}

        # 1. 파일시스템
        print("\n[1/3] 파일시스템 벤치마크...")
        results["filesystem"] = self.benchmark_filesystem()

        # 2. MinIO
        print("\n[2/3] MinIO 벤치마크...")
        results["minio"] = self.benchmark_minio()

        # 3. RocksDB
        print("\n[3/3] RocksDB 벤치마크...")
        results["rocksdb"] = self.benchmark_rocksdb()

        # 결과 저장
        self.save_results(results)

        return results

    def save_results(self, results):
        """결과를 JSON 파일로 저장"""
        import json
        with open("/results/benchmark_results.json", "w") as f:
            json.dump(results, f, indent=2)

        print("\n결과가 /results/benchmark_results.json에 저장되었습니다.")

if __name__ == "__main__":
    benchmark = StorageBenchmark()
    benchmark.run_all()
```

#### Dockerfile

**benchmark/Dockerfile:**

```dockerfile
FROM python:3.11-slim

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libsnappy-dev \
    zlib1g-dev \
    libbz2-dev \
    liblz4-dev \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /benchmark

CMD ["python", "benchmark.py"]
```

**benchmark/requirements.txt:**

```
minio==7.2.0
psycopg2-binary==2.9.9
redis==5.0.1
python-rocksdb==0.7.0
```

### 벤치마크 결과 템플릿

| 저장소 조합             | 쓰기 (MB/s) | 읽기 (ms, 95p) | 메타 조회 (ms) | 디스크 효율 | S3 호환 | 점수 |
| ----------------------- | ----------- | -------------- | -------------- | ----------- | ------- | ---- |
| FS + PostgreSQL         | ?           | ?              | ?              | ?           | ❌      | ?    |
| FS + PostgreSQL + Redis | ?           | ?              | ?              | ?           | ❌      | ?    |
| RocksDB                 | ?           | ?              | ?              | ?           | ❌      | ?    |
| MinIO + PostgreSQL      | ?           | ?              | ?              | ?           | ✅      | ?    |
| MinIO + Redis           | ?           | ?              | ?              | ?           | ✅      | ?    |

### PoC 검증 결과 및 의사결정 기준

**검증 목표:**

- 각 저장소 옵션별 성능 측정 (쓰기/읽기 속도, 메모리 사용량)
- 치과 이미지 특성에 맞는 최적화 효과 검증
- 운영 복잡도 및 유지보수성 평가
- **MinIO 추가 검증**: S3 호환성, 클라우드 동기화 성능, 멀티테넌시

**PoC 성공 기준:**

- 명확한 성능 차이 측정 (20% 이상 차이 시 의미 있음)
- 저장소 조합별 장단점 정량화
- 기술적 의사결정 근거 문서화
- 프로덕션 개발 시 저장소 선택 가이드라인 제시
- **MinIO 평가 기준**:
  - S3 API 100% 호환 (boto3, aws-sdk 동작 확인)
  - 클라우드 동기화 속도 > 10MB/s
  - HTTP 오버헤드 < 20% (vs 파일시스템)

**의사결정 매트릭스:**

| 기준             | 가중치 | 파일시스템 | RocksDB | MinIO |
| ---------------- | ------ | ---------- | ------- | ----- |
| 성능 (읽기/쓰기) | 30%    | ?          | ?       | ?     |
| 운영 단순성      | 25%    | ?          | ?       | ?     |
| 클라우드 호환성  | 20%    | ?          | ?       | ?     |
| 메모리 효율      | 15%    | ?          | ?       | ?     |
| 확장성           | 10%    | ?          | ?       | ?     |
| **총점**         | 100%   | ?          | ?       | ?     |

**의사결정:**

- PoC 결과 기반 저장소 조합 선정
- 치과 이미지 특성에 최적화된 아키텍처 도출
- 순수 로컬 vs 클라우드 하이브리드 선택 기준 정립
- 향후 프로덕션 개발 시 고려사항 정리

## 5. 개발 언어 고려사항 (Rust 우선)

### 5.1 저장소 인터페이스 구현 언어

**Rust (권장):**

- **장점**: 안전한 고성능 I/O, 낮은 런타임 오버헤드, 단일 바이너리
- **적합성**: 파일 시스템 조작, 데이터베이스/Redis 연동, 동시성 처리(tokio)
- **라이브러리**:
  - PostgreSQL: sqlx 또는 tokio-postgres
  - Redis: redis-rs
  - 파일시스템: std::fs/tokio::fs
  - RocksDB: rust-rocksdb
  - **MinIO/S3**: rust-s3, aws-sdk-s3 (공식 AWS SDK)

**Python (대안):**

- **장점**: 풍부한 PostgreSQL 라이브러리, 빠른 개발
- **라이브러리**:
  - PostgreSQL: psycopg2
  - 파일시스템: pathlib, os
  - **MinIO**: minio-py (공식 Python SDK)
- **단점**: 성능 제한, 의존성 관리

### 5.2 캐시 관리 로직 구현 언어

**Rust (권장):**

- **장점**: lock-free/async 패턴, 메모리 안전성, 높은 처리량
- **적합성**: LRU/LFU, TinyLFU 입소 필터, 스풀/저널 워커

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

**MinIO:**

- **라이선스**: GNU AGPL v3 (서버) / Apache 2.0 (클라이언트 SDK)
- **상업적 사용**: ✅ 허용 (클라이언트 SDK 사용 시)
- **주의사항**: MinIO 서버 코드 수정 시 AGPL 의무 (소스 공개), 바이너리만 사용 시 문제없음
- **상용 라이선스**: 엔터프라이즈 기능 필요 시 별도 구매 가능

**Rust 언어:**

- **라이선스**: Apache-2.0 / MIT (듀얼)
- **상업적 사용**: ✅ 허용
- **수정/배포**: ✅ 허용
- **고지 의무**: ✅ 라이선스 고지 유지

### 5.4 Windows/Linux 설치 호환성 고려사항

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

**MinIO Windows 배포:**

- **바이너리**: 단일 실행 파일 (minio.exe)
- **의존성**: 없음 (Go로 컴파일된 정적 바이너리)
- **서비스 등록**: NSSM으로 Windows 서비스 등록 가능
- **설정**: 환경 변수 또는 설정 파일로 구성
- **데이터 경로**: `C:\ProgramData\MinIO\data` 권장

**Rust 애플리케이션 Windows 배포:**

- **바이너리**: 단일 실행 파일로 컴파일 가능 (MSVC toolchain)
- **의존성**: PostgreSQL 클라이언트 라이브러리 (libpq.dll) 등 필요 시 동봉
- **MinIO 연동**: rust-s3 또는 aws-sdk-s3 크레이트 사용
- **서비스 등록**: windows-service/NSSM 활용
- **설정 파일**: JSON/YAML 설정 파일 지원

**PostgreSQL Linux 배포:**

- **연결**: 기존 PostgreSQL 서버 또는 Docker 컨테이너
- **의존성**: libpq-dev 설치
- **서비스**: systemd로 클라이언트/에이전트 관리

**Redis/RocksDB Linux 배포:**

- **Redis**: apt/yum 설치, systemd 서비스
- **RocksDB**: 패키지 또는 정적 링크, glibc/반영 의존성 확인

**MinIO Linux 배포:**

- **바이너리**: 단일 실행 파일 (wget으로 다운로드)
- **설치**: `/usr/local/bin/minio` 권장
- **서비스**: systemd 서비스 등록
- **Docker**: 공식 이미지 `minio/minio` 제공
- **데이터 경로**: `/var/lib/minio/data` 권장

**Rust 애플리케이션 Linux 배포:**

- **배포**: 단일 바이너리 + systemd 서비스
- **의존성**: libpq, OpenSSL 등 배포 스크립트로 설치
- **MinIO 연동**: rust-s3 크레이트 (aws-sdk-s3도 가능)
- **컨테이너**: Docker/Podman 지원 (CacheBox 시나리오와 호환)

### 다음 단계

선정된 저장소 구조로 PoC #4 통합 프로토타입에 적용
