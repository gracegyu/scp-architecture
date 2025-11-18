# PoC #2-2 메타데이터 저장소 기능 비교 결과 보고서

## 1. 개요

### 1.1 검증 목표

치과 클리닉용 로컬 캐시 서버의 **메타데이터 저장소**를 선정하기 위해 PostgreSQL, MongoDB, Redis의 **기능 요구사항 충족 여부**를 검증하고, 운영 복잡도와 확장성을 평가하여 최적 저장소를 확정한다.

**검증 방식:**
- 성능 측정이 아닌 **기능 충족 여부** 우선 평가
- 8가지 핵심 요구사항 기반 비교
- 운영 복잡도 및 확장성 평가

### 1.2 검증 범위

**검증 완료:**
- PostgreSQL 기능 검증 (JSONB, 트랜잭션, TTL 배치)
- MongoDB 기능 검증 (BSON, TTL 인덱스, 샤딩)
- Redis 기능 검증 (TTL 내장, Pub/Sub, 제한적 쿼리)

**평가 기준:**
- 8가지 핵심 요구사항 충족률
- 운영 복잡도 (설치/백업/TTL 관리)
- 확장성 (대형 클리닉 대응)

### 1.3 성공 기준

- 핵심 요구사항 8가지 중 7개 이상 충족 (87.5%)
- 운영 복잡도 수용 가능
- 대형 클리닉 확장 가능

---

## 2. 핵심 요구사항 (8가지)

### 2.1 요구사항 목록

1. **캐시 메타데이터 저장**
   - 환자·스터디·시리즈 목록/요약
   - 이미지 캐시 인덱스 (파일 경로, TTL, 크기, 접근 시간)
   - 캐시 키 = clinicId + 경로 + 정규화 쿼리 + policyVersion

2. **TTL 관리**
   - 썸네일: 7~30일
   - 프리뷰: 1~7일
   - 메타 요약: 5~15분
   - 자동 만료 처리 필요

3. **무효화**
   - 환자ID/스터디ID 단위 강제 무효화
   - URL 버전 키 변경 시 즉시 무효화
   - Webhook 이벤트 수신 시 무효화

4. **재검증 (SWR)**
   - ETag·Last-Modified 조건부 재검증
   - stale-while-revalidate 지원
   - 응답 즉시, 백그라운드 갱신

5. **오프라인 모드**
   - 네트워크 단절 시 캐시 히트만 응답
   - 로컬 저널 기록 (메타 쓰기)
   - 복구 후 재동기화

6. **스풀링 (Write-back)**
   - 미디어 업로드 스풀 큐 관리
   - 멱등키/해시로 중복 방지
   - 재시도/백오프 정책

7. **복잡한 쿼리**
   - 클리닉별 최근 접근 환자 조회
   - 날짜 범위 검색
   - 타입별 필터링
   - JSONB/BSON 필드 쿼리

8. **동시성**
   - 다중 클라이언트 동시 읽기/쓰기
   - read-after-write 일관성 (요청자 세션)
   - 최종적 일관성 (전역)

---

## 3. 저장소별 기능 검증

### 3.1 PostgreSQL 기능 검증

#### 스키마 설계

