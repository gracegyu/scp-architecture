**문서 통제**

| 항목        | 내용                                         |
| --- | --- |
| 문서 ID | ESIP-GW-REQ |
| 문서 버전 | v1.2 |
| 적용 제품 버전 | gw/1.0.0.0~ |
| 분류 | 통제 문서 (Controlled · IEC 62304 / ISO 13485 — 요구사항 추적성) |
| 상태 | Draft |
| PRD | [PRD (v2)](<VT API Gateway — PRD (v2).md>) |

**원칙**: 모든 요구사항을 빠짐없이 등록하고 **목표 버전**을 배정한다(누락이 아니라 일정 배치). **v1.0(MVP)은 데모가 아니라 'v1.0 요구사항 전부 구현 + 수용 기준 통과'로 제대로 동작하는 완결 제품**이다. 현재 전체 67개 중 v1.0 배정 54개 (ESMN Roadmap 흡수 14건 추가 — COMPAT·WH·OneID·라우팅 키). 각 FR은 11장 수용 기준과 추적 연결.

**심도(depth) 정책**: 총 공수 ≤ 9.5MM(목표 그 이하). 핵심 요구사항은 제대로 구현하되, **감사(AUD-01) · RBAC(ADM-02) · 관리자 UI(ADM-01) · consent(COMP-01) · 분류 태깅(COMP-02)은 v1.0에서 경량(MVP 수준)**으로 구현한다. 제외 항목(DPoP·멀티클라우드·10만대 마이그)은 post-MVP. 2단계: core(gw/1.0.0.b1) → full(gw/1.0.0.0).

## 1. 기능 요구사항 (FR)

### **인증 / 토큰 (AUTH)**

| ID | 요구사항 | 우선 | 버전 | 수용 기준 |
| --- | --- | --- | --- | --- |
| FR-AUTH-01 | 디바이스 OAuth2 client_credentials 인증 | M | v1.0 | 토큰 발급·검증 성공 |
| FR-AUTH-02 | 사내 호출자 JWT 발급·검증 | M | v1.0 | JWT 발급·서명 검증 |
| FR-AUTH-03 | 외부 토큰 저장·자동 갱신(암호화) | M | v1.0 | 만료 전 자동 갱신·평문 미노출 |
| FR-AUTH-04 | secret 자동 회전(dual-window) | M | v1.0 | 무중단 교체 |
| FR-AUTH-05 | token claim hard binding(device/region/aud/TTL) | M | v1.0 | claim 강제·검증 |
| FR-AUTH-06 | DPoP (sender-constrained) | M | v1.1 | 타 위치 replay 차단 |
| FR-AUTH-07 | 하드웨어 키(SE/TPM) 보관 | M | v1.1 | 키 비추출 |
| FR-AUTH-08 | OneID(OIDC) 연계 — 사람·클리닉·사내 호출자(EzServer/CleverOne) 인증 | M | v1.0 | OneID 토큰 검증·연계 성공 |
| FR-AUTH-09 | 디바이스 머신 인증 ↔ OneID 신원 분리·매핑(2면 공존) | M | v1.0 | 두 surface 분리·매핑 검증 |

### **디바이스 레지스트리 (DEV)**

| ID | 요구사항 | 우선 | 버전 | 수용 기준 |
| --- | --- | --- | --- | --- |
| FR-DEV-01 | 디바이스 레지스트리(등록·조회) | M | v1.0 | CRUD·조회 |
| FR-DEV-02 | allowlist 접근 통제(OPA) | M | v1.0 | 미등록 차단 |
| FR-DEV-03 | lifecycle(pending→active→suspended→revoked) | M | v1.0 | 상태 전이·이력 |
| FR-DEV-04 | revocation(강한 일관성) | M | v1.0 | 즉시 차단 |

### **온보딩 (ENR)**

| ID | 요구사항 | 우선 | 버전 | 수용 기준 |
| --- | --- | --- | --- | --- |
| FR-ENR-01 | enrollment token 발급 = allowlist 등록 | M | v1.0 | 토큰 기반 등록 |
| FR-ENR-02 | 공장 토큰 / OOB 일회 코드 부트스트랩 | M | v1.0 | 1회·짧은 TTL |
| FR-ENR-03 | nonce challenge(replay 방지) | M | v1.0 | 서버 nonce 서명 |
| FR-ENR-04 | device fingerprint 바인딩 | S | v1.0 | HW 특성 바인딩 |
| FR-ENR-05 | geo/velocity 이상탐지 | S | v1.1 | 이상 등록 탐지 |
| FR-ENR-06 | 하드웨어 attestation | S | v1.1 | 제조사 인증서 |

