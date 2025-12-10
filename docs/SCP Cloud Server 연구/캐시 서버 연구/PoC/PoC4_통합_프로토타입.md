# PoC #4: 로컬 캐시 서버 통합 프로토타입

## 개요

PoC #1, #2, #3에서 검증된 기술을 통합하여 **Windows Native 배포 가능한 통합 프로토타입**을 단계적으로 구현한다. **목적**: 선정된 기술 스택의 통합 동작을 검증하고, 프로덕션 개발 가이드라인을 도출한다.

**기간:** 3주

**목표:**

- 통합 기술 검증 및 프로덕션 개발 가이드라인 도출
- Windows Native 환경에서 실행 가능한 프로토타입 구현
- 성능 벤치마크 및 안정성 검증

## 전제 조건

PoC #1, #2, #3 완료 및 의사결정:

- Reverse Proxy 선정 완료
- 저장소 아키텍처 결정 완료 (MongoDB Interface)
- 캐시 알고리즘 및 파라미터 확정 (LRU, PoC3 결과 반영)

## 개발 언어 및 배포 환경

**구현 언어: Rust (필수)**

**개발 환경:**

- **OS**: macOS (개발 환경)
- **빌드 도구**: cargo (Rust), 크로스 컴파일 도구
- **Windows 크로스 컴파일**: macOS에서 Windows 바이너리 빌드 지원
  - 타겟: `x86_64-pc-windows-msvc`
  - 도구 체인: `rustup target add x86_64-pc-windows-msvc`
  - 빌드 명령: `cargo build --release --target x86_64-pc-windows-msvc`

**배포 환경:**

- **OS**: Windows 10/11 이상
- **배포 형태**: 단일 바이너리 (.exe)
- **런타임 의존성**: 없음 (정적 링킹)
- **Windows 서비스**: windows-service 크레이트 활용
- **NSIS 설치**: .exe 파일만 포함하여 간단한 설치 구조

**배포 요구사항:**

- Windows 10/11 이상
- MongoDB (별도 설치 또는 포함)
- 네트워크 연결 (CloudFront/S3 접근)

**제외 사항:**

- Docker 컨테이너 (Native 환경만 지원)
- Python 런타임 (Rust 단일 바이너리만 사용)
- 외부 Reverse Proxy (Nginx/Envoy) 대신 Rust 내장 HTTP 서버 사용 (선택 배경은 "Reverse Proxy 아키텍처 결정 배경" 섹션 참조)

---

## Phase 진행 현황

**전체 기간:** 3주

- [x] **Phase 1: 읽기 경로 구현** (4-5일, Week 1)

  - 목표: 기본 리버스 프록시와 캐시 HIT/MISS 동작 구현
  - [x] HTTP 서버 기본 구조 생성 (Axum 프로젝트 초기화)
  - [x] MongoDB 연결 및 인덱스 생성
  - [x] 캐시 키 생성 로직 (`clinicId:URI:queryNorm:policyVersion`)
  - [x] 캐시 상태 확인 로직 (HIT/MISS/STALE)
  - [x] 업스트림 서버 프록시 요청 (reqwest 클라이언트)
  - [x] 캐시된 파일에서 실제 응답 제공 (파일 읽기 구현)
  - [x] Content-Type 헤더 설정 (mime_guess 사용)
  - [x] 쿼리 파라미터 정규화 완성 (정렬 및 소문자 변환)
  - [x] TTL 기반 만료 처리 (경로별 차등 TTL 적용)
  - [x] 에러 처리 개선 (상세 에러 메시지 및 적절한 HTTP 상태 코드)
  - [x] 설정 파일 로드 기능 (TOML 파일에서 설정 읽기)
  - [x] 기본 통합 테스트 (자동화 테스트 스크립트 및 검증)

- [x] **Phase 2: 캐시 최적화** (3일, Week 2)

  - 목표: LRU 알고리즘 구현, 무효화 메커니즘, 조건부 재검증, 프리페칭으로 히트율 80% 달성
  - [x] LRU 알고리즘 구현 (lru 크레이트 또는 자체 구현)
  - [x] 용량 기반 캐시 제거 (캐시 크기 초과 시)
  - [x] 무효화 API 엔드포인트 구현 (`POST /api/cache/invalidate`)
  - [x] 패턴 매칭 무효화 (환자/스터디 단위)
  - [x] ETag 지원 및 저장
  - [x] Last-Modified 지원
  - [x] 조건부 GET 처리 (`If-None-Match`, `If-Modified-Since`)
  - [x] 304 Not Modified 응답 처리
  - [x] Stale-while-revalidate 구현
  - [x] 프리페칭 전략 구현 (환자 진입 이벤트)

