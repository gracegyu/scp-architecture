# AXS vs CleverSpace 연동 차이 (참조 정리)

> **성격**: GW가 연동하는 두 target(AXS·CleverSpace)의 인증·org 식별·파일 경로·webhook 차이를 한눈에 보는 **참조 문서**. **정본은 GW SRS**(§2.3·§4.1·§7.1.5·§7.5·§7.6)·④ AXS Sub-SRS·② CleverSpace OnePager. 값이 어긋나면 SRS가 우선.
> **작성**: 2026-09-01 · connector_type 개명(`oauth2_org_header`)·CleverSpace 연동 v1.1 정리 반영.

---

## 0. 한눈에 요약

| 축 | **AXS** | **CleverSpace** |
| --- | --- | --- |
| 연동 시점 | **v1.0 실연동**(유일) | **v1.1 예정**(v1.0은 미실연동) |
| trust profile | **external (C)** — 외부 파트너 | **internal (B)** — 사내 신뢰망 *(단 ③b 신원 전달 미정·아래 §7)* |
| connector_type | **`oauth2_org_header`** | **`oauth2_jwt_assertion`** (v1.1·카탈로그엔 `availability:planned`) |
| 아웃바운드 인증 | OAuth2 client_credentials(tenant 단일 토큰) | **미정(P0)** — 권장: GW 서명 JWT 어서션 / 차선: device 토큰 verbatim |
| 테넌트(org) 식별 | `Organization-ID` **헤더**(clinic→org_mapping) | **토큰 클레임**(device_id→테넌트·clinic 개념 없음) |
| 업로드 바이트 | **GW 토큰 위임**(사이드카) | **presigned**(CleverSpace 자체 발급) |
| 다운로드 바이트 | **presigned**(Blob SAS) | presigned |
| egress 고정 IP | **필요**(allowlist·fail-closed) | 불필요(내부망) |
| **Webhook(인바운드)** | **보냄** — GW가 수신·분배(v1.0 유일) | **안 보냄** — 수신 대상 아님·완료처리는 CleverSpace 내부(GW 무관) |

---

## 1. 연동 시점·범위

| | AXS | CleverSpace |
| --- | --- | --- |
| 실연동 | **v1.0**(AXS 연동 전체: 업로드·다운로드·webhook·org 링크) | **v1.1**(추후 CleverSpace 연동 요구 시) |
| v1.0에서의 상태 | 실 sandbox 연동·데모 완료 | GW가 **presigned 중계 capability**만 구조적으로 지원(실 target 미등록) |
| 근거(SRS) | §2.7·§7.5.2·④ Sub-SRS | §2.6·§2.7·§7.1.5(소비자 v1.1) |

---

## 2. 아웃바운드 인증 (③ GW → target)

| | AXS (③a) | CleverSpace (③b) |
| --- | --- | --- |
| 방식 | OAuth2 **client_credentials** | **미정(P0)** — 아래 2안 |
| 토큰 성격 | **tenant 단일**(target 고정 client_id/secret/scope·전 clinic 공유) | (권장안) GW가 서명한 upstream JWT 어서션 |
| GW의 역할 | `credential`로 커넥터 토큰 취득 후 `Authorization: Bearer` 주입 | (권장) `aud=cleverspace`·claim `device_id`+`clinic_id` JWT 서명·주입 / (차선) ②의 device 토큰 verbatim 전달 |
| 검증 주체 | AXS가 자기 OAuth로 검증 | CleverSpace **GW Guard**가 **GW JWKS**로 검증(§7.1.5) |
| 왜 다른가 | 표준 OAuth2 파트너 | CleverSpace는 **모든 API가 JWT 필수**(테넌트 스코프가 토큰 클레임에서 나옴)·`Vatech-Clinic-Id` 헤더만으론 테넌트 확정 불가 |
| 미결(P0) | — | **③b 신뢰 앵커 결정**(GW 서명 어서션 vs device verbatim)·review-log-12239 C-02·백로그 **B-20** |

> ⚠ **이름 주의**: `oauth2_org_header`의 "org"는 **자격/토큰 스코프가 아니라 요청 헤더**를 가리킨다. AXS 인증 토큰은 org별이 **아니다**(tenant 단일). ("org_scoped"가 오독을 불러 `oauth2_org_header`로 개명·2026-09-01.)

---

## 3. 테넌트(조직) 식별

| | AXS | CleverSpace |
| --- | --- | --- |
| 식별 수단 | **`Organization-ID` 헤더**(업무 API마다 주입) | **토큰 클레임**(서명에 묶인 `device_id`) |
| 매핑 | `clinic → org_mapping` 정조회 **1:1 필수**(0→403·N→409·fail-closed) | CleverSpace에 **clinic 개념 자체가 없음**·device 기준 신원 해석 |
| GW가 하는 일 | clinic으로 org 해석 후 헤더 주입 | (권장) 서명 어서션에 `device_id`(+`clinic_id`) 실어 전달 |
| 근거 | §7.5.1·§7.3 org_mapping | review-log-12239 C-02·§7.1.5 |

---

## 4. 파일 경로 (업로드 / 다운로드)

