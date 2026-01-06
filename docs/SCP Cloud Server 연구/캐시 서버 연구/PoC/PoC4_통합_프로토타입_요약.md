# PoC #4: 통합 프로토타입 구현 요약

## Phase 구성

Phase 1(읽기 경로) 완료, Phase 2(캐시 최적화) 완료, Phase 3(쓰기 경로) 완료, Phase 4(장애 처리 및 오프라인 모드) 완료, Phase 5(운영 준비) 완료, Phase 6(성능 검증 및 안정성 테스트) 완료

## Phase 1 완료 내용

- Rust 기반 HTTP 서버(Axum) 구현
- MongoDB 메타데이터 저장소 연동
- 캐시 HIT/MISS/STALE 동작 및 TTL 처리

## Phase 2 완료 내용

- LRU 알고리즘 및 용량 기반 캐시 제거(200GB 초과 시 자동 축출), 캐시 통계 수집
- 무효화 API (POST /api/cache/invalidate) 및 패턴 매칭 무효화(clinic/patient/study 단위)
- ETag/Last-Modified 지원, 조건부 GET 처리(304 Not Modified), Stale-while-revalidate 구현
- 프리페칭 API (POST /api/prefetch)로 환자 진입 시 썸네일/프리뷰 비동기 프리페칭

## Phase 3 완료 내용

- 미디어 업로드 API (POST /api/upload) 및 Write-back 스풀링(로컬 임시 저장 후 백그라운드 S3 업로드)
- 스풀 큐 관리(MongoDB), 멱등키 기반 중복 방지, 재시도 로직(최대 3회)
- 메타데이터 Write-through API (POST /api/metadata) 및 로컬 저널링(실패 시 재생 워커)
- Read-after-write 보장(SessionCache로 세션별 캐시 핀 관리, 1-5분 TTL)

## Phase 4 완료 내용

- 헬스체크 모니터(업스트림 서버/네트워크/디스크/메모리 상태 확인, 5초 간격, 3회 연속 실패 시 장애 판정)
- 장애 감지 로직(연속 실패 횟수 추적, Healthy/Degraded/Unhealthy 상태 자동 전환)
- 오프라인 모드(네트워크 단절 감지, 로컬 캐시만 서빙, 오프라인 상태 UI 표시 지원)
- 재동기화 서비스(POST /api/sync로 저널 재생, 스풀 큐 재처리, 차등 스캔, 오래된 캐시 무효화)
- 폴백 메커니즘(복구 감지 및 자동 전환)

## Phase 5 완료 내용

- 인증/권한 처리(JWT 토큰 패스스루, 권한 변경 시 캐시 무효화 카운터, Webhook 수신 준비)
- 보안 강화(파일 단위 AES-256 암호화, 감사 로그, 환자 ID SHA256 해싱, 90일 로그 보존)
- 헬스체크 및 관리 API(GET /health 상태 확인, GET /metrics Prometheus 메트릭, GET /api/cache/stats 캐시 통계)
- 구조화 로깅(JSON 액세스 로그, 에러 로그 분리, 타임스탬프/IP/메서드/URI/상태/캐시 상태/응답 시간 기록)
- Prometheus 메트릭(캐시 요청/바이트/제거 수, 스풀 큐 길이, 저널 재생 오류, 오리진 요청, 응답 시간 히스토그램)
- Windows Service 지원(windows-service 크레이트, 서비스 제어 핸들러, 서비스 상태 관리)

## Phase 6 완료 내용

- 부하 테스트 스크립트(k6 기반, 정상 운영: 100명/5,000 req/s/1시간, 피크 부하: 300명/10,000 req/s/10분, 대용량 파일: 100MB/동시 10건)
- 성능 벤치마크 도구(부하 테스트 자동화, 메트릭 수집 및 분석)
- 장애 시나리오 테스트 준비(네트워크 단절, 서버 재시작, 디스크 풀)
- 보안 테스트 준비(인증 우회 시도, 권한 없는 리소스 접근)

## 기술 스택

- **Rust 전면 개발:** 모든 컴포넌트(Axum HTTP 서버, reqwest 클라이언트, MongoDB, Tokio 비동기, 백그라운드 워커)를 Rust로 구현하여 단일 언어 스택 유지보수 효율성 확보

## 소스코드

- 소스코드: https://dev.azure.com/ewoosoft/prototypes/_git/scp-cache-poc?path=/poc4