### **리전 / 라우팅 / 주권 (RGN)**

| ID | 요구사항 | 우선 | 버전 | 수용 기준 |
| --- | --- | --- | --- | --- |
| FR-RGN-01 | device→region resolver(단일 리전) | M | v1.0 | 매핑 라우팅 |
| FR-RGN-02 | mapping_version(drift·롤백) | M | v1.0 | 버전 추적 |
| FR-RGN-03 | PHI 리전 밖 미이동 보장 | M | v1.0 | 경계 검증 |
| FR-RGN-04 | region reassign/override + audit(relocation) | S | v1.0 | 재지정·감사·재동의 |
| FR-RGN-05 | 멀티 리전 + 리전 signer 다수 | M | v1.2 | 다리전 동작 |
| FR-RGN-06 | 라우팅 키 통합 — clinic_id↔device↔region (resolver가 device_id·clinic_id 모두 수용) | M | v1.0 | 두 키로 동일 리전 해석 |

### **업로드 세션 / 데이터 (SES)**

| ID | 요구사항 | 우선 | 버전 | 수용 기준 |
| --- | --- | --- | --- | --- |
| FR-SES-01 | upload session(start→chunk→commit) | M | v1.0 | 세션 수명주기 |
| FR-SES-02 | presigned URL 디바이스→리전 직결 | M | v1.0 | GW 미경유 업로드 |
| FR-SES-03 | resumable/multipart | M | v1.0 | 중단 재개 |
| FR-SES-04 | idempotency key | M | v1.0 | 중복 commit 방지 |
| FR-SES-05 | checksum/ETag 무결성 | M | v1.0 | 무결성 검증 |
| FR-SES-06 | 멀티클라우드 presign broker(S3/Blob/GCS/MinIO) | M | v1.2 | 이종 스토리지 |

### **연동 / Connector (INT)**

| ID | 요구사항 | 우선 | 버전 | 수용 기준 |
| --- | --- | --- | --- | --- |
| FR-INT-01 | connector(adapter) 프레임워크 | M | v1.0 | 플러그형 등록 |
| FR-INT-02 | Straumann AXS connector(OAuth2·proxy·파일) | M | v1.0 | AXS E2E |
| FR-INT-03 | connector별 egress 정책 + endpoint allowlist | M | v1.0 | 허용 대상만 |
| FR-INT-04 | 추가 connector(DS Core/3Shape) | S | v1.1 | 설정 추가 |

### **Fleet 운영 (FLEET)**

| ID | 요구사항 | 우선 | 버전 | 수용 기준 |
| --- | --- | --- | --- | --- |
| FR-FLEET-01 | device heartbeat·상태 가시성 | M | v1.0 | health 수집 |
| FR-FLEET-02 | kill-switch(긴급 정지) | M | v1.0 | 즉시 정지 |
| FR-FLEET-03 | upload 성공률·오류 분포 지표 | S | v1.0 | 지표 노출 |
| FR-FLEET-04 | config rollout/카나리 | S | v1.1 | 단계 배포 |
| FR-FLEET-05 | 10만대 운영 최적화 | M | v2.0 | 대규모 안정 |

### **Config (CFG)**

| ID | 요구사항 | 우선 | 버전 | 수용 기준 |
| --- | --- | --- | --- | --- |
| FR-CFG-01 | 중앙 config push/pull(타겟팅) | M | v1.0 | 원격 적용 |

### **마이그레이션 (MIG)**

| ID | 요구사항 | 우선 | 버전 | 수용 기준 |
| --- | --- | --- | --- | --- |
| FR-MIG-01 | dual-run(레거시+신규 병행) | M | v2.0 | 무중단 병행 |
| FR-MIG-02 | 단계적 cutover(카나리) | M | v2.0 | 리전·고객 단위 |
| FR-MIG-03 | enrollment 백필 | M | v2.0 | 소급 등록 |
| FR-MIG-04 | clock skew(NTP/허용오차) | M | v2.0 | 시계 오차 수용 |

### **관리 / 감사 / 컴플라이언스 (ADM/AUD/COMP)**

