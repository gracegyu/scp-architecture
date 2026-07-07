# Vatech API Gateway — Redis(=Valkey) 키스페이스 카탈로그 (설계 초안)

> **엔진 = Valkey**(AWS=ElastiCache for Valkey). Valkey는 Redis 포크로 **RESP 프로토콜·클라이언트·명령·키스페이스가 완전 호환**이라 본 카탈로그(키 패턴·TTL·자료형)가 그대로 적용된다. 문서 내 "Redis"는 Redis 호환(=Valkey)을 가리킨다(SRS §1.4). 키 프리픽스(`gw:…`)·파일명은 변경 없음.
> dev-chain-design 산출물. `design/dbml`(PostgreSQL SSOT)·`design/openapi`와 나란히 둔다.
> **Redis는 SSOT가 아니다** — PostgreSQL이 SSOT(`design/dbml`). Redis는 **① 캐시**(원본에서 재구성 가능 — 대부분 PG, 일부 KMS/S3) + **② 휘발 상태**(nonce·멱등·dedup·rate-limit·lock·폐기 denylist)만 보관한다.
> 정밀 자료형·TTL 값은 LLD에서 확정. 본 문서는 키 네임스페이스·용도·종류(cache/ephemeral)·재구성 출처를 고정한다.
> **값(value) 내부 스키마는 여기서 재정의하지 않는다** — `자료형`(Redis 타입)만 고정하고, 값의 필드 구성·JSON 모양은 **재구성 출처(SSOT: DBML 행 / OpenAPI 스키마 / well-known)** 를 그대로 따른다(중복·드리프트 방지). 출처로 덮이지 않는 비자명한 값 구조만 `비고`/`용도`에 명시한다.

## 원칙

- **SSOT 아님**: 캐시 손실은 원본에서 재구성(cache-aside). 휘발 상태 손실은 보안/멱등에 영향이 있으나 영속 데이터가 아니다(짧은 TTL).
- **TTL 필수**: 모든 키에 TTL — 키 누수 방지. cache는 TTL + `mapping_version`/버전 변화 시 무효화(§7.3.2).
- **멀티 서버**: 한 리전 내 모든 pod가 **동일 Redis 공유**(§2.1.1) — 멱등·dedup·rate-limit·폐기 전파·캐시 무효화가 인스턴스 간 일관.
- **멀티 리전**: Redis는 **리전 로컬**. 전역 데이터(매핑·레지스트리·JWKS)는 **각 리전이 로컬 PostgreSQL(복제본)에서 캐시**하며 Redis끼리 교차 복제하지 않는다(§2.1.1).
- **PHI 미저장**(§6.4). 객체 키/메타에 환자정보 미포함.
- **네이밍**: `gw:{class}:{...}` — `class` = `cache` | `nonce` | `idemp` | `wh` | `rl` | `lock` | `revoked`. 콜론(`:`) 계층 구분.

## ① 캐시 (rebuildable — 원본에서 재구성 · 출처 대부분 PostgreSQL, 단 `compat`=S3·`jwks`/`wh-secret`/`conn-token`=KMS — TTL + 버전 무효화)

| 키 패턴 | 자료형 | TTL(예시) | 용도 | 재구성 출처 |
| --- | --- | --- | --- | --- |
| `gw:cache:clinic-region:{clinicId}` | string/hash | 초~분 | clinic→region 해석(§7.3.1) | `clinic`(region 컬럼) |
| `gw:cache:device-region:{deviceId}` | string/hash | 초~분 | device→region 해석(파생) | `device.clinic_id → clinic.region`(region A안, `region_mapping` 폐기·§6.4.1) |
| `gw:cache:device:{clientId}` | hash | 초~분 | **디바이스 인증 hot path 캐시**(private_key_jwt 검증용 `client_public_key`·`status`·`clinic_id`·region, §7.1.1·§2.3.2) — 매 토큰 발급마다 조회 | `device`(+clinic 파생). **revoke/kill·status 변경 시 즉시 삭제**(§7.2.4, 아래 폐기 모델). clientId↔deviceId 1:1 |
| `gw:cache:org:{targetId}:{externalOrgId}` | string | 초~분 | webhook 라우팅 키(org→clinic, §2.3.6) | `org_mapping` |
| `gw:cache:upstream:{targetId}` | hash | 분 | 연동 대상(upstream) config(서브도메인 라벨→host·profile·timeout·webhook 수신 config, §4.1.2·§7.6) | `upstream` |
| `gw:cache:webhook-host:{inboundHost}` | string | 분 | **webhook 발신자 식별 역조회**(수신 Host/SNI → `target_id`, §7.6.2·§2.3.6) — `upstream`은 targetId 키라 역방향 인덱스 필요 | `upstream.inbound_host`(역인덱스) |
| `gw:cache:wh-secret:{targetId}` | string | 짧음 | **webhook HMAC 검증 시크릿**(§7.6.2) — `secret_ref`로 KMS에서 로드, **비밀 취급**(로그 미기록·§6.2) | KMS(`upstream.secret_ref`) |
| `gw:cache:regions` | hash/json | 분 | GW 운영 리전 목록(§7.3.6) | `region_catalog` |
| `gw:cache:jwks:{issuer}` | string/json | 분 | **발급기별 JWKS(공개키)** — ① 운영자 IdP(직원 MS365/Entra·§7.1.4 토큰 검증) · ② (enroll B안) **LMP 제3자 서명 attestation 검증**(§2.3.1 B·③-P-LMP). issuer별 런타임 fetch+캐시. device 공개키는 `cache:device`(디바이스별·DB) | 각 발급기 JWKS 엔드포인트 |
| `gw:cache:compat` | hash | 분 | 호환성 매트릭스/well-known(§7.7) | **well-known JSON(리전 로컬 S3·CI 발행·§7.7.5) — PG 아님**(`compat_matrix` 테이블 폐기, 2026-07-01) |
| `gw:cache:conn-token:{targetId}` | string | 토큰 만료 전(선제 갱신) | **아웃바운드 OAuth2 access token** 캐시(§7.1.3) — GW가 external(C) 호출에 쓰는 토큰. **만료 전 자동 갱신**(만료 후 아님) | upstream 토큰 엔드포인트(자격=`upstream.credential_ref`, KMS) |
| `gw:cache:config:gw` | hash/json | 초~분 | **v1.0** GW-내부 실효 config(`gw.*` · region/global 병합, pod 공유·§7.8.4) — heartbeat 응답의 주기·`configVersion` 산출 | `config`(`gw.*` 기여 행) |
| `gw:cache:config:{deviceId}` | hash/json | 초~분 | **gw/1.1+** device **실효 config**(`device.*` · device>clinic>region>global 병합 + `configVersion`, pull `GET /v1/fleet/config`·heartbeat) — v1.0 미사용 | `config`(기여 스코프 행 병합) |