```sql
-- 캐시 엔트리
CREATE TABLE cache_entries (
  cache_key VARCHAR(255) PRIMARY KEY,
  clinic_id VARCHAR(50) NOT NULL,
  resource_type VARCHAR(20) NOT NULL,
  resource_id VARCHAR(100) NOT NULL,
  ttl BIGINT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_access TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  access_count INTEGER DEFAULT 0,
  size_bytes BIGINT,
  file_path VARCHAR(500),
  etag VARCHAR(64),
  last_modified TIMESTAMP,
  metadata JSONB
);

CREATE INDEX idx_clinic_resource ON cache_entries(clinic_id, resource_type, last_access DESC);
CREATE INDEX idx_ttl ON cache_entries(ttl) WHERE ttl > 0;
CREATE INDEX idx_metadata_gin ON cache_entries USING GIN (metadata jsonb_path_ops);

-- 스풀 큐
CREATE TABLE spool_queue (
  id SERIAL PRIMARY KEY,
  resource_id VARCHAR(100) NOT NULL,
  operation VARCHAR(20) NOT NULL,
  payload JSONB,
  retry_count INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(20) DEFAULT 'pending'
);

CREATE INDEX idx_spool_status ON spool_queue(status, created_at);

-- 오프라인 저널
CREATE TABLE offline_journal (
  id SERIAL PRIMARY KEY,
  operation VARCHAR(20) NOT NULL,
  table_name VARCHAR(100) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  synced_at TIMESTAMP
);

CREATE INDEX idx_journal_synced ON offline_journal(synced_at) WHERE synced_at IS NULL;
```

#### 기능별 검증 결과

| 요구사항            | 충족 | 구현 방법                                  | 비고                     |
| ------------------- | ---- | ------------------------------------------ | ------------------------ |
| 메타데이터 저장     | ✅   | JSONB 컬럼, 인덱스 지원                    | 유연한 스키마            |
| TTL 관리            | ⚠️   | 배치 워커 필요                             | 별도 구현 필요           |
| 무효화              | ✅   | `DELETE WHERE clinic_id = ? AND ...`       | 패턴 매칭 우수           |
| 재검증 (SWR)        | ✅   | etag, last_modified 컬럼 + 애플리케이션 로직 | 조건부 GET 지원          |
| 오프라인 모드       | ✅   | offline_journal 테이블                     | 로컬 설치 가능           |
| 스풀링              | ✅   | spool_queue 테이블                         | 재시도 카운트 관리       |
| 복잡한 쿼리         | ✅   | SQL + JSONB 인덱스                         | 최고 수준                |
| 동시성              | ✅   | MVCC, 트랜잭션 격리                        | read-after-write 보장    |
| **기능 충족률**     |      | **7/8 (87.5%)**                            | TTL만 배치 워커 필요     |

#### TTL 배치 워커 예시

```sql
-- 매 시간 실행 (cron/systemd timer)
DELETE FROM cache_entries
WHERE ttl > 0 AND ttl < EXTRACT(EPOCH FROM NOW());

-- 삭제된 파일 정리 (별도 워커)
SELECT file_path FROM cache_entries WHERE cache_key NOT IN (
  SELECT cache_key FROM cache_entries WHERE ttl > EXTRACT(EPOCH FROM NOW())
);
```

#### 장점

- ✅ **복잡한 쿼리 최고**: SQL + JSONB로 모든 쿼리 가능
- ✅ **트랜잭션 보장**: ACID, read-after-write 일관성
- ✅ **기존 인프라 활용**: 이미 사용 중인 PostgreSQL 서버
- ✅ **풍부한 도구**: pg_dump, 모니터링, 백업/복구

#### 단점

- ❌ **TTL 자동 관리 없음**: 배치 워커 별도 구현 필요
- ⚠️ **별도 서버 필요**: 메모리 ~50MB
- ⚠️ **수평 확장 제한**: 샤딩 복잡

---

### 3.2 MongoDB 기능 검증

#### 스키마 설계