| ID | 요구사항 | 우선 | 버전 | 수용 기준 |
| --- | --- | --- | --- | --- |
| FR-ADM-01 | 테넌트·키·디바이스 관리 UI | M | v1.0 | CRUD UI |
| FR-ADM-02 | 운영자 RBAC | M | v1.0 | 권한 분리 |
| FR-AUD-01 | 감사 로그(append-only) | M | v1.0 | 변조 방지·보존 |
| FR-COMP-01 | data classification tagging(→OPA) | M | v1.0 | 태그 기반 게이팅 |
| FR-COMP-02 | cross-border consent tracking | M | v1.0~v2.0 | 동의 추적 |

### **API 버전 호환성 (COMPAT)**

ESMN Roadmap 1단계 흡수. GW 신설 전에도 기존 경로에서 **즉시** 적용 — CleverSpace v1.3.0 일정의 호환성 문제에 우선 대응.

| ID | 요구사항 | 우선 | 버전 | 수용 기준 |
| --- | --- | --- | --- | --- |
| FR-COMPAT-01 | Vatech-* 식별 헤더(Product·Version·OS·Clinic-Id·Via) 표준 | M | v1.0 | 헤더 파싱·originator 식별 |
| FR-COMPAT-02 | well-known 런타임 버전 공시(API/기능별 최소 클라이언트 버전) | M | v1.0 | 런타임 공시·캐시 |
| FR-COMPAT-03 | 서버 버전 체크(validate-limits 사전검증) | M | v1.0 | 버전 게이팅 |
| FR-COMPAT-04 | 오류코드 매핑·fallback(업데이트 필요 안내) | M | v1.0 | 표준 오류·fallback |
| FR-COMPAT-05 | 호환성 매트릭스 단일 소스(빌드/CI 반영) | M | v1.0 | 매트릭스 동결·CI 검증 |

### **외부 이벤트 / Webhook (WH)**

ESMN Roadmap §2.7 흡수. GW가 외부 이벤트의 단일 수신·분배점. b1(pilot)에 AXS forward + Edge(EzServer) MQTT 역방향(WH-06) 포함 — AXS pilot 일정 반영.

| ID | 요구사항 | 우선 | 버전 | 수용 기준 |
| --- | --- | --- | --- | --- |
| FR-WH-01 | 외부 Webhook 단일 수신 엔드포인트(/webhooks/<provider>) | M | v1.0 | 단일 진입·수신 |
| FR-WH-02 | 수신 검증(HMAC 서명·IP allowlist·timestamp) | M | v1.0 | 부정 호출 거부 |
| FR-WH-03 | 멱등 처리(eventId dedup) | M | v1.0 | 중복 1회 처리 |
| FR-WH-04 | 빠른 ACK + 내부 큐(재시도·백오프·DLQ) | M | v1.0 | 2xx 즉시·큐 위임 |
| FR-WH-05 | 클라우드 분배(HTTP push, 내부망) | M | v1.0 | 대상 전달·순서 |
| FR-WH-06 | Edge 분배 — EzServer MQTT(QoS1·persistent·토픽 클리닉 단위) | M | v1.0 | 오프라인 버퍼·재전달 |

## 2. 비기능 요구사항

### **비기능 (NFR)**

| ID | 요구사항 | 우선 |
| --- | --- | --- |
| NFR-SEC | 전 구간 TLS·KMS·최소 IAM·PII/PHI 비저장 | v1.0 |
| NFR-PERF | 인증·프록시 p95 < 300ms(파일 제외) | v1.0 |
| NFR-AVA | Multi-AZ ≥ 99.9%(v1.0) → 글로벌 active-active(v1.2) | v1.0~ |
| NFR-SCL | 플랫폼·테넌트·리전 추가 설정 기반 O(1) | v1.0 |
| NFR-OBS | 구조화 로그·메트릭·감사 분리 | v1.0 |
| NFR-MNT | IaC 환경 재현 | v1.0 |

## 3. 버전 배정 요약

- **v1.0 (MVP · 제대로 동작)**: 인증 코어·디바이스 레지스트리·enrollment·단일 리전 주권·업로드 세션·AXS connector·egress·fleet 기본(heartbeat/kill-switch)·config·감사·RBAC·NFR 전부.
- **v1.1**: DPoP+HW키·하드웨어 attestation·fleet 확장·2nd connector.
- **v1.2**: 멀티 리전·멀티클라우드 presign·signer 확장.
- **v2.0**: 레거시 10만대 마이그레이션.
- **Roadmap 흡수 (v1.0)**: API 버전 호환성(COMPAT-01~05)·OneID 인증면(AUTH-08/09)·Webhook Receiver(WH-01~06, Edge MQTT 역방향 포함)·라우팅 키 통합(RGN-06).