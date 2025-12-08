# PoC #4: 통합 프로토타입 구현 결과 보고서

## 1. 개요

### 1.1 검증 목표

PoC #1, #2, #3에서 검증된 기술을 통합하여 **Windows Native 배포 가능한 통합 프로토타입**을 단계적으로 구현하고, 선정된 기술 스택의 통합 동작을 검증하여 프로덕션 개발 가이드라인을 도출한다.

**소스코드 저장소:**

소스코드는 다음 위치에서 확인할 수 있습니다:

- **Azure DevOps**: https://ewoosoft@dev.azure.com/ewoosoft/prototypes/\_git/scp-cache-poc/poc4

**검증 방식:**

- Phase별 단계적 구현 및 검증
- 통합 기술 스택 동작 검증
- 성능 벤치마크 및 안정성 검증

### 1.2 검증 범위

**전체 Phase:**

- Phase 1: 읽기 경로 구현
- Phase 2: 캐시 최적화
- Phase 3: 쓰기 경로 구현
- Phase 4: 장애 처리 및 오프라인 모드
- Phase 5: 모니터링 및 로깅
- Phase 6: 성능 검증 및 안정성 테스트

### 1.3 성공 기준

**기능 요구사항:**

- 기본 리버스 프록시 및 캐시 HIT/MISS 동작 정상 작동
- 캐시 알고리즘 적용 (LRU 기반)
- TTL 기반 캐시 만료 처리
- 쓰기 경로 동작 (쓰기 백 스풀링)
- 오프라인 모드 동작
- 모니터링 및 로깅 기능

**성능 요구사항:**

- 캐시 HIT 지연: 95p < 50ms
- 캐시 MISS 지연: CloudFront 직접 + 20ms 이내
- 동시 100 req/s 처리 가능

---

## 2. 구현 진행 상황

### 2.1 Phase 1: 읽기 경로 구현 (완료)

**구현 완료 일자:** 2024년 (진행 중)

**구현 내용:**

1. **HTTP 서버 기본 구조 생성**

   - Axum 프레임워크 기반 HTTP 서버 구현
   - Rust 프로젝트 초기화 및 구조 설정
   - 기본 라우팅 및 헬스 체크 엔드포인트 구현

2. **MongoDB 연결 및 인덱스 생성**

   - MongoDB 클라이언트 연결 구현
   - `cache_metadata` 컬렉션 인덱스 생성
   - 캐시 키 기반 인덱스 및 만료 시간 기반 인덱스 설정

3. **캐시 키 생성 로직**

   - 형식: `clinicId:URI:queryNorm:policyVersion`
   - 쿼리 파라미터 정규화 구현 (정렬 및 소문자 변환)
   - SHA256 기반 해시 생성

4. **캐시 상태 확인 로직**

   - HIT/MISS/STALE 상태 판별
   - MongoDB 메타데이터 조회
   - TTL 기반 만료 시간 확인

5. **업스트림 서버 프록시 요청**

   - reqwest 클라이언트 구현
   - CloudFront 및 API 서버 프록시
   - 헤더 전달 (Authorization, X-Clinic-ID 등)

6. **캐시된 파일에서 실제 응답 제공**

   - MongoDB에서 파일 경로 조회
   - 파일 시스템에서 실제 파일 읽기
   - 스트림 기반 응답 생성

7. **Content-Type 헤더 설정**

   - mime_guess 크레이트 사용
   - 파일 확장자 기반 MIME 타입 추론
   - Content-Length 헤더 설정

8. **쿼리 파라미터 정규화 완성**

   - 파라미터 정렬 및 소문자 변환
   - 동일 쿼리를 일관된 키로 변환

9. **TTL 기반 만료 처리**

   - 경로별 차등 TTL 적용
     - Thumbnail: 30일
     - Preview: 7일
     - 기타: 10분
   - 만료된 캐시 자동 재요청

10. **에러 처리 개선**

    - anyhow::Context 사용한 상세 에러 메시지
    - 에러 타입별 HTTP 상태 코드 설정
    - 캐시 서빙 실패 시 자동 업스트림 재요청

11. **설정 파일 로드 기능**

    - TOML 파일 기반 설정 로드 (`cache-config.toml`)
    - 설정 파일이 없으면 기본값 사용
    - 설정 파일 예시 제공 (`cache-config.toml.example`)