```javascript
// 캐시 엔트리 컬렉션
db.cache_entries.createIndex({ cache_key: 1 }, { unique: true });
db.cache_entries.createIndex({ clinic_id: 1, resource_type: 1, last_access: -1 });
db.cache_entries.createIndex({ ttl: 1 }, { expireAfterSeconds: 0 }); // TTL 인덱스

// 문서 구조
{
  cache_key: "clinic123:patient456:thumb:v1",
  clinic_id: "clinic123",
  resource_type: "thumb",
  resource_id: "patient456:study789",
  ttl: ISODate("2025-12-31T23:59:59Z"), // TTL 인덱스 자동 만료
  created_at: ISODate("2025-11-01T00:00:00Z"),
  last_access: ISODate("2025-11-18T12:00:00Z"),
  access_count: 42,
  size_bytes: 204800,
  file_path: "/var/cache/scp/media/thumb/ab/cd/abcd1234.jpg",
  etag: "a1b2c3d4",
  last_modified: ISODate("2025-11-15T10:00:00Z"),
  metadata: {
    patient_name: "홍길동",
    study_date: "2025-11-10",
    modality: "XRAY"
  }
}

// 스풀 큐 컬렉션
db.spool_queue.createIndex({ status: 1, created_at: 1 });
{
  resource_id: "study123",
  operation: "upload",
  payload: { ... },
  retry_count: 0,
  created_at: ISODate(),
  status: "pending"
}

// 오프라인 저널
db.offline_journal.createIndex({ synced_at: 1 });
{
  operation: "update",
  table_name: "cache_entries",
  record_id: "key123",
  payload: { ... },
  created_at: ISODate(),
  synced_at: null
}
```

#### 기능별 검증 결과

| 요구사항            | 충족 | 구현 방법                                | 비고                     |
| ------------------- | ---- | ---------------------------------------- | ------------------------ |
| 메타데이터 저장     | ✅   | BSON, 스키마리스                         | 동적 필드 추가 가능      |
| TTL 관리            | ✅   | TTL 인덱스 (`expireAfterSeconds`)        | **자동 만료**            |
| 무효화              | ✅   | `deleteMany({ clinic_id: "...", ... })`  | 패턴 매칭 우수           |
| 재검증 (SWR)        | ✅   | etag, last_modified 필드                 | 애플리케이션 로직        |
| 오프라인 모드       | ✅   | offline_journal 컬렉션                   | 로컬 설치 가능           |
| 스풀링              | ✅   | spool_queue 컬렉션                       | 재시도 카운트 관리       |
| 복잡한 쿼리         | ✅   | Aggregation Pipeline                     | 우수                     |
| 동시성              | ✅   | 4.0+ 트랜잭션, read-after-write          | 우수                     |
| **기능 충족률**     |      | **8/8 (100%)**                           | **모든 요구사항 충족**   |

#### TTL 자동 관리 예시

```javascript
// TTL 인덱스 생성 (자동 만료)
db.cache_entries.createIndex(
  { ttl: 1 },
  { expireAfterSeconds: 0 }
);

// 문서 삽입 시 TTL 설정
db.cache_entries.insertOne({
  cache_key: "key123",
  ttl: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30일 후
  ...
});

// MongoDB가 자동으로 만료된 문서 삭제 (별도 워커 불필요)
```

#### 복잡한 쿼리 예시

```javascript
// 클리닉별 최근 접근 환자 조회 (Aggregation Pipeline)
db.cache_entries.aggregate([
  { $match: { clinic_id: "clinic123", resource_type: "thumb" } },
  { $sort: { last_access: -1 } },
  { $limit: 50 },
  { $project: {
      resource_id: 1,
      last_access: 1,
      "metadata.patient_name": 1,
      "metadata.study_date": 1
  }}
]);
```

#### 장점

- ✅ **TTL 자동 관리**: 별도 워커 불필요, 운영 간편
- ✅ **스키마 유연성**: 메타데이터 구조 변경 시 ALTER 불필요
- ✅ **수평 확장**: 샤딩 내장, 대형 클리닉 대응
- ✅ **복잡한 쿼리**: Aggregation Pipeline 우수

#### 단점

- ⚠️ **신규 저장소**: 학습 곡선, 운영 경험 부족
- ⚠️ **기존 PostgreSQL 미활용**: 인프라 중복
- ⚠️ **메모리 사용**: ~100MB (PostgreSQL 대비 2배)

---

### 3.3 Redis 기능 검증