- [ ] **Phase 3: 쓰기 경로 구현** (2일, Week 2)

  - 목표: Write-back 스풀링, 로컬 저널링, 일관성 보장
  - [ ] 미디어 업로드 API 구현 (`POST /api/upload`)
  - [ ] 로컬 스풀 저장 (`C:\ProgramData\SCP\Cache\spool\`)
  - [ ] 백그라운드 S3 멀티파트 업로드 워커
  - [ ] 업로드 진행률 API (`GET /api/upload/{resourceId}/status`)
  - [ ] 스풀 큐 MongoDB 컬렉션 구성
  - [ ] 재시도 로직 (최대 3회, 지수 백오프)
  - [ ] 멱등키 기반 중복 방지
  - [ ] 메타데이터 Write-through 구현 (`POST /api/metadata`)
  - [ ] 로컬 저널링 구현 (MongoDB 컬렉션)
  - [ ] 저널 재생 백그라운드 워커
  - [ ] Read-after-write 보장 (세션 전용 캐시 핀)

- [ ] **Phase 4: 장애 대응** (2일, Week 3)

  - 목표: 폴백 메커니즘, 오프라인 모드, 재동기화
  - [ ] 헬스체크 구현 (업스트림 서버 상태 모니터링)
  - [ ] 장애 감지 로직 (3회 연속 실패 시)
  - [ ] 클라이언트 폴백 메커니즘 (URI 경로 유지)
  - [ ] 네트워크 단절 감지
  - [ ] 오프라인 모드 구현 (로컬 캐시만 서빙)
  - [ ] 오프라인 상태 UI 표시 지원
  - [ ] 저널 재생 절차 구현
  - [ ] 스풀 큐 재처리 절차
  - [ ] 차등 스캔 구현 (`updatedAt` 비교)
  - [ ] 재동기화 후 캐시 무효화

- [ ] **Phase 5: 운영 준비** (2일, Week 3)

  - 목표: 인증/권한 처리, 보안 강화, 모니터링/로깅
  - [ ] JWT 토큰 패스스루 (Authorization 헤더)
  - [ ] 권한 변경 시 캐시 무효화 (Webhook 수신)
  - [ ] 디스크 암호화 (BitLocker 또는 파일 단위 AES-256)
  - [ ] TLS 1.3 지원 (rustls 크레이트)
  - [ ] Windows 방화벽 규칙 설정
  - [ ] 감사 로그 구현 (모든 접근 기록)
  - [ ] 헬스체크 API (`GET /health`)
  - [ ] 메트릭 API (`GET /metrics` - Prometheus 포맷)
  - [ ] 수동 무효화 API (`POST /cache/invalidate`)
  - [ ] 캐시 통계 API (`GET /cache/stats`)
  - [ ] 구조화 JSON 액세스 로그
  - [ ] Prometheus exporter 구현
  - [ ] Windows Service 등록 (windows-service 크레이트)

- [ ] **Phase 6: 성능 검증 및 최종 보고서** (1일, Week 3)
  - 목표: 부하 테스트, 성능 벤치마크, 최종 보고서 작성
  - [ ] 정상 운영 시나리오 부하 테스트 (100명, 5,000 req/s, 1시간)
  - [ ] 피크 부하 테스트 (300명, 10,000 req/s, 10분)
  - [ ] 대용량 파일 테스트 (100MB 파일, 동시 10건)
  - [ ] 성능 벤치마크 결과 분석 (히트율, TTFB, 오리진 감소율)
  - [ ] 리소스 사용량 측정 (CPU, 메모리, 디스크)
  - [ ] 장애 시나리오 테스트 (네트워크 단절, 서버 재시작, 디스크 풀)
  - [ ] 보안 테스트 (인증 우회, 권한 없는 접근)
  - [ ] 최종 보고서 작성 (Executive Summary, 아키텍처, 성능 결과, 운영 가이드)

---

## Phase 1: 읽기 경로 구현

**기간:** 1주 (Week 1)

### 목표

기본 리버스 프록시와 캐시 HIT/MISS 동작을 구현하여 CloudFront → 로컬 캐시 → 클라이언트 읽기 경로를 완성한다.

### 구현 범위

#### 1.1 HTTP 서버 및 Reverse Proxy 구현 (Rust)

##### 아키텍처 결정 배경

**PoC #1 검증 결과 요약:**

PoC #1에서 Nginx(OpenResty), Envoy, Pingora를 비교 검증한 결과:

**Nginx(OpenResty) 성능:**

- 캐시 HIT 처리량: 461 req/s
- 지연시간 (99p): 12.5ms
- 에러율: 0%
- 총점: 105점 (최고점)

**주요 발견:**

- Docker 환경에서 우수한 성능 검증
- Windows Native 환경에서는 설치/설정 복잡도 존재
- Nginx 바이너리 + 설정 파일 + Lua 스크립트 관리 필요

**PoC #4에서 Rust 내장 HTTP 서버 선택 이유:**

PoC #1의 검증 결과를 바탕으로, **PoC #4에서는 Rust 내장 HTTP 서버(Axum)를 선택**했습니다.

**1. 배포 편의성 (주요 이유)**

1. **단일 바이너리 배포**: `.exe` 파일 하나만으로 모든 기능 포함
2. **런타임 의존성 없음**: Nginx, Lua 등 추가 소프트웨어 설치 불필요
3. **Windows Native 환경 최적화**: Windows Service 통합 용이
4. **설치 프로세스 단순화**: NSIS 설치 패키지 제작 시 복잡도 감소
5. **버전 관리 용이**: 바이너리 하나만 관리하여 업데이트/롤백 간편

**2. 성능 고려사항**

- Axum은 Tokio 기반 비동기 런타임으로 성능 우수
- Rust의 메모리 안전성과 제로 코스트 추상화로 낮은 오버헤드
- PoC #1의 목표 성능(100 req/s) 대비 충분한 여유 (Axum은 수천 req/s 처리 가능)
- 실제 워크로드에서 성능 병목은 네트워크 I/O와 디스크 I/O가 주 요인

**3. 기술 스택 통합**

- Rust 기반으로 캐시 로직, HTTP 서버, MongoDB 클라이언트를 하나의 코드베이스로 관리
- 타입 안전성과 컴파일 타임 검증으로 운영 안정성 향상
- 단일 언어/프레임워크로 개발/디버깅/유지보수 효율성 증대

**4. 트레이드오프 분석**

- PoC #1의 최고 성능(461 req/s) 대비 일부 성능 차이 가능
- 다만 실제 클리닉 환경에서는 네트워크 대역폭과 디스크 I/O가 주요 제약이므로 HTTP 서버 성능 차이는 영향 적음
- 배포 편의성과 운영 복잡도 감소가 성능 미세 차이보다 더 큰 가치 제공

**결론:** Windows Native 환경에서의 배포 편의성과 운영 복잡도 감소를 위해 Rust 내장 HTTP 서버(Axum)를 선택했으며, PoC #1에서 검증한 성능 요구사항(100 req/s, 95p < 50ms)은 충분히 달성 가능합니다.

##### 구현 사항

**Axum 프레임워크 사용:**

- Tokio 기반 비동기 HTTP 서버
- PoC #1에서 검증한 성능 요구사항(100 req/s, 95p < 50ms) 충분히 달성 가능
- 단일 바이너리로 모든 기능 포함

**구현 항목:**

- HTTP/HTTPS 프록시 기능
- 업스트림 서버 연결 (CloudFront, API 서버)
- 커넥션 풀링, Keep-Alive, 타임아웃 설정
- 단일 바이너리로 빌드 (cargo build --release)

**성능 목표:**

- 캐시 HIT 지연: 95p < 50ms (PoC #1 검증 기준)
- 캐시 MISS 지연: CloudFront 직접 + 20ms 이내
- 동시 100 req/s 처리 가능

#### 1.2 캐시 저장소 구성

- 미디어 저장소 초기화 (파일시스템 구조)
  - Windows 프로덕션 경로: `C:\ProgramData\SCP\Cache\media\`
  - Linux 프로덕션 경로: `/var/cache/scp/media`
  - macOS 개발 경로 (기본값): `~/Library/Caches/scp-cache/media`
  - 디렉터리 구조: `{clinicId}/{studyId}/{resourceType}/`
  - **경로는 설정 파일(`cache-config.toml`)의 `[cache].media_root`로 변경 가능**
- 메타데이터 저장소 초기화 (MongoDB 연결)
  - MongoDB 드라이버: mongodb 크레이트
  - 연결 설정: `mongodb://localhost:27017` (기본) 또는 설정 파일에서 지정
  - 데이터베이스: `scp_cache`
  - 컬렉션: `cache_metadata`, `cache_keys`, `cache_stats`
  - 인덱스 생성: 캐시 키, TTL, 클리닉 ID별 인덱스
- 디렉터리 권한 및 용량 설정
  - 캐시 최대 용량 설정 (설정 파일)
  - 디스크 사용량 모니터링

#### 1.3 기본 캐시 로직

- 캐시 키 생성: `clinicId:URI:queryNorm:policyVersion`
- 캐시 HIT: 로컬에서 즉시 응답
- 캐시 MISS: CloudFront에서 가져와 저장 후 응답
- TTL 설정 (경로별 차등)
  - 썸네일: 30일
  - 프리뷰: 7일
  - 메타데이터: 10분

#### 1.4 응답 헤더

- `X-Cache-Status: HIT|MISS|STALE`
- `X-Cache-Key: {키 정보}`
- `Cache-Control`, `Expires` 전달

### 검증 기준

**기능 테스트:**

- [ ] 썸네일 첫 조회 MISS, 두 번째 조회 HIT
- [ ] 프리뷰 첫 조회 MISS, 두 번째 조회 HIT
- [ ] TTL 만료 후 재검증 동작
- [ ] 다른 clinicId는 별도 캐시

**성능 테스트:**

- [ ] 캐시 HIT 지연: 95p < 50ms
- [ ] 캐시 MISS 지연: CloudFront 직접 + 20ms 이내
- [ ] 동시 100 req/s 처리

**안정성:**

- [ ] 24시간 연속 운영 무장애
- [ ] 디스크 풀 시 LRU 제거 동작

---

## Phase 2: 캐시 최적화

**기간:** 3일 (Week 2)

### 목표

LRU 알고리즘 구현, 무효화 메커니즘, 조건부 재검증, 프리페칭으로 히트율을 목표치(80%)까지 향상한다.

### 구현 범위

#### 2.1 LRU 알고리즘 구현 (PoC3 결과 반영)

- PoC3 검증 결과: LRU 알고리즘 선정
- LRU 캐시 구현 (Rust)
  - `lru` 크레이트 또는 자체 구현
  - 용량 기반 제거 (캐시 크기 초과 시)
- TTL 기반 만료 정책
- 캐시 통계 수집 (히트율, 미스율)

#### 2.2 무효화 메커니즘

- REST API 엔드포인트: `POST /api/cache/invalidate`
- Webhook 수신 처리
- 패턴 매칭 무효화
  - 환자 단위: `clinic:{id}:patient:{patientId}:*`
  - 스터디 단위: `clinic:{id}:study:{studyId}:*`
- 무효화 로그 저장 (MongoDB 컬렉션: `invalidation_log`)

#### 2.3 조건부 재검증

- ETag 지원: CloudFront 응답 ETag 저장
- Last-Modified 지원
- 조건부 GET: `If-None-Match`, `If-Modified-Since`
- 304 Not Modified 처리

#### 2.4 Stale-while-revalidate

- 만료 후에도 즉시 응답 (stale)
- 백그라운드 재검증 비동기 수행
- 재검증 완료 후 캐시 갱신

#### 2.5 프리페칭

- 환자 진입 이벤트 수신
- 썸네일 전량 프리페치 (비동기)
- 대표 프리뷰 3개 프리페치

### 검증 기준

**히트율 목표:**

- [ ] 요청 기준 히트율: 80% 이상
- [ ] 바이트 기준 히트율: 70% 이상

**무효화:**

- [ ] 환자 삭제 시 관련 캐시 즉시 무효화
- [ ] 권한 변경 시 5초 이내 반영

**재검증:**

- [ ] ETag 일치 시 304 반환 (전송 절약)
- [ ] SWR로 체감 지연 50% 감소

**프리페칭:**

- [ ] 환자 진입 후 3초 내 썸네일 프리페치 완료
- [ ] 히트율 +10% 향상

---

## Phase 3: 쓰기 경로 구현

**기간:** 2일 (Week 2)

### 목표

Write-back 스풀링, 로컬 저널링, 일관성 보장으로 업로드 및 메타데이터 쓰기를 구현한다.

### 구현 범위

#### 3.1 미디어 업로드 (Write-back)

- 업로드 요청 수신: `POST /api/upload`
- 로컬 스풀 저장 (Windows 경로: `C:\ProgramData\SCP\Cache\spool\`)
- 즉시 응답: `202 Accepted` + `resourceId`
- 백그라운드 워커: S3 멀티파트 업로드
- 진행률 API: `GET /api/upload/{resourceId}/status`

#### 3.2 스풀 큐 관리

- MongoDB 컬렉션: `spool_queue`
- 상태: `pending` → `processing` → `done` / `failed`
- 재시도 로직: 최대 3회, 지수 백오프 (1s, 2s, 4s)
- 멱등키: 해시 기반 중복 방지
- MongoDB 인덱스: 상태별, 타임스탬프별 인덱스

#### 3.3 메타데이터 쓰기 (Write-through)

- `POST /api/metadata` → 원서버 전송
- 성공 시: MongoDB 캐시 즉시 반영 + `200 OK`
- 실패 시: 로컬 저널 기록 + `500 Error`

#### 3.4 로컬 저널링

- MongoDB 컬렉션: `journal`
- 실패한 메타 쓰기 기록 (순서, 타임스탬프)
- 백그라운드 재생 (매 1분, Tokio 스케줄러)
- 성공 시 저널 항목 제거

#### 3.5 Read-after-write 보장

- 요청자 세션 추적 (세션 ID)
- 세션 전용 캐시 핀 (1-5분)
- 다른 세션은 최종적 일관성

### 검증 기준

**업로드:**

- [ ] 100MB 파일 업로드 성공률 99% 이상
- [ ] 스풀 큐 처리 지연: 평균 30초
- [ ] 멱등키로 중복 업로드 0건

**일관성:**

- [ ] Read-after-write: 요청자 세션 100% 보장
- [ ] 타 세션: 5분 내 최종 일관성

**재시도:**

- [ ] 네트워크 단절 시 재시도 동작
- [ ] 재시도 성공률 95% 이상

---

## Phase 4: 장애 대응

**기간:** 2일 (Week 3)

### 목표

캐시 서버 장애, 네트워크 단절 시 폴백 및 오프라인 모드를 구현하고 복구 후 재동기화를 수행한다.

### 구현 범위

#### 4.1 자동 폴백 메커니즘

- 헬스체크: 캐시 서버 상태 모니터링 (매 5초)
- 장애 감지: 3회 연속 실패 시 장애 판정
- 클라이언트 폴백: 호스트만 교체 (캐시 → 클라우드)
  - URI 경로 동일 유지
  - `/v1/clinic/{id}/...` → CloudFront 직접 연결
- 복구 감지: 헬스체크 성공 시 캐시 재사용

#### 4.2 오프라인 모드

- 네트워크 단절 감지 (외부 연결 실패)
- 로컬 캐시만으로 서빙
- 제약 사항 UI 표시
  - "오프라인 모드: 일부 기능 제한"
  - 캐시 미보유 항목 조회 불가 안내

#### 4.3 쓰기 처리 (오프라인)

- 미디어 업로드: 스풀 큐 보류
- 메타데이터 쓰기: 로컬 저널 기록
- 온라인 복구 시 재동기화

#### 4.4 재동기화 절차

1. **저널 재생**
   - 로컬 저널 순서대로 재적용
   - 버전/타임스탬프 검증
   - 충돌 시 서버 우선 (마지막 쓰기 승리)
2. **스풀 큐 처리**
   - 보류된 업로드 재시도
   - 멱등키로 중복 방지
3. **차등 스캔**
   - `updatedAt` 비교
   - 변경분만 동기화 (양방향)
4. **캐시 무효화**
   - 환자/스터디 단위 강제 무효화
   - 프리페치 재시작

### 검증 기준

**폴백:**

- [ ] 캐시 장애 감지: 15초 이내
- [ ] 클라이언트 자동 전환: 5초 이내
- [ ] URI 경로 유지로 무중단 조회

**오프라인 모드:**

- [ ] 네트워크 단절 시 캐시 데이터 100% 서빙
- [ ] 미보유 항목 명확한 에러 메시지
- [ ] 쓰기 작업 저널/스풀 큐 보류

**재동기화:**

- [ ] 저널 재생 성공률: 99% 이상
- [ ] 스풀 큐 처리 완료: 5분 이내
- [ ] 충돌 해결: 서버 데이터 우선 적용

**시나리오 테스트:**

- [ ] 네트워크 단절 → 1시간 오프라인 → 복구 → 재동기화 성공
- [ ] 캐시 서버 재시작 → 10초 내 폴백 → 복구 후 재연결

---

## Phase 5: 운영 준비

**기간:** 2일 (Week 3)

### 목표

인증/권한 처리, 보안 강화, 모니터링/로깅으로 운영 환경 배포를 준비한다.

### 구현 범위

#### 5.1 인증/권한 처리

- JWT 토큰 패스스루
  - `Authorization` 헤더 → 원서버 전달
  - 캐시 키에서 제외 (히트율 유지)
- Signed URL/Cookie 처리
  - CloudFront 서명 검증 (옵션)
  - 경로 기반 HMAC 서명 (옵션)
- 권한 변경 즉시 무효화
  - Webhook: 권한 이벤트 수신
  - 관련 캐시 강제 제거

#### 5.2 보안

- **디스크 암호화 (Windows)**
  - BitLocker 볼륨 암호화 (권장)
  - 또는 파일 단위 암호화 (AES-256, ring 크레이트)
- **전송 암호화**
  - TLS 1.3 (클라이언트 ↔ 캐시, rustls 크레이트)
  - TLS 1.2+ (캐시 ↔ 클라우드)
- **접근 제어**
  - Windows 방화벽 규칙 (netsh 또는 WinAPI)
  - 최소 권한 원칙 (Windows Service 계정 권한)
- **감사 로그**
  - 모든 접근 기록 (접근 시간, IP, 리소스)
  - 민감 정보 마스킹 (환자 ID 해싱)
  - 로그 보존 기간: 90일
  - Windows Event Log 연동 (옵션)

#### 5.3 헬스체크 및 관리 API

- `GET /health`: 상태 확인
  - `status`: `healthy` / `degraded` / `unhealthy`
  - 디스크 용량, 메모리 사용량
- `GET /metrics`: Prometheus 포맷
  - `cache_hit_rate`, `cache_miss_rate`
  - `origin_traffic_bytes`
  - `spool_queue_size`
- `POST /cache/invalidate`: 수동 무효화
- `GET /cache/stats`: 캐시 통계
  - Top 10 항목 (빈도 기준)
  - 히트율 추이 (시간별)

#### 5.4 로깅

- **액세스 로그** (구조화 JSON)
  ```json
  {
    "timestamp": "2025-10-21T10:00:00Z",
    "client_ip": "192.168.1.100",
    "method": "GET",
    "uri": "/thumb/...",
    "status": 200,
    "cache_status": "HIT",
    "response_time_ms": 12
  }
  ```
- **에러 로그**
  - 스택 트레이스, 에러 코드
  - 알람 연동 (Critical 에러)
- **로그 전송**
  - 중앙 로그 서버 (Fluentd/Logstash)
  - 또는 CloudWatch Logs

#### 5.5 메트릭 수집

- Prometheus exporter
- 주요 메트릭:
  - `cache_requests_total{status="hit|miss"}`
  - `cache_bytes_total{status="hit|miss"}`
  - `cache_evictions_total`
  - `spool_queue_length`
  - `journal_replay_errors_total`
  - `origin_requests_total`
  - `response_time_seconds{quantile="0.5|0.95|0.99"}`

### 검증 기준

**인증:**

- [ ] JWT 토큰 유효성 검증 (원서버 위임)
- [ ] 권한 변경 5초 내 캐시 무효화

**보안:**

- [ ] 디스크 암호화 활성화
- [ ] TLS 1.3 연결
- [ ] 감사 로그 100% 기록

**관측성:**

- [ ] Prometheus 메트릭 노출
- [ ] 액세스 로그 JSON 포맷
- [ ] 알람 동작 (디스크 풀 90% 시)

**관리 API:**

- [ ] 헬스체크 5초 내 응답
- [ ] 수동 무효화 정상 동작

---

## Phase 6: 성능 검증 및 최종 보고서

**기간:** 1일 (Week 3)

### 목표

부하 테스트, 성능 벤치마크로 목표 지표 달성을 검증하고 최종 보고서를 작성한다.

### 검증 범위

#### 6.1 부하 테스트

**시나리오 1: 정상 운영**

- 동시 사용자: 100명
- 요청: 5,000 req/s (HIT 80% + MISS 20%)
- 지속 시간: 1시간
- 측정:
  - 처리량 (req/s)
  - 지연시간 (50/95/99p)
  - 에러율 (< 0.1%)

**시나리오 2: 피크 부하**

- 동시 사용자: 300명
- 요청: 10,000 req/s
- 지속 시간: 10분
- 측정: 시스템 안정성, 큐 지연

**시나리오 3: 대용량 파일**

- 100MB 파일 업로드/다운로드
- 동시 10건
- 측정: 처리 시간, 메모리 사용

#### 6.2 성능 벤치마크

**목표 지표:**

- [ ] 캐시 히트율: 요청 80%, 바이트 70%
- [ ] TTFB: 95p < 100ms, 99p < 200ms
- [ ] 오리진 트래픽 감소: 60% 이상
- [ ] 스풀 큐 지연: 평균 30초
- [ ] Read-after-write 보장: 100%

**리소스 사용:**

- [ ] CPU: 평균 < 50%, 피크 < 80%
- [ ] 메모리: < 8GB
- [ ] 디스크: 200GB에 환자 100명 이상

#### 6.3 장애 시나리오 테스트

**테스트 케이스:**

- [ ] 네트워크 단절 → 오프라인 모드 → 복구 → 재동기화
- [ ] 캐시 서버 재시작 → 폴백 → 복구
- [ ] 디스크 풀 → LRU 제거 → 정상 동작
- [ ] 원서버 장애 → 캐시만 서빙
- [ ] 무효화 폭주 (1000건/s) → 처리 지연 < 5초

#### 6.4 보안 테스트

**테스트 케이스:**

- [ ] 인증 우회 시도 → 차단
- [ ] 권한 없는 리소스 접근 → 403
- [ ] SQL Injection 시도 → 차단
- [ ] 디스크 암호화 확인
- [ ] 감사 로그 무결성

#### 6.5 최종 보고서 작성

**보고서 구성:**

1. **Executive Summary**
   - 프로젝트 목표 및 성과
   - 주요 의사결정 (Reverse Proxy, 저장소, 알고리즘)
2. **아키텍처 개요**
   - 전체 구조도
   - 컴포넌트 설명
3. **성능 결과**
   - 히트율, TTFB, 오리진 감소율
   - 부하 테스트 결과
4. **기능 검증**
   - Phase별 체크리스트 완료 현황
   - 장애 시나리오 결과
5. **운영 가이드**
   - 배포 절차
   - 설정 파라미터
   - 모니터링 지표
   - 장애 대응 매뉴얼
6. **향후 계획**
   - 프로덕션 배포 일정
   - 추가 개선 항목
   - 확장 계획

### PoC 검증 성공 기준

**통합 검증 완료:**

- [ ] Phase 1: 선정된 기술 스택 통합 동작 검증 ✅
- [ ] Phase 2: 캐시 알고리즘 통합 성능 검증 ✅
- [ ] Phase 3: 쓰기 경로 통합 동작 검증 ✅
- [ ] Phase 4: 장애 대응 통합 검증 ✅
- [ ] Phase 5: 운영 준비 통합 검증 ✅
- [ ] Phase 6: 전체 시스템 성능 검증 ✅

**PoC 성공 기준:**

- [ ] 선정된 기술 스택의 통합 동작 확인
- [ ] 기술적 의사결정 근거 문서화
- [ ] 프로덕션 개발 가이드라인 제시
- [ ] 기술적 리스크 식별 및 완화 방안 도출

---

## Phase 구조 개요

**단계별 진행 방식:**

- Phase 1 ~ Phase 6 순차 진행
- 각 Phase는 독립적으로 검증 가능
- Phase 완료 시 체크리스트 확인 후 다음 Phase 진행
- 각 Phase별 완료 기준 명시

**Phase 진행 흐름:**

```
Phase 1: 읽기 경로 구현 (기본 캐시 동작)
    ↓
Phase 2: 캐시 최적화 (히트율 향상)
    ↓
Phase 3: 쓰기 경로 구현 (업로드, 일관성)
    ↓
Phase 4: 장애 대응 (폴백, 오프라인 모드)
    ↓
Phase 5: 운영 준비 (보안, 모니터링, Windows Service)
    ↓
Phase 6: 성능 검증 및 최종 보고서
```

## 리소스 요약

**인력:**

- 개발자 1명 (Raymond) - 풀타임 개발 및 아키텍처 설계

**인프라:**

- 개발 환경: macOS 개발 머신 (Windows 크로스 컴파일)
- 테스트 환경: Windows Server 또는 Windows 10/11
- 스토리지: 500GB+ SSD (캐시 저장소용)
- 네트워크: 1Gbps (CloudFront/S3 접근)
- MongoDB: 로컬 설치 또는 원격 서버

**도구:**

- 부하 테스트: k6, wrk, 또는 Rust 기반 테스트 도구
- 모니터링: Prometheus exporter (Rust)
- 로그: 구조화 JSON 로그 (파일 출력 또는 Windows Event Log)
- 빌드: cargo (Rust)

### 7.4 라이선스 고려사항

**Rust 및 주요 크레이트:**

- **Rust**: Apache-2.0 / MIT (듀얼) ✅
- **Axum/Actix-web**: MIT License ✅
- **mongodb**: Apache-2.0 ✅
- **tokio**: MIT / Apache-2.0 ✅
- **windows-service**: MIT ✅
- **prometheus**: Apache-2.0 ✅

**모든 라이선스 상업적 사용 가능**: ✅ 법적 리스크 없음

**참고:**

- Windows 빌드: macOS에서 Windows 바이너리 크로스 컴파일 가능
- 빌드 명령: `cargo build --release --target x86_64-pc-windows-msvc`
- 배포 및 설치 패키지 제작은 PoC #5에서 진행

## 다음 단계

PoC #4 완료 후:

1. 프로덕션 배포 계획 수립
2. 파일럿 클리닉 선정 및 베타 테스트
3. 피드백 수집 및 개선
4. 전체 클리닉 확대 배포

---

## Engineering One Pager

### Project Name

로컬 캐시 서버 통합 프로토타입 (PoC #4)

### Date

2025-01-XX

### Submitter Info

**제출자**: Raymond  
**프로젝트**: SCP Cloud Server 연구  
**PoC 단계**: #4 (통합 프로토타입)

### Project Description

PoC #1, #2, #3에서 검증된 기술(Reverse Proxy, 저장소 아키텍처, 캐시 알고리즘)을 통합하여 **Windows Native 환경에서 배포 가능한 통합 프로토타입**을 구현합니다. Rust 기반 단일 바이너리로 개발하며, NSIS 기반 설치 패키지로 배포합니다.

**주요 목표:**

- 캐시 서버 통합 구현 (읽기/쓰기 경로)
- Windows Service로 실행 가능한 형태
- MongoDB 기반 메타데이터 저장소 연동
- LRU 캐시 알고리즘 구현 (PoC3 결과 반영)
- 성능 벤치마크 및 안정성 검증

### Business and Marketing Justification

**비즈니스 가치:**

1. **클라우드 운영 비용 절감**: 오리진 트래픽 60% 감소로 데이터 전송 비용 절감
2. **사용자 경험 개선**: 로컬 캐시로 조회 속도 향상 (TTFB 95p < 100ms)
3. **안정성 향상**: 오프라인 모드 지원으로 네트워크 단절 시에도 부분 서비스 가능

**배포 전략:**

- Windows Native 환경에서 실행 가능한 프로토타입 완성
- 단일 바이너리 (.exe) 형태로 빌드
- 배포 및 설치 패키지 제작은 PoC #5에서 진행

### Risk Assessment

**기술적 리스크:**

1. **MongoDB 의존성**: MongoDB 설치/설정 복잡도 → 설치 스크립트 자동화 필요
2. **Windows Service 안정성**: 장기 운영 시 메모리 누수/크래시 가능성 → 철저한 테스트 필요
3. **성능 목표 미달**: 목표 히트율(80%) 달성 실패 가능성 → PoC3 결과 반영, 단계적 최적화

**완화 방안:**

- Phase별 검증 및 단계적 구현
- 부하 테스트 및 장기 안정성 테스트 강화
- 프리페칭 등 추가 최적화 전략 준비

### Resource and Scheduling Details

**인력:**

- 개발자 1명 (Raymond) - 풀타임 개발 및 아키텍처 설계

**기간:** 3주 (Phase 1~6 순차 진행)

**기술 스택:**

- **언어**: Rust
- **HTTP 서버**: Axum/Actix-web
- **데이터베이스**: MongoDB (mongodb 크레이트)
- **비동기 런타임**: Tokio
- **Windows Service**: windows-service 크레이트
- **빌드**: cargo (Rust)

**배포 도구:**

- Windows Service API (서비스 등록용)
- 배포 및 설치 패키지 제작은 PoC #5에서 진행

### Technical Description

**Phase별 구현 범위:**

1. **Phase 1 (1주)**: 읽기 경로 구현

   - Axum 기반 Rust HTTP 서버 구현 (Nginx 대신 Rust 내장 서버)
   - LRU 캐시 알고리즘 구현
   - MongoDB 메타데이터 저장소 연동

2. **Phase 2 (3일)**: 캐시 최적화

   - 무효화 메커니즘
   - 조건부 재검증 (ETag, Last-Modified)
   - 프리페칭 전략 검증

3. **Phase 3 (2일)**: 쓰기 경로 구현

   - Write-back 스풀링
   - MongoDB 저널링
   - Read-after-write 보장

4. **Phase 4 (2일)**: 장애 대응

   - 오프라인 모드
   - 폴백 메커니즘
   - 재동기화 절차

5. **Phase 5 (2일)**: 운영 준비

   - Windows Service 등록
   - 보안 강화 (TLS, 암호화)
   - 모니터링/로깅 (Prometheus)

6. **Phase 6 (1일)**: 성능 검증 및 최종 보고서
   - 부하 테스트
   - 성능 벤치마크
   - 최종 보고서 작성

**배포 아키텍처:**

```
Windows 클라이언트
  ↓ HTTP/HTTPS
scp-cache-server.exe (Rust 단일 바이너리)
  ├── 캐시 저장소 (파일시스템)
  ├── MongoDB (메타데이터)
  └── CloudFront/S3 (원본 서버)
```

**성공 기준:**

- 캐시 히트율: 요청 80%, 바이트 70%
- TTFB: 95p < 100ms
- 오리진 트래픽 감소: 60% 이상
- Windows Service로 안정적 운영 (24시간 무장애)
- 프로덕션 개발 가이드라인 완성