12. **기본 통합 테스트**
    - 자동화된 테스트 스크립트 (`tests/integration_test.sh`)
    - 헬스체크, 캐시 HIT/MISS, 클리닉 ID 분리, 쿼리 파라미터 정규화 테스트
    - 테스트 가이드 문서 작성 (`tests/README.md`)

**구현 파일:**

- `src/main.rs`: 메인 진입점, 라우팅
- `src/config.rs`: 설정 관리 (TOML 파일 로드 지원)
- `src/storage.rs`: 저장소 관리 (MongoDB, 파일시스템)
- `src/cache.rs`: 캐시 로직 (키 생성, 상태 확인, 메타데이터 관리)
- `src/proxy.rs`: 프록시 핸들러 (캐시 확인, 업스트림 요청, 응답 생성)
- `cache-config.toml.example`: 설정 파일 예시
- `tests/integration_test.sh`: 통합 테스트 스크립트
- `tests/README.md`: 테스트 가이드

**주요 의존성:**

- `axum`: HTTP 서버 프레임워크
- `mongodb`: MongoDB 드라이버
- `reqwest`: HTTP 클라이언트
- `mime_guess`: MIME 타입 추론
- `tokio-util`: 비동기 스트림 유틸리티
- `toml`: TOML 설정 파일 파싱
- `anyhow`: 에러 처리

**검증 결과:**

- 컴파일 성공
- 기본 구조 동작 확인
- 캐시 HIT/MISS 로직 정상 작동
- 설정 파일 로드 기능 정상 작동
- 통합 테스트 스크립트 작성 완료

**테스트 시나리오:**

1. **헬스체크 테스트**: `/health` 엔드포인트 정상 응답 확인

   - HTTP 200 상태 코드
   - "OK" 응답 본문

2. **캐시 MISS 테스트**: 첫 요청 시 `X-Cache-Status: MISS` 확인

   - 업스트림 서버로 요청 전달
   - 응답 캐시에 저장 시도

3. **캐시 HIT 테스트**: 두 번째 요청 시 `X-Cache-Status: HIT` 확인 (업스트림 성공 시)

   - 로컬 캐시에서 파일 읽기
   - Content-Type, Content-Length 헤더 설정

4. **클리닉 ID 분리 테스트**: 다른 클리닉 ID로 별도 캐시 키 생성 확인

   - `X-Clinic-Id` 헤더로 클리닉 구분
   - 캐시 키에 클리닉 ID 포함

5. **쿼리 파라미터 정규화 테스트**: 동일한 쿼리가 정규화되어 동일 캐시 키 생성 확인
   - 파라미터 정렬 및 소문자 변환
   - 순서가 달라도 동일 캐시 키 생성

**설정 파일 기능:**

- TOML 형식 설정 파일 지원 (`cache-config.toml`)
- 설정 파일이 없으면 기본값 사용
- 런타임에 설정 파일 로드 및 파싱
- 설정 파일 예시 제공 (`cache-config.toml.example`)

**통합 테스트 도구:**

- 자동화된 테스트 스크립트 (`tests/integration_test.sh`)
- 환경 변수 기반 설정 지원
- 색상 코드로 테스트 결과 시각화
- 테스트 가이드 문서 (`tests/README.md`)

**다음 단계:**

- Phase 2: 캐시 최적화 (LRU 알고리즘 구현, 캐시 용량 관리)

---

### 2.2 Phase 2: 캐시 최적화 (예정)

**예정 내용:**

- LRU 알고리즘 구현
- 메모리 내 캐시 인덱스 관리
- 캐시 용량 제한 및 축출 정책

---

### 2.3 Phase 3: 쓰기 경로 구현 (예정)

**예정 내용:**

- 쓰기 백 스풀링 구현
- 로컬 저널링
- 일관성 보장

---

### 2.4 Phase 4: 장애 처리 및 오프라인 모드 (예정)

**예정 내용:**

- 네트워크 단절 감지
- 오프라인 모드 동작
- Fallback 메커니즘

---

### 2.5 Phase 5: 모니터링 및 로깅 (예정)

**예정 내용:**

- Prometheus 메트릭 노출
- Windows Event Log 통합
- 로깅 구조화

---

### 2.6 Phase 6: 성능 검증 및 안정성 테스트 (예정)

**예정 내용:**

- 부하 테스트
- 성능 벤치마크
- 장애 시나리오 테스트

---

## 3. 기술 스택 결정

### 3.1 구현 언어: Rust

**선택 이유:**