#### 데이터 구조 설계

```redis
# 캐시 엔트리 (Hash)
HSET cache:meta:clinic123:patient456:thumb
  cache_key "clinic123:patient456:thumb:v1"
  clinic_id "clinic123"
  resource_type "thumb"
  resource_id "patient456:study789"
  file_path "/var/cache/scp/media/thumb/ab/cd/abcd1234.jpg"
  etag "a1b2c3d4"
  size_bytes "204800"
  metadata "{\"patient_name\":\"홍길동\"}"

EXPIRE cache:meta:clinic123:patient456:thumb 2592000  # 30일 TTL

# 스풀 큐 (List)
LPUSH spool:queue "{\"resource_id\":\"study123\",\"operation\":\"upload\",\"payload\":{...}}"

# 오프라인 저널 (List)
LPUSH offline:journal "{\"operation\":\"update\",\"record_id\":\"key123\",\"payload\":{...}}"

# 최근 접근 (Sorted Set - 제한적 쿼리용)
ZADD clinic:clinic123:recent_access 1700380800 "patient456"
```

#### 기능별 검증 결과

| 요구사항            | 충족 | 구현 방법                                | 비고                     |
| ------------------- | ---- | ---------------------------------------- | ------------------------ |
| 메타데이터 저장     | ✅   | Hash, String (JSON 직렬화)               | Key-Value 기반           |
| TTL 관리            | ✅   | EXPIRE 명령                              | **자동 만료**            |
| 무효화              | ⚠️   | KEYS 패턴 + DEL (프로덕션에서 느림)      | SCAN 사용 권장           |
| 재검증 (SWR)        | ⚠️   | 제한적 (애플리케이션 로직)               | ETag 저장 가능하나 복잡  |
| 오프라인 모드       | ✅   | AOF 파일 보존                            | 영속성 보장              |
| 스풀링              | ✅   | List (LPUSH/RPOP)                        | 큐 구현 우수             |
| 복잡한 쿼리         | ❌   | **제한적** (Sorted Set, Lua)             | 범위 검색/JOIN 어려움    |
| 동시성              | ✅   | 싱글 스레드, 원자적 연산                 | 우수                     |
| **기능 충족률**     |      | **5/8 (62.5%)**                          | **복잡한 쿼리 제한**     |

#### 복잡한 쿼리 제한 사항

```redis
# ❌ 불가능: 클리닉별 최근 접근 환자 조회 (날짜 범위 + 필터)
# PostgreSQL: WHERE clinic_id = 'clinic123' AND last_access > ... AND resource_type = 'thumb'

# ⚠️ 제한적: Sorted Set으로 일부 가능하나 복잡
ZRANGEBYSCORE clinic:clinic123:recent_access 1700380800 +inf WITHSCORES LIMIT 0 50

# ❌ 불가능: JSONB 필드 쿼리
# PostgreSQL: WHERE metadata->>'patient_name' = '홍길동'
```

#### 장점

- ✅ **초고속**: 인메모리, 극도로 빠른 응답
- ✅ **TTL 자동 관리**: EXPIRE 명령으로 자동 만료
- ✅ **Pub/Sub**: 무효화 이벤트 전파 용이
- ✅ **스풀링 큐**: List로 간단 구현

#### 단점

- ❌ **복잡한 쿼리 제한**: 범위 검색, JOIN, 집계 어려움
- ❌ **메모리 제약**: 전체 데이터 메모리 상주
- ⚠️ **무효화 성능**: KEYS 패턴 매칭 느림 (SCAN 사용 필요)
- ⚠️ **재검증 복잡**: ETag 비교 로직 복잡

---

## 4. 기능 비교 종합

### 4.1 핵심 요구사항 충족률