| | AXS | CleverSpace |
| --- | --- | --- |
| 업로드 | **GW 토큰 위임** — AXS는 presigned 미발급·create-document 응답의 `storageUrl` 감지 시 **위임 토큰 사이드카** 부착 → EzServer가 직접 POST | **presigned** — CleverSpace가 **스스로 발급**(경로②)·GW는 **발급 요청 중계만** |
| 다운로드 | **presigned**(AXS `storageDownloadUri`·Blob SAS·self-auth) | presigned(CleverSpace 발급) |
| 공통 | **바이트는 GW 미경유**(EzServer ↔ target storage 직접)·GW는 제어 경로만 | 동일 |
| 완료처리 | (AXS 이벤트=webhook·아래 §6) | **CleverSpace 책임**(명시 commit API + RabbitMQ + 보정 스케줄러·ObjectCreated는 "신설 검토"·GW 무관) |
| 근거 | §2.3.4·§7.5.2 | §2.3.5·§4.1.4·② OnePager |

---

## 5. egress (나가는 트래픽 통제)

| | AXS | CleverSpace |
| --- | --- | --- |
| 고정 egress IP allowlist | **필요**(외부 C)·`egress_allowlist` **fail-closed 집행**(비면 아무 데도 못 나감) | **불필요**(내부망 B) |
| 근거 | §2.1.1·§7.5.1 | §4.1.2 |

---

## 6. Webhook (인바운드 이벤트: target → GW)

| | AXS | CleverSpace |
| --- | --- | --- |
| GW로 이벤트 발신 | **보냄**(v1.0 유일 발신 target) | **안 보냄** |
| 수신 대상 여부 | 해당(GW가 수신·분배) | **수신 대상 아님**(§2.3.6·§7.6·② OnePager `_status`) |
| 수신 호스트 | `axs.webhook.<region>.gw.<도메인>`(Host/SNI로 발신자 식별) | — |
| 인증·멱등 | **HMAC + timestamp** 검증·`Signature` 헤더·hex·`eventId`(messageId) 멱등(HMAC-SHA512·④) | — |
| 이벤트 예 | `patient.file.uploaded` / `updated` → EzServer로 MQTT 하행 | — |
| 완료 콜백 오해 주의 | — | CleverSpace 완료처리에 "콜백"이 있으나 **CleverSpace 내부/클라이언트용**이며 **GW로 향하지 않음**(GW는 발급 중계만·§903) |
| 근거 | §2.3.6·§7.6·④ Sub-SRS | §2.3.6·§7.6.5·review-log-12239 |

---

## 7. connector_type / profile 정리

| connector_type | profile | 인증 | org 구분 | egress | 예시 | 상태 |
| --- | --- | --- | --- | --- | --- | --- |
| `oauth2_org_header` | external(C) | OAuth2 client_credentials(tenant 단일) | `Organization-ID` 헤더·org_mapping 1:1 | fail-closed 집행 | **AXS** | v1.0 |
| `oauth2_jwt_assertion` | (내부 B 신뢰) | GW 서명 upstream JWT 어서션(권장안) | 토큰 클레임(device_id) | 내부망 | **CleverSpace** | **v1.1 planned** |
| `internal_bypass` | internal(B) | 없음(verbatim·주입 없음) | 없음 | 미집행(내부) | *(v1.0 확정 사용처 없음)* | v1.0 |

> **CleverSpace ≠ `internal_bypass`**: CleverSpace는 JWT 인증이 필수라 "인증 없이 그대로 전달"하는 `internal_bypass`와 맞지 않는다. ③b 결정이 **차선(device verbatim)** 이면 `internal_bypass`가 될 수 있으나, **권장안(GW 서명 어서션)** 이면 `oauth2_jwt_assertion`이다. 결정 전까지 CleverSpace 타입은 **planned로만** 둔다.

---

## 8. 미결·주의 (열린 항목)

| 항목 | 내용 | 추적 |
| --- | --- | --- |
| ③b 신원 전달 방식 | GW 서명 어서션(권장) vs device 토큰 verbatim(차선) — CleverSpace 타입 확정 종속 | **B-20**·review-log-12239 C-02 |
| CleverSpace 실연동 | v1.1(추후 요구 시)·target 등록·GW Guard(§7.1.5)·Console 폼 활성 | **B-20** |
| capability-off verbatim | 외부(C) target credential 미설정 시 verbatim no-op의 스펙 근거 대조 | 백로그 후보 |
| 새 external target 범용성 | AXS·CleverSpace 외 추가 시 override·org-less·추가 프로파일 | **B-19** |

> **핵심 원칙(범용 불변식)**: 위 차이는 **모두 `connector_type` → 프로파일**로 표현되며, 런타임 소스에 `if targetId==='axs'` 류 **특정 target 하드코딩은 금지**(§7.5.1 NORMATIVE). 단 "신규 target = 코드 0"은 관례가 기존 프로파일과 일치할 때만 성립하고, 초기 target은 인증·org 식별이 달라 **새 프로파일/전략 추가가 불가피**하다(성숙기 목표·§7.5.1 제약).