- Windows Native 배포 편의성 (단일 바이너리)
- 높은 성능 및 메모리 안전성
- 크로스 컴파일 지원 (macOS 개발 → Windows 배포)

### 3.2 HTTP 서버: Axum (Rust 내장)

**선택 이유:**

- 배포 편의성 (단일 바이너리, 런타임 의존성 없음)
- Windows Native 환경 최적화
- Tokio 기반 비동기 런타임으로 성능 우수
- 기술 스택 통합 (단일 언어/프레임워크)

### 3.3 저장소: MongoDB Interface

**선택 이유:**

- PoC #2 검증 결과 반영
- 유연한 스키마 및 인덱싱
- TTL 인덱스 지원

---

## 4. 아키텍처

### 4.1 전체 구조

```
Client Request
    ↓
Axum HTTP Server
    ↓
ProxyHandler
    ↓
CacheManager ←→ Storage (MongoDB + FileSystem)
    ↓
Cache HIT → Serve from Cache
Cache MISS → Fetch from Upstream → Save to Cache
```

### 4.2 주요 컴포넌트

1. **ProxyHandler**: HTTP 요청 처리, 캐시 확인, 업스트림 프록시
2. **CacheManager**: 캐시 로직 (키 생성, 상태 확인, TTL 관리)
3. **Storage**: MongoDB 메타데이터 저장, 파일시스템 미디어 저장

---

## 5. 검증 결과

### 5.1 Phase 1 검증 결과

**기능 검증:**

- HTTP 서버 정상 시작 ✅
- MongoDB 연결 성공 ✅
- 캐시 키 생성 정상 작동 ✅
- 캐시 HIT/MISS 판별 정상 ✅
- 파일 시스템 읽기/쓰기 정상 ✅
- Content-Type 헤더 설정 정상 ✅
- 설정 파일 로드 기능 정상 작동 ✅
- 통합 테스트 스크립트 정상 실행 ✅

**통합 테스트 결과:**

- 헬스체크 엔드포인트 정상 응답 ✅
- 캐시 MISS/HIT 동작 확인 ✅
- 클리닉 ID별 캐시 분리 확인 ✅
- 쿼리 파라미터 정규화 확인 ✅

**성능 검증:**

- (Phase 6에서 진행 예정)

**안정성 검증:**

- (Phase 6에서 진행 예정)

---

## 6. 결론 및 다음 단계

### 6.1 현재 상태

Phase 1 (읽기 경로 구현)이 완료되었으며, 기본적인 캐시 서버 기능이 동작함을 확인했습니다.

### 6.2 다음 단계

1. Phase 2 진행: 캐시 최적화 구현
2. Phase 3 진행: 쓰기 경로 구현
3. Phase 4-6 진행: 장애 처리, 모니터링, 성능 검증

### 6.3 의사결정

- Rust + Axum 조합이 Windows Native 배포에 적합함을 확인
- MongoDB Interface를 통한 메타데이터 관리가 효과적임을 확인
- 단계적 구현 방식이 효과적임을 확인

---

## 부록

### A. 소스코드 위치

소스코드는 다음 저장소에서 확인할 수 있습니다:

- **Azure DevOps**: https://ewoosoft@dev.azure.com/ewoosoft/prototypes/\_git/scp-cache-poc/poc4
- **경로**: `poc4/prototype/` 디렉터리

### B. 빌드 및 실행 방법

```bash
# 개발 환경 (macOS)
cargo build --release

# Windows 크로스 컴파일
rustup target add x86_64-pc-windows-msvc
cargo build --release --target x86_64-pc-windows-msvc
```

### C. 설정 파일 구조

#### 설정 파일 예시 (`cache-config.toml`)

```toml
[server]
host = "0.0.0.0"
port = 8080

[cache]
media_root = "/var/cache/scp/media"
max_size_gb = 200
thumbnail_ttl_days = 30
preview_ttl_days = 7
metadata_ttl_minutes = 10

[mongodb]
uri = "mongodb://localhost:27017"
database = "scp_cache"

[upstream]
cloudfront_url = "https://d1234567890.cloudfront.net"
api_url = "https://api.scp-cloud.com"
```

#### 설정 파일 사용법

1. 예시 파일 복사: `cp cache-config.toml.example cache-config.toml`
2. 원하는 값으로 수정
3. 서버 재시작 시 설정 자동 로드
4. 설정 파일이 없으면 기본값 사용

### C. 성능 벤치마크 결과

(Phase 6 완료 후 추가)