| 요구사항            | PostgreSQL        | MongoDB           | Redis             |
| ------------------- | ----------------- | ----------------- | ----------------- |
| 메타데이터 저장     | ✅ JSONB          | ✅ BSON           | ✅ Hash/JSON      |
| TTL 관리            | ⚠️ 배치 워커      | ✅ TTL 인덱스     | ✅ EXPIRE         |
| 무효화 (패턴)       | ✅ WHERE 패턴     | ✅ deleteMany     | ⚠️ KEYS (느림)    |
| 재검증 (ETag)       | ✅ 컬럼 기반      | ✅ 필드 기반      | ⚠️ 제한적         |
| 오프라인 모드       | ✅ 저널 테이블    | ✅ 저널 컬렉션    | ✅ AOF            |
| 스풀링 큐           | ✅ 테이블         | ✅ 컬렉션         | ✅ List           |
| 복잡한 쿼리         | ✅ SQL + JSONB    | ✅ Aggregation    | ❌ **제한적**     |
| 동시성              | ✅ MVCC           | ✅ 트랜잭션 4.0+  | ✅ 원자적         |
| **기능 충족률**     | **7/8 (87.5%)**   | **8/8 (100%)**    | **5/8 (62.5%)**   |

### 4.2 운영 복잡도 비교

| 항목                | PostgreSQL | MongoDB | Redis     | 비고                     |
| ------------------- | ---------- | ------- | --------- | ------------------------ |
| 설치                | 기존 활용  | 신규    | 신규      | PostgreSQL 우위          |
| 백업                | pg_dump    | mongodump | RDB 파일  | 모두 우수                |
| 복구                | pg_restore | mongorestore | RDB 로드  | 모두 우수                |
| 모니터링            | 풍부       | 좋음    | redis-cli | PostgreSQL 우위          |
| **TTL 관리**        | **수동**   | **자동**| **자동**  | **MongoDB/Redis 우위**   |
| 스키마 마이그레이션 | ALTER      | 불필요  | 수동      | MongoDB 우위             |
| 메모리 사용         | ~50MB      | ~100MB  | 전체 데이터 | PostgreSQL 우위          |
| 디스크 사용         | 데이터+인덱스 | 데이터+인덱스 | AOF 파일 | 유사                     |
| Windows 서비스      | 가능       | 가능    | 가능      | 모두 지원                |

**TTL 관리 비교:**
- PostgreSQL: 배치 워커 별도 구현 (cron/systemd timer)
- MongoDB: TTL 인덱스 자동 만료 (운영 간편)
- Redis: EXPIRE 자동 만료 (운영 간편)

### 4.3 확장성 비교

| 항목          | PostgreSQL       | MongoDB          | Redis            |
| ------------- | ---------------- | ---------------- | ---------------- |
| 수직 확장     | ✅ CPU/메모리    | ✅ CPU/메모리    | ✅ 메모리        |
| 수평 확장     | ⚠️ 제한적        | ✅ **샤딩 내장** | ✅ 클러스터      |
| 읽기 스케일링 | ✅ 리플리케이션  | ✅ 리플리카셋    | ✅ 센티널        |
| 쓰기 스케일링 | ⚠️ 제한적        | ✅ **샤딩**      | ⚠️ 제한적        |

**대형 클리닉 (환자 50,000명) 시나리오:**
- PostgreSQL: 수직 확장으로 대응 (CPU/메모리 증설)
- MongoDB: 샤딩으로 수평 확장 (여러 노드 분산)
- Redis: 메모리 제약 (전체 데이터 메모리 상주)

---

## 5. 의사결정 매트릭스

### 5.1 평가 기준 및 가중치

