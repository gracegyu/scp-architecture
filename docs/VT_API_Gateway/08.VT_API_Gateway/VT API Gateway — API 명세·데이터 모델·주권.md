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
| v0.3 | 2026-07-06 | (SRS 동기화) | 데이터 모델 표를 device-중심 정체성·policy scope·egress SSOT로 정합 — Device=주체(clinic_id nullable)·Clinic=선택적 그룹, **Policy `tenant`→`scope_type/scope_id`·egress 제거**(§7.5.3), **Connector=egress SSOT(#31)**, UpstreamRegistry=target 서브도메인+연결 timeout(egress·재시도·서킷 제외, R1/R4). 정본=SRS §1.2·§6.4.1·§7.5.3·DBML |

출처: [PRD](<VT API Gateway — PRD (v2).md>) · [ARD](<VT API Gateway — ARD (아키텍처).md>) · [요구사항 명세](<VT API Gateway — 요구사항 명세 (Requirements).md>). 상세 OpenAPI는 LLD에서 확정.

## 1. API 표면 (MVP · OpenAPI 기준선)

**API 문서**: NestJS `@nestjs/swagger` code-first — 데코레이터에서 OpenAPI 자동 생성, `/api-docs` 노출. (상세 스펙은 LLD에서 확정.)

| 메서드 | 경로 | 설명 | FR |
| --- | --- | --- | --- |
| POST | /v1/auth/token | 디바이스 client_credentials → JWT 발급 | AUTH-01/02 |
| POST | /v1/enroll/start | enrollment 시작 → nonce challenge | ENR-01/03 |
| POST | /v1/enroll/complete | 서명+공개키(clientPublicKey) 검증 → device 등록(pending) + **clinic·region 확립**(Clinic-ID로 upsert, region 기본=GeoDNS 최근접·C/S override) | ENR-01/04·RGN-* |
| GET | /v1/region/resolve | device→region 해석(mapping_version) | RGN-01/02 |
| POST | /v1/clinics | 클리닉 관리 — 운영자(OneID) 교정·예외적 수동 등록 (**주 생성 경로는 enroll**) | RGN-* |
| POST | /v1/clinics/{clinicId}/org-bindings | 외부 provider Org-ID 등록(연동 연결 시·provider별) | INT-* |
| GET | /v1/regions | GW 운영 리전 목록 조회(클라이언트 region 선택지) | RGN-* |
| PUT | /v1/clinics/{clinicId}/region | 클리닉 접속 리전 **운영 중 변경**(재동의·감사) | RGN-04 |
| GET/POST | /v1/devices, /v1/devices/{id} | 디바이스 레지스트리·lifecycle | DEV-01/03 |
| POST | /admin/v1/devices/{id}/kill | kill-switch | FLEET-02 |
| GET | /admin/v1/... | 관리자·감사 조회(경량) | ADM/AUD |
| GET | /.well-known/<env>/server-configuration.json | 런타임 버전·호환성 공시(API/기능별 최소 클라이언트 버전) | COMPAT-02 |
| POST | `…/webhooks/<provider>` (provider별 등록·유연) | 외부 이벤트 수신(발신자 검증 HMAC·IP·timestamp·멱등) → 매핑 분배. **경로/형식은 provider 규약 수용, GW 비강제·payload 비해석** | WH-01~05 |
| POST | /v1/auth/oneid/verify | OneID(OIDC) 토큰 검증·연계(사람·클리닉·사내 호출자) | AUTH-08 |

※ 모든 클라이언트 요청에 **Vatech-* 식별 헤더**(Product·Version·OS·Clinic-Id·Via)를 부착 — API Compatibility Gate가 버전 호환을 판정(COMPAT-01). originator 권위 소스는 전용 헤더(`Vatech-Product`/`Version`/`OS`)이고, 경유 중계 홉은 `Vatech-Via`에 누적한다(`User-Agent`는 직전 송신자). **모든 제품의 모든 요청에 `Vatech-*` 식별 헤더 + 표준화 `User-Agent` 부착을 강제**하며 **공용 라이브러리**로 표준화한다(2026-06 회의 — 전 제품 필수). 상세는 SRS §7.7.1·Roadmap §5.1.

※ **라우팅 모델 = target-routed proxy**(§4.1.1·§4.1.2·ADR-11). GW는 **두 면**만 노출하고 `Vatech-Target` 헤더 유무로 배타적으로 가른다 — **없으면 위 표의 GW 고유 API(A)** 로 GW가 처리, **있으면 Proxy**로 등록 upstream에 전달. Proxy는 **`Vatech-Target`(논리 서비스 ID enum, 예 `cleverspace`/`axs`)을 레지스트리 allowlist→host로 해석**해 클라이언트가 친 **upstream 경로를 host만 바꿔 verbatim 전달**(body 그대로). **proxy 호출엔 `Vatech-Target` 필수**(누락 → `400`, 미등록/allowlist 외 → `404`/`403`). 내부(B)·외부(C) 구분은 trust profile뿐(라우팅 동일) — C는 OAuth·고정 egress IP 추가. 신규 upstream = **레지스트리 1행**(경로/코드 변경 0). 위 표는 A면만 나열하며, 원서버 호출(CleverSpace·AXS 등)은 Proxy면이라 본 표에 없다(upstream OpenAPI 정본). 정본: **SRS §4.1.2**.

> **`Vatech-Target`(라우팅, proxy 필수) ≠ `Vatech-*` 식별 헤더(버전 호환 필수, 위 ※).** 이름이 비슷하나 역할이 다르다.

※ 파일 업로드: **GW는 presigned를 발급하지 않는다.** 발급 주체는 CleverSpace(경로②)·AXS(경로③)이고 GW는 발급 요청을 **중계(B/C bypass)** 만 하며, 파일 바이트는 **발급 주체 storage로 직접** 업로드(GW 미경유). 위 표(A면)에 업로드 API가 없는 이유다. 상세 SRS §4.1.4·§7.4.

## 2. 데이터 모델 (핵심 엔터티)

| 엔터티 | 핵심 필드 | 비고 |
| --- | --- | --- |
| Device | device_id, client_id(nullable), client_public_key, clinic_id(nullable), status(lifecycle) | **GW 호출 주체(principal)** — v1.0=EzServer(clinic-bound), 미래 비-EzServer/clinic-less 가능(§1.2). PHI 없음 · region은 clinic 파생(A안) · **인증 자격 통합**(별도 Credential 테이블 없음): private_key_jwt(client_id+공개키(client_public_key), 공유 secret 없음) |
| Policy | scope_type(global/clinic/device)/scope_id/connector, allowed_endpoints, scopes | OPA · 주체=device, 실효=device→clinic→global(§7.5.3) · **egress는 Connector SSOT #31** |
| Connector | name(axs), endpoint, credential_ref, **egress_allowlist(egress SSOT #31)** | adapter · 외부(C) 자격·egress 단일 홈 |
| AuditLog | ts, actor, action, result | append-only |
| FleetState | device_id, last_heartbeat, success_rate | 관측 |
| CompatMatrix | api/feature, min_client_version, error_code, fallback | 호환성 단일 소스 |
| WebhookEvent | event_id, provider, external_org_id, clinic_id, region, payload_ref, state, target | 멱등·분배 상태·해석된 대상(GW payload 비해석) |
| Clinic | clinic_id, region, mapping_version | device의 **선택적 그룹**(clinic-종속 정보 홈: region·policy 기본·provider-org) · 라우팅 키 통합(device↔clinic) |
| **RegionCatalog** | region_id, display_name, endpoint, status(active/draining/planned), is_default | **GW 운영 리전 목록**(region list API SSOT, §7.3.6) |
| **OrgMapping** | provider, external_org_id, clinic_id, mapping_version | **webhook 라우팅 키** — (provider·Org-ID)→clinic→region |
| **WebhookProvider** | provider, inbound_route, sig_scheme, secret_ref, source_ip_allowlist, org_id_path | **유연 수신 config** — 발신자 검증·라우팅 키 추출(GW 비해석) |
| **UpstreamRegistry** | target_id(=target 서브도메인 라벨), host, profile(internal/external), connect/response/total_deadline_ms, enabled | **target 서브도메인 proxy 라우팅**(ADR-11·7/2 R1) · GW 연결 timeout(D1~D3) · egress=Connector, 재시도·서킷=istio |
| **DeliveryChannel** | clinic_id, channel_type(mqtt_edge/http_cloud), endpoint | webhook 분배 채널(Edge MQTT/Cloud HTTP) |

> **Enrollment 모델(2026-07-01 확정)**: 부트스트랩 신뢰 = **LM 라이선스·Clinic-ID**(EzServer가 설치 시 LMP에서 수신)이며, **공장 토큰/OOB 코드·사전 발급 토큰은 미도입**(과거 `EnrollmentToken`/`token_ref` 폐기). 흐름: enroll(라이선스·Clinic-ID 검증 + nonce·공개키(client_public_key) 바인딩) → `device.status=pending` → **C/S(현장 설치 담당)의 GW Console 승인** → `active`(인증 허용). 사람 승인이 신뢰 앵커라 Clinic-ID 위·변조 가짜 등록을 차단한다. 승인 대기 상태는 별도 테이블 없이 `device.pending`, 이력은 `AuditLog`. **이후 디바이스 인증 = 비대칭 `private_key_jwt`**(enroll 키페어 개인키 서명 → `client_public_key` 공개키 검증, 공유 secret 없음, ADR-13·§7.1.1). 정본: SRS §2.3.1·§7.1.1·§7.2.5·§7.9.2 · ARD §5.1.

## 3. 데이터 주권 매핑

- **PHI(환자 영상)**: **발급 주체(CleverSpace/AXS) storage**에만 저장 · GW control plane 미경유 · 리전 밖 미이동.
- GW control plane은 **메타데이터만**(device_id·region·매핑·token) — PHI·업로드 객체 키를 저장하지 않음(세션·object_key는 발급 주체 소유).
- presigned URL은 **매핑 리전 endpoint**만 지시. cross-border는 consent·classification 게이팅(COMP).