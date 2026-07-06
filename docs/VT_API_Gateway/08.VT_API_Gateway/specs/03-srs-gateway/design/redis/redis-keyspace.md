# Vatech API Gateway — Redis(=Valkey) 키스페이스 카탈로그 (설계 초안)

> **엔진 = Valkey**(AWS=ElastiCache for Valkey). Valkey는 Redis 포크로 **RESP 프로토콜·클라이언트·명령·키스페이스가 완전 호환**이라 본 카탈로그(키 패턴·TTL·자료형)가 그대로 적용된다. 문서 내 "Redis"는 Redis 호환(=Valkey)을 가리킨다(SRS §1.4). 키 프리픽스(`gw:…`)·파일명은 변경 없음.
> dev-chain-design 산출물. `design/dbml`(PostgreSQL SSOT)·`design/openapi`와 나란히 둔다.
> **Redis는 SSOT가 아니다** — PostgreSQL이 SSOT(`design/dbml`). Redis는 **① 캐시**(PG에서 재구성 가능) + **② 휘발 상태**(nonce·멱등·dedup·rate-limit·lock)만 보관한다.
> 정밀 자료형·TTL 값은 LLD에서 확정. 본 문서는 키 네임스페이스·용도·종류(cache/ephemeral)·재구성 출처를 고정한다.

## 원칙

- **SSOT 아님**: 캐시 손실은 PG에서 재구성(cache-aside). 휘발 상태 손실은 보안/멱등에 영향이 있으나 영속 데이터가 아니다(짧은 TTL).
- **TTL 필수**: 모든 키에 TTL — 키 누수 방지. cache는 TTL + `mapping_version` 변화 시 무효화(§7.3.2).
- **멀티 서버**: 한 리전 내 모든 pod가 **동일 Redis 공유**(§2.1.1) — 멱등·dedup·rate-limit이 인스턴스 간 일관.
- **멀티 리전**: Redis는 **리전 로컬**. 전역 데이터(매핑·레지스트리·JWKS)는 **각 리전이 로컬 PostgreSQL(복제본)에서 캐시**하며 Redis끼리 교차 복제하지 않는다(§2.1.1).
- **PHI 미저장**(§6.4). 객체 키/메타에 환자정보 미포함.
- **네이밍**: `gw:{class}:{...}` — `class` = `cache` | `nonce` | `idemp` | `wh` | `rl` | `lock`. 콜론(`:`) 계층 구분.

## ① 캐시 (rebuildable — PostgreSQL이 출처, TTL + mapping_version 무효화)

| 키 패턴 | 자료형 | TTL(예시) | 용도 | 재구성 출처(PG) |
| --- | --- | --- | --- | --- |
| `gw:cache:clinic-region:{clinicId}` | string/hash | 초~분 | clinic→region 해석(§7.3.1) | `clinic`(region 컬럼) |
| `gw:cache:device-region:{deviceId}` | string/hash | 초~분 | device→region 해석(파생) | `device.clinic_id → clinic.region`(region A안, `region_mapping` 폐기·§6.4.1) |
| `gw:cache:org:{provider}:{externalOrgId}` | string | 초~분 | webhook 라우팅 키(org→clinic, §2.3.6) | `org_mapping` |
| `gw:cache:provider:{provider}` | hash | 분 | 연동 대상 config(서브도메인 라벨→host·profile·timeout·webhook 수신 config, §4.1.2·§7.6) | `provider` |
| `gw:cache:regions` | hash/json | 분 | GW 운영 리전 목록(§7.3.6) | `region_catalog` |
| `gw:cache:jwks` | string/json | 분 | 토큰 검증 공개키(§7.1.2) | 키 저장소(KMS)/발급기 |
| `gw:cache:compat` | hash | 분 | 호환성 매트릭스/well-known(§7.7) | `compat_matrix` |
| `gw:cache:conn-token:{provider}` | string | 토큰 만료 전(선제 갱신) | **아웃바운드 OAuth2 access token** 캐시(§7.1.3) — GW가 external(C) 호출에 쓰는 토큰. **만료 전 자동 갱신**(만료 후 아님) | provider 토큰 엔드포인트(자격=`provider.credential_ref`, KMS) |
| `gw:cache:config:{deviceId}` | hash/json | 초~분 | device **실효 config** 캐시(§7.8.4) — 키별 device>clinic>region>global 병합 결과 + `configVersion`. pull(`GET /v1/fleet/config`)·heartbeat 응답에 사용 | `config`(기여 스코프 행 병합) |

> cache 무효화: 원본 변경 시 `mapping_version`/버전 키 증가 → 캐시 미스 시 강한 일관성 경로로 재적재(§7.3.1).
>
> **`gw:cache:conn-token`은 bearer 자격이라 비밀로 다룬다** — 로그 미기록(§6.2), 네트워크 격리, 토큰 만료보다 짧은 TTL(만료 전 갱신). 크리덴셜 원문은 캐시가 아니라 KMS(`provider.credential_ref`)에만 둔다.

## ② 휘발 상태 (ephemeral — PG에 없음, 재구성 불가, 짧은 TTL)

| 키 패턴 | 자료형 | TTL | 용도 | 비고 |
| --- | --- | --- | --- | --- |
| `gw:nonce:enroll:{challengeId}` | string | 짧음(분) | enrollment nonce challenge(§7.2.6) | 1회용·재사용 거부 |
| `gw:idemp:{scope}:{key}` | string | 시간~일 | idempotency(업로드 commit·요청 멱등, §4.5) | 저장 결과 ref/상태 |
| `gw:wh:dedup:{provider}:{eventId}` | string | 시간~일 | webhook eventId 중복 처리 방지(§7.6.4) | 인스턴스 공유 필수 |
| `gw:rl:{subject}:{window}` | counter(string/INCR) | window 길이 | rate-limit 카운터(§7.1.1) | 윈도우 만료 시 자동 소멸 |
| `gw:lock:{resource}` | string(SET NX) | 짧음(초) | 분산 락(선택 — 단발 작업 직렬화) | 필요 시만 |

## 매핑

- 캐시 키 ↔ PostgreSQL 테이블은 위 "재구성 출처" 열이 SSOT 링크. DBML 변경 시 본 카탈로그 동기화.
- 본 카탈로그는 SRS §3.1.2·§6.4·§2.1.1에서 참조한다.