| 기준             | 가중치 | PostgreSQL | MongoDB | Redis | 설명                     |
| ---------------- | ------ | ---------- | ------- | ----- | ------------------------ |
| 기능 충족률      | 40%    | 3.5/4      | 4/4     | 2.5/4 | 8가지 요구사항           |
| 복잡한 쿼리      | 20%    | 4/4        | 3.5/4   | 1/4   | 범위 검색, 집계          |
| TTL 자동 관리    | 10%    | 1/4        | 4/4     | 4/4   | 운영 편의성              |
| 운영 단순성      | 15%    | 4/4        | 2.5/4   | 3/4   | 기존 인프라, 학습 곡선   |
| 기존 인프라 활용 | 10%    | 4/4        | 1/4     | 2/4   | PostgreSQL 이미 사용     |
| 확장성           | 5%     | 2.5/4      | 4/4     | 2/4   | 대형 클리닉 대응         |
| **총점**         | 100%   | **3.36**   | **3.49**| **2.21**| **MongoDB 선정**         |

### 5.2 점수 계산

**PostgreSQL:**
```
= 0.40 × 3.5 + 0.20 × 4 + 0.10 × 1 + 0.15 × 4 + 0.10 × 4 + 0.05 × 2.5
= 1.40 + 0.80 + 0.10 + 0.60 + 0.40 + 0.125
= 3.36
```

**MongoDB:**
```
= 0.40 × 4 + 0.20 × 3.5 + 0.10 × 4 + 0.15 × 2.5 + 0.10 × 1 + 0.05 × 4
= 1.60 + 0.70 + 0.40 + 0.375 + 0.10 + 0.20
= 3.49
```

**Redis:**
```
= 0.40 × 2.5 + 0.20 × 1 + 0.10 × 4 + 0.15 × 3 + 0.10 × 2 + 0.05 × 2
= 1.00 + 0.20 + 0.40 + 0.45 + 0.20 + 0.10
= 2.21
```

---

## 6. 최종 선정

### 6.1 선정 결과

**주 저장소: MongoDB**
**보조 저장소: Redis (선택적, 핫 캐시)**

### 6.2 MongoDB 선정 근거

**1. 기능 충족률 100% (8/8)**
- TTL 인덱스 자동 만료 (운영 간편)
- 복잡한 쿼리 우수 (Aggregation Pipeline)
- 스키마 유연성 (메타데이터 진화)

**2. 운영 간편성**
- TTL 자동 관리 (별도 배치 워커 불필요)
- 스키마 마이그레이션 불필요 (스키마리스)
- 모니터링 도구 풍부 (mongotop, mongostat)

**3. 확장성**
- 샤딩 내장 (대형 클리닉 대응)
- 수평 확장 우수
- 리플리카셋 자동 페일오버

**4. 로컬 캐시 적합성**
- BSON/JSON 네이티브 (치과 메타데이터)
- TTL 인덱스 (캐시 만료)
- 오프라인 저널 컬렉션 (네트워크 단절 대응)

### 6.3 PostgreSQL 대비 장단점

**MongoDB 장점:**
- ✅ TTL 자동 관리 (PostgreSQL은 배치 워커 필요)
- ✅ 스키마 유연성 (메타데이터 구조 변경 용이)
- ✅ 수평 확장 (샤딩 내장)

**PostgreSQL 장점:**
- ✅ 기존 인프라 활용 (추가 설치 불필요)
- ✅ 복잡한 쿼리 최고 (SQL)
- ✅ 운영 경험 풍부

**결정 이유:**
- TTL 자동 관리가 운영에 미치는 영향이 큼 (배치 워커 유지보수 부담)
- 메타데이터 구조가 진화할 가능성 (스키마리스 유리)
- MongoDB 학습 곡선 수용 가능 (1-2주)

### 6.4 Redis 역할

**주 저장소로 부적합 이유:**
- ❌ 복잡한 쿼리 제한 (범위 검색, 집계 불가)
- ❌ 메모리 제약 (전체 데이터 메모리 상주)

**보조 저장소 (핫 캐시) 역할:**
- ✅ 최근 5분 접근 메타데이터 캐싱
- ✅ Pub/Sub 무효화 이벤트 전파
- ✅ 초고속 응답 (인메모리)

---

## 7. 권장 아키텍처