> cache 무효화: 원본 변경 시 `mapping_version`/버전 키 증가 → 캐시 미스 시 강한 일관성 경로로 재적재(§7.3.1).
>
> **비밀 취급 캐시(`conn-token`·`wh-secret`)**: bearer/HMAC 자격이라 **로그 미기록(§6.2)·네트워크 격리·짧은 TTL**. 크리덴셜/시크릿 **원문은 캐시가 아니라 KMS**(`upstream.credential_ref`·`upstream.secret_ref`)에만 둔다.

## ② 휘발 상태 (ephemeral — PG에 없거나 파생 제어신호, 짧은 TTL)

| 키 패턴 | 자료형 | TTL | 용도 | 비고 |
| --- | --- | --- | --- | --- |
| `gw:nonce:enroll:{challengeId}` | string | 짧음(분) | enrollment nonce challenge(§7.2.6) | 1회용·재사용 거부 |
| `gw:idemp:{scope}:{key}` | string | 시간~일 | idempotency(업로드 commit·요청 멱등, §4.5) | 저장 결과 ref/상태 |
| `gw:wh:dedup:{targetId}:{eventId}` | string | 시간~일 | webhook eventId 중복 처리 방지(§7.6.4) | 인스턴스 공유 필수 |
| `gw:rl:{subject}:{window}` | counter(string/INCR) | window 길이 | rate-limit 카운터(§7.1.1 토큰·**무인증 enroll은 IP/서브넷 subject**·§7.2 R9) | 윈도우 만료 시 자동 소멸 |
| `gw:revoked:{deviceId}` | string(SET) | ≈ access token 최대 수명 | **폐기 디바이스 denylist**(kill/revoke 즉시 전파·§7.2.4) — 이미 발급된 **단명 토큰을 만료 전 차단**(그 후엔 토큰이 자연 만료라 키 불요) | 출처=`device.status=revoked`(PG)·멀티 pod 공유 필수 |
| `gw:lock:{resource}` | string(SET NX) | 짧음(초) | 분산 락(선택 — 단발 작업 직렬화) | 필요 시만 |

> **폐기(revocation) 모델(§7.2.4)** — "revoked 디바이스 즉시 차단(캐시 TTL 무관)"의 실제 구현:
> 1. kill/revoke 시 **`gw:cache:device:{clientId}` 즉시 삭제** → 다음 인증이 PG를 재조회해 `revoked` 확인 → **신규 토큰 발급 차단**.
> 2. **`gw:revoked:{deviceId}` denylist 등재**(TTL=access token 최대 수명) → 이미 발급된 무상태 JWT도 만료 전 요청 경로에서 차단.
> 모든 pod가 **동일 Redis 공유**(§2.1.1)라 두 조치가 즉시 전파된다. access token 자체는 무상태 JWT라 저장하지 않는다(§7.1.1·ADR-02).

## 매핑

- 캐시 키 ↔ 출처: 위 "재구성 출처" 열이 SSOT 링크. 대부분 **PostgreSQL**(`design/dbml`)이며, 예외는 **`compat`=S3 well-known(§7.7.5)** · **`jwks`=발급기 JWKS** · **`wh-secret`/`conn-token`=KMS**. DBML·§7.7.5 변경 시 본 카탈로그 동기화.
- 본 카탈로그는 SRS §3.1.2·§6.4·§2.1.1에서 참조한다.
