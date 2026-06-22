**문서 통제**

| 항목        | 내용                                         |
| --- | --- |
| 문서 ID | ESIP-GW-API |
| 문서 버전 | v0.2 (Roadmap 흡수) |
| 적용 제품 버전 | gw/1.0.0.0 |
| 분류 | 통제 문서 (Controlled · IEC 62304 / ISO 13485) |
| 상태 | Draft |

## 0. 개정 이력

| 버전 | 일자 | 작성 | 변경 |
| --- | --- | --- | --- |
| v0.1 | 2026-06-08 | Scott | API 표면·데이터 모델·주권 매핑 초안 |
| v0.2 | 2026-06-15 | Scott | Roadmap 흡수 — well-known·Webhook·OneID 엔드포인트, 호환성·이벤트·클리닉매핑 엔터티 추가 |

출처: [PRD](<VT API Gateway — PRD (v2).md>) · [ARD](<VT API Gateway — ARD (아키텍처).md>) · [요구사항 명세](<VT API Gateway — 요구사항 명세 (Requirements).md>). 상세 OpenAPI는 LLD에서 확정.

## 1. API 표면 (MVP · OpenAPI 기준선)

**API 문서**: NestJS `@nestjs/swagger` code-first — 데코레이터에서 OpenAPI 자동 생성, `/api-docs` 노출. (상세 스펙은 LLD에서 확정.)

| 메서드 | 경로 | 설명 | FR |
| --- | --- | --- | --- |
| POST | /v1/auth/token | 디바이스 client_credentials → JWT 발급 | AUTH-01/02 |
| POST | /v1/enroll/start | enrollment 시작 → nonce challenge | ENR-01/03 |
| POST | /v1/enroll/complete | 서명+fingerprint 검증 → 자격 발급(allowlist 등록) | ENR-01/04 |
| GET | /v1/region/resolve | device→region 해석(mapping_version) | RGN-01/02 |
| POST | /v1/uploads | 업로드 세션 start(정책·region 검사) | SES-01 |
| POST | /v1/uploads/{id}/chunks | chunk presigned URL 발급(짧은 TTL) | SES-02/03 |
| POST | /v1/uploads/{id}/commit | 무결성 확인·확정(idempotency) | SES-04/05 |
| ANY | /v1/{tenant}/connectors/axs/* | AXS proxy(OAuth2 위임) | INT-02 |
| GET/POST | /v1/devices, /v1/devices/{id} | 디바이스 레지스트리·lifecycle | DEV-01/03 |
| POST | /admin/v1/devices/{id}/kill | kill-switch | FLEET-02 |
| GET | /admin/v1/... | 관리자·감사 조회(경량) | ADM/AUD |
| GET | /.well-known/<env>/server-configuration.json | 런타임 버전·호환성 공시(API/기능별 최소 클라이언트 버전) | COMPAT-02 |
| POST | /v1/webhooks/{provider} | 외부 이벤트 수신(HMAC·IP·timestamp·멱등) → 내부 큐 분배 | WH-01~05 |
| POST | /v1/auth/oneid/verify | OneID(OIDC) 토큰 검증·연계(사람·클리닉·사내 호출자) | AUTH-08 |

※ 모든 클라이언트 요청에 **Vatech-* 식별 헤더**(Product·Version·OS·Clinic-Id·Via)를 부착 — API Compatibility Gate가 버전 호환을 판정(COMPAT-01). originator 권위 소스는 전용 헤더.

※ **라우팅의 SSOT는 경로/호스트 네임스페이스**(서버측 라우트 테이블). **handle**(GW 고유 API, A버킷) **vs bypass**(B 내부 프록시 `/cs/*`·`/oneid/*` 등 · C 외부 커넥터 `/v1/{tenant}/connectors/*`)는 **경로로 정적 결정**되며, A 예약 네임스페이스(`/v1/<고정 세그먼트>`·`/admin/v1/*`·`/.well-known/*`)는 B/C·tenant 경로가 침범할 수 없다(reserved-segment). **`Vatech-Target`(논리 서비스 ID)은 의무 헤더가 아니라 보조 가드** — 보내면 allowlist·경로 파생 target과 일치 검증(불일치 `400`), 없어도 경로만으로 라우팅 성립. (위 ※의 **`Vatech-*` 식별 헤더는 버전 호환용 필수**, **`Vatech-Target`은 라우팅 보조용 선택** — 역할이 다름.) 정본: **SRS §4.1.2**.

※ 대용량 파일 바이트는 게이트웨이 미경유(디바이스→리전 storage presigned 직결).

## 2. 데이터 모델 (핵심 엔터티)

| 엔터티 | 핵심 필드 | 비고 |
| --- | --- | --- |
| Device | device_id, fingerprint, region, status(lifecycle) | PHI 없음 |
| EnrollmentToken | token_ref, serial, expires_at, used | 1회·짧은 TTL |
| Credential | device_id, client_id, secret_ref(KMS), hw_key_bound | 시크릿 참조만 |
| Token | device_id, jwt_claims, expires_at | claim binding |
| RegionMapping | device_id, region, mapping_version | drift·롤백 |
| UploadSession | session_id, device_id, region, object_key, status | PHI 미포함 키 |
| Policy | tenant/connector, allowed_endpoints, scopes, egress | OPA |
| Connector | name(axs), endpoint, credential_ref, egress_allowlist | adapter |
| AuditLog | ts, actor, action, result | append-only |
| FleetState | device_id, last_heartbeat, success_rate | 관측 |
| CompatMatrix | api/feature, min_client_version, error_code, fallback | 호환성 단일 소스 |
| WebhookEvent | event_id, provider, payload_ref, state(received/dispatched), target | 멱등·분배 |
| ClinicRegionMapping | clinic_id, region, mapping_version | 라우팅 키 통합(device↔clinic) |

## 3. 데이터 주권 매핑

- **PHI(환자 영상)**: 리전 storage에만 저장 · control plane 미경유 · 리전 밖 미이동.
- control plane은 **메타데이터만**(device_id·region·object_key·token) — 객체 키/메타에 PHI 미포함.
- presigned URL은 **매핑 리전 endpoint**만 지시. cross-border는 consent·classification 게이팅(COMP).