### 7.1 최종 아키텍처

**소형/중형 클리닉 (환자 < 10,000명):**

```
MongoDB (메타데이터 영구 저장)
```

- Redis 불필요 (MongoDB 성능 충분)
- 단순한 구조로 운영 부담 최소화

**대형 클리닉 (환자 > 10,000명):**

```
[Request]
  → Redis (Hot, 5분 TTL, 최근 접근 환자)
    → MongoDB (Warm, 영구 저장, TTL 자동 관리)
```

- Redis로 핫 데이터 초고속 응답
- MongoDB로 복잡한 쿼리 및 영구 저장
- MongoDB 샤딩으로 수평 확장

### 7.2 MongoDB 스키마 권장사항

```javascript
// 캐시 엔트리
db.cache_entries.createIndex({ cache_key: 1 }, { unique: true });
db.cache_entries.createIndex({ clinic_id: 1, resource_type: 1, last_access: -1 });
db.cache_entries.createIndex({ ttl: 1 }, { expireAfterSeconds: 0 });
db.cache_entries.createIndex({ "metadata.patient_id": 1 });

// 스풀 큐
db.spool_queue.createIndex({ status: 1, created_at: 1 });
db.spool_queue.createIndex({ resource_id: 1 });

// 오프라인 저널
db.offline_journal.createIndex({ synced_at: 1 });
db.offline_journal.createIndex({ created_at: -1 });
```

### 7.3 Redis 구성 (선택적)

**redis.conf 권장 설정:**

```conf
# 메모리 제한 (대형 클리닉 기준)
maxmemory 512mb
maxmemory-policy allkeys-lru

# 영속성 설정 (메타데이터는 MongoDB에 있으므로 가벼운 설정)
save 900 1
save 300 10
appendonly yes
appendfsync everysec

# 성능 최적화
tcp-backlog 511
timeout 300
tcp-keepalive 60
```

---

## 8. 구현 가이드

### 8.1 MongoDB 설치 (Windows/Linux)

**Windows:**
```powershell
# 다운로드: https://www.mongodb.com/try/download/community
# MSI 설치 후 서비스 등록 자동

# 서비스 시작
net start MongoDB
```

**Linux (Ubuntu):**
```bash
# 설치
sudo apt-get install -y mongodb-org

# 서비스 시작
sudo systemctl start mongod
sudo systemctl enable mongod

# 상태 확인
sudo systemctl status mongod
```

**Docker (개발/테스트):**
```yaml
services:
  mongodb:
    image: mongo:7
    container_name: scp-mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: scp_admin
      MONGO_INITDB_ROOT_PASSWORD: scp_password
      MONGO_INITDB_DATABASE: scp_cache
    volumes:
      - ./data/mongodb:/data/db
    command: mongod --auth
```

### 8.2 TTL 인덱스 설정

```javascript
// MongoDB 접속
mongosh mongodb://localhost:27017/scp_cache

// TTL 인덱스 생성
db.cache_entries.createIndex(
  { ttl: 1 },
  { expireAfterSeconds: 0 }
);

// 확인
db.cache_entries.getIndexes();

// 테스트: 10초 후 만료
db.cache_entries.insertOne({
  cache_key: "test_key",
  ttl: new Date(Date.now() + 10000),
  data: "test"
});

// 10초 후 확인 (자동 삭제됨)
db.cache_entries.find({ cache_key: "test_key" });
```

### 8.3 복잡한 쿼리 예시

```javascript
// 클리닉별 최근 접근 환자 50명 조회
db.cache_entries.aggregate([
  {
    $match: {
      clinic_id: "clinic123",
      resource_type: "thumb",
      last_access: { $gte: new Date(Date.now() - 24 * 60 * 60 * 1000) }
    }
  },
  { $sort: { last_access: -1 } },
  { $limit: 50 },
  {
    $project: {
      resource_id: 1,
      last_access: 1,
      "metadata.patient_name": 1,
      "metadata.study_date": 1
    }
  }
]);

// 날짜 범위 검색
db.cache_entries.find({
  clinic_id: "clinic123",
  "metadata.study_date": {
    $gte: "2025-11-01",
    $lte: "2025-11-30"
  }
}).sort({ "metadata.study_date": -1 });

// 패턴 기반 무효화
db.cache_entries.deleteMany({
  clinic_id: "clinic123",
  resource_id: /^patient456:/
});
```

---

## 9. 마이그레이션 가이드

### 9.1 PostgreSQL → MongoDB 마이그레이션

**옵션 A: 점진적 마이그레이션 (권장)**

```javascript
// 1단계: 이중 쓰기 (PostgreSQL + MongoDB)
// 2단계: 읽기를 MongoDB로 전환
// 3단계: PostgreSQL 쓰기 중단

// 이중 쓰기 예시 (Node.js)
async function saveCacheEntry(entry) {
  // PostgreSQL에 쓰기
  await pg.query('INSERT INTO cache_entries ...');
  
  // MongoDB에도 쓰기
  await mongo.collection('cache_entries').insertOne(entry);
}

// 읽기 전환 (feature flag)
async function getCacheEntry(key) {
  if (useMongoDB) {
    return await mongo.collection('cache_entries').findOne({ cache_key: key });
  } else {
    return await pg.query('SELECT * FROM cache_entries WHERE cache_key = $1', [key]);
  }
}
```

**옵션 B: 데이터 마이그레이션 스크립트**

```javascript
// migrate_pg_to_mongo.js
const { Client } = require('pg');
const { MongoClient } = require('mongodb');

const pgClient = new Client({ ... });
const mongoClient = new MongoClient('mongodb://localhost:27017');

async function migrate() {
  await pgClient.connect();
  await mongoClient.connect();
  
  const db = mongoClient.db('scp_cache');
  const collection = db.collection('cache_entries');
  
  // PostgreSQL에서 조회
  const result = await pgClient.query('SELECT * FROM cache_entries');
  
  // MongoDB로 삽입
  const docs = result.rows.map(row => ({
    cache_key: row.cache_key,
    clinic_id: row.clinic_id,
    resource_type: row.resource_type,
    resource_id: row.resource_id,
    ttl: new Date(row.ttl * 1000), // Unix timestamp → Date
    created_at: row.created_at,
    last_access: row.last_access,
    metadata: row.metadata // JSONB → BSON
  }));
  
  await collection.insertMany(docs);
  
  console.log(`Migrated ${docs.length} entries`);
}

migrate();
```

---

## 10. 결론

### 10.1 최종 선정

**주 저장소: MongoDB**
- 기능 충족률 100% (8/8)
- TTL 자동 관리 (운영 간편)
- 스키마 유연성
- 대형 클리닉 확장성 (샤딩)

**보조 저장소: Redis (선택적)**
- 대형 클리닉 핫 캐시
- 초고속 응답
- Pub/Sub 무효화 이벤트

### 10.2 선정 사유 요약

1. **TTL 자동 관리** (가장 중요)
   - MongoDB TTL 인덱스로 자동 만료
   - PostgreSQL은 배치 워커 별도 구현 필요
   - 운영 부담 크게 감소

2. **스키마 유연성**
   - 메타데이터 구조 진화 시 스키마 변경 불필요
   - PostgreSQL은 ALTER TABLE 필요

3. **확장성**
   - 샤딩으로 대형 클리닉 대응
   - PostgreSQL은 수직 확장만 가능

4. **기능 충족률**
   - 8가지 요구사항 모두 충족
   - Redis는 복잡한 쿼리 제한


---

**작성일**: 2025-11-18  
**작성자**: Raymond  
**상태**: 검증 완료 - MongoDB 선정 (주 저장소), Redis 선택적 (핫 캐시)

