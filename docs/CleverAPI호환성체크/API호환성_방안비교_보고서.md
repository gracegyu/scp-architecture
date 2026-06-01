# Clever API 호환성 방안 비교 보고서

작성일: 2026-06-01  
과제: VKS 요청 — CleverOne·EzServer·CleverSpace API 호환성 검토 (Thomas)  
근거: VKS(과제 요청·현황·논의사항), 수집 문서(OneID/EzCloud RestApi CSV, CleverSpace v1.3 기능정의서·MMI ErrorCode, EzServer PMS Integration SRS MD), 4개 제품 소스코드, EzServer Releases CSV, PLAN-1191/EZSV-2506 Jira XML

---

## Executive Summary

CleverOne ↔ EzServer ↔ CleverSpace 연동에서 **클라이언트 버전이 전달되지 않고**, CleverSpace **제품 릴리즈 버전 API도 없어** v1.3.0(유상화·신규 API) 대응 시 구버전이 신규 error code를 인식하지 못하는 문제가 반복된다.

**핵심 전제**

- 연동 경로가 **2개**다: `CleverOne → EzServer → CleverSpace`(경로 A), `CleverOne → CleverSpace`(경로 B, Direct).
- **EzServer는 Server이면서 Client**다. CleverOne 입장의 서버이고, CleverSpace·OneID 입장의 클라이언트다.
- 호환성 제어 방안 4가지는 **배타적 선택이 아니다**. 서버가 **제약을 집행**하고, 클라이언트는 **사전에 호환 여부를 알아 UX를 개선**하는 **2~3개 조합**이 현실적이다.
- 클라이언트(CleverOne, EzDent-i 등)는 **여러 개**를 고쳐야 하지만, CleverSpace·EzServer는 **한 곳(또는 소수) 수정으로 전 클라이언트에 효과**를 줄 수 있다.

**권장 조합**

| 구분 | 조합 | 역할 |
|------|------|------|
| **1차 (v1.3.0)** | **방법 2 + 4 + (일부 1)** | CleverSpace **서버 사전 검증**(`validate-limits` 등) + **호환성 매트릭스** + **Client 식별 헤더** + 클라이언트 **error code·fallback** |
| **2차 (장기)** | **방법 3 + 4 + 1** | EzServer **Gateway 집중** + well-known **capability** + ESLinkageCloudPlatform **부분 업데이트** |

단독으로 방법 1(클라이언트만) 또는 2(서버만)를 택하면 **2경로·EzServer 이중 역할·ESLinkageCloudPlatform 공유 라이브러리**를 모두 커버하기 어렵다.

---

## 1. 연동 구조와 검토 범위

### 1.1 두 연동 경로

VKS에서 정리한 두 경로는 **동시에 존재**하며, ESLinkageCloudPlatform이 **기능별로 분기**한다.

```
[경로 A] CleverOne ──HTTP(EPI)──► EzServer(EPI) ──HTTP──► CleverSpace / OneID
              └──MQTT(wss)──► EzServer Messenger ──► (업로드/공유 결과)

[경로 B] CleverOne ──HTTP──► OneID / CleverSpace (Direct, OAuth)
              └── CheckUploadCondition, tenant/member 조회 등
```

| 기능 | 경로 | ESLinkageCloudPlatform 구현 |
|------|------|----------------------------|
| 업로드·공유·이력·파일크기 | **A** (EzServer 경유) | `CEzServerLinker` → EPI `/ezcloud/cases/*` |
| OneID 로그인·OAuth | **B** (Direct) | `COneIdLinker` |
| 업로드 제한 조회, tenant/member 검색 | **B** (Direct) | `CEzCloudLinker` → `GET /organization-data/upload/limit` 등 |
| 업로드/공유 **결과 알림** | **A** (EzServer MQTT) | CleverOne `CMQTTManager` → EzServer messenger |

SRS v6.2(EzServer PMS Integration)는 경로 A의 시퀀스를 정의한다. Imaging App(CleverOne)이 EPI에 업로드/공유를 요청하면, EPI가 presigned URL·organization-data API를 호출하고 **결과를 MQTT로 Imaging App에 전달**한다.

### 1.2 EzServer의 이중 역할

| 관점 | 역할 | 버전·식별 현황 |
|------|------|----------------|
| CleverOne → EzServer | **Server** (EzWebServer + EPI) | CleverOne이 `GetVersion` 후 `CheckServerVersion`(최소 6.3.1). UserAgent에 `"CleverOne"`만, **버전 없음** |
| EzServer → CleverSpace/OneID | **Client** (EPI HTTP) | OAuth client_id 기반. UserAgent·client product version **미전달** |
| EzServer → CleverOne | **Server** (MQTT messenger) | `clever_space_error_codes`를 MQTT payload로 전달 |

**시사점:** CleverSpace에서 min client version을 검증하려면 **경로 B(Direct)는 CleverOne 헤더**를, **경로 A는 EzServer가 대리 전달**해야 한다. EzServer만 고치면 경로 A는 일괄 적용되지만, **경로 B는 CleverOne(ESLinkageCloudPlatform) 수정 없이는 버전을 알 수 없다.**

---

## 2. 현황 분석 (문서·소스 근거)

### 2.1 Client 식별·버전 전달

| 구간 | UserAgent / Header | 버전 체크 | 근거 |
|------|-------------------|-----------|------|
| CleverOne → EzServer | `"CleverOne"` (PRODUCT_NAME) | CleverOne → EzServer **있음** | `CleverOneInitializer.cpp`: `pHttp->Set(..., PRODUCT_NAME, ...)`, `CheckServerVersion(..., REQUIRE_EZWEBSERVER_API_VERSION)` |
| CleverOne → OneID/CleverSpace (Direct) | `"CleverOne"` (`strAgent`) | **없음** | `EzCloudController.cpp` → `CEzCloudServiceHelper(..., "CleverOne")` → `EzCloudLinker`/`OneIdLinker` → `m_pHttp->Set(..., strAgent, ...)` |
| EzServer → CleverSpace | client_id/OAuth | **없음** | EPI HTTP client, SRS v6.2 |
| CleverSpace → Client | `server-configuration.json` `"version":"v1"` | URI API 버전만, **제품 릴리즈 버전 API 없음** | ezcloud repo |

VKS 논의사항(tick): Client는 UserAgent에 **제품명·버전·OS명·OS버전**을 넣도록 전사 표준화 — **현재 미적용**.

### 2.2 기존 호환성 패턴

**CleverOne → EzServer (동작 중인 유일한 버전 게이트)**

- 시작 시 EzServer 버전 조회 → major/minor/micro별 종료·경고.
- EzServer Releases CSV와 유사한 **클라이언트 내장 최소 버전** 방식.

**EzServer → Third-party PMS (참고 모델, EzCloud 미적용)**

- `post_clinics.rs`: PMS `GET /versions`로 EPI 지원 여부 확인.
- **EzCloud(CleverSpace) endpoint에는 동일 패턴 없음.**

**CleverOne 사전 검증 (Direct, 제한적)**

- `CheckUploadCondition()` → `GET /organization-data/upload/limit` (v1.1 RestApi).
- 업로드 **직전** 파일 개수·용량 등 정적 제한만 조회. v1.3 **구독·quota 통합 검증**(`validate-limits`)은 **미연동**.

### 2.3 Error code 처리 gap

#### MMI v1.3 Error code (EzServer → CleverOne MQTT, Desktop)

| 우선순위 | 유형 | Code | CleverOne `MessagingDialog` |
|----------|------|------|----------------------------|
| 4 | 네트워크 | EzServer 동적 code | 별도 분기 없음 |
| 3 | 사용 한도 초과 | 400110~400113 | **처리** |
| 3 | 일일 업로드(남용) | **400116** (v1.3 신규) | **미처리** |
| 2 | 권한 없음 | 404101, 403100, 401101 | **처리** (403100은 v1.1 CSV에 4031xx와 번호 체계 상이 — 구현·문서 정합 확인 필요) |
| 1 | 사용자 오류(zip 등) | 400102 | **처리** |
| 5 | 시스템 | 500xxx | 5xx prefix만 |

#### EzCloud v1.1 RestApi `(errors).csv` vs v1.3

- v1.1: `400101` QUOTA_EXCEEDED (통합).
- v1.3 MMI: quota **세분화** (400110 조직 스토리지, 400111 공유 횟수, 400112 파일 개수, 400113 파일 용량, 400116 일일 업로드).
- EzServer EPI: CleverSpace API error를 `clever_space_error_codes`로 수집해 MQTT 전달 (`upload_manager_context.rs`, `ez_cloud_share_task.rs`). **400101 era와 40011x era 공존 가능.**

#### CleverSpace v1.3 기능정의서와의 대응

P1 요구(스토리지·공유·다운로드·CT 조회 제한)는 MMI error code **400110~400113** 및 PLAN-1191 **`validate-limits`**와 정합. 웹 UI는 CleverSpace에서 처리, Desktop은 **MQTT + 사전 API**로 동일 제약을 전달해야 한다.

### 2.4 v1.3 신규 API (문서·구현 gap)

| API | 출처 | v1.1 CSV | ezcloud repo |
|-----|------|----------|--------------|
| `POST /tenants/subscriptions/validate-limits` | PLAN-1191 | **없음** | **미구현** (검색 결과 없음) |
| `GET /organization-data/upload/limit` | v1.1 | **있음** | 구현됨 (CleverOne Direct 사전 조회에 사용) |
| `GET /tenants/subscriptions/metrics` | v1.1 | **있음** | 홈·플랜 현황용 |

PLAN-1191: EzServer가 MQTT error code 확장·히스토리 에러 표시 담당, CleverSpace가 `validate-limits` 제공 — **호출 주체·시점(EzServer vs CleverOne Direct)은 미확정**.

---

## 3. 호환성 제어 방안 (4가지, 조합 가능)

4가지는 **상호 배타적이 아니다**. 아래 조합이 VKS 과제 요청(서버 제어 + 클라이언트 사전 인지 + 다수 클라이언트 vs 단일 서버 수정)에 부합한다.

### 방법 1: 클라이언트 주도 — capability·호환 범위 **사전 조회**

클라이언트(또는 ESLinkageCloudPlatform)가 CleverSpace/EzServer **지원 기능·min version**을 조회하고, 미달 시 기능 비활성화·업데이트 안내.

| 장점 | 단점 |
|------|------|
| UX 선제 제어(grey-out, 업로드 버튼 비활성). EzServer `CheckServerVersion` 패턴과 일관 | **N개 클라이언트** 배포 필요. 구버전은 서버 없이 우회 가능 |
| Direct 경로에서 **업로드 전** `upload/limit`·`validate-limits` 호출 가능 | capability API **신규** 필요(현재 없음) |

**단독 적용:** 불충분. **방법 2·4와 병행** 시 “미리 알려주는” UX 레이어로 적합.

### 방법 2: 서버 주도 — 요청 시 검증·거부·구조화 응답

CleverSpace(및 EzServer EPI)가 Client 식별 헤더를 파싱하거나, **사전 검증 API**로 quota·min version을 집행.

| 장점 | 단점 |
|------|------|
| **한 곳(CleverSpace) 수정으로 모든 클라이언트에 효과** (Direct 수신 시) | 경로 A는 EzServer가 **헤더 대리 전달** 필요 |
| `validate-limits`로 v1.3 유상화 **업로드/공유 직전** 차단 | 헤더 표준화 선행 |
| PLAN-1191 “웹·앱 버전 확인 후 업데이트 안내”와 부합 | |

**단독 적용:** UX는 거칠 수 있음(갑작스런 403). **방법 1·4와 병행** 권장.

### 방법 3: EzServer Gateway — Policy Enforcement Point

CleverOne Direct를 점진 폐기하고 CleverSpace API를 **EzServer EPI가 대리**. 버전·quota·error code 변환을 EPI 한곳에 집중.

| 장점 | 단점 |
|------|------|
| 검증·로깅·호환 **단일 지점**. PMS `/versions` 패턴 재사용 | **아키텍처 변경**. Direct 경로(OneID OAuth, member search) 이전 비용 |
| EzServer가 CleverSpace **대표 Client** → 헤더·버전 일원화 | 단기 v1.3 일정에 과함 |

**단독 적용:** 2차 목표. 1차에서는 EPI에 **validate-limits 호출·error 전달 강화**만 선적용.

### 방법 4: 계약·호환성 매트릭스 — 릴리즈 프로세스

EzServer Releases CSV와 유사한 **CleverSpace 호환성 테이블** + error code registry + unknown code **fallback** 규칙.

| 장점 | 단점 |
|------|------|
| QA·릴리즈 노트·버전 조합 **명시적 관리** | 매트릭스 **운영 부담** (자동화 없으면 drift) |
| 런타임(2) + 프로세스 이중 안전 | 런타임만으로는 구버전 차단 불가 |

**단독 적용:** 불충분. **방법 2의 설계 입력** + **방법 1의 클라이언트 내장표**로 사용.

### 3.1 방안 조합 비교

| 조합 | 서버 1곳 수정 효과 | 클라이언트 UX | 2경로 커버 | v1.3 적합도 |
|------|-------------------|---------------|-----------|-------------|
| **2 + 4** (1차 core) | **높음** | 중간 | A: EzServer/EPI, B: CleverSpace Direct | **최우선** |
| **2 + 4 + 1** (1차 권장) | 높음 | **높음** | A+B | **권장** |
| **2 + 1** (헤더 없이) | 높음 | 중간 | B만 Direct 검증 | 차선 |
| **3 + 4 + 1** (2차) | **최고** | 높음 | Direct 축소 후 단순 | 장기 |
| 1만 | 낮음 | 높음(신규만) | 구버전 우회 | 부족 |
| 2만 | 높음 | 낮음 | B는 헤더 필요 | 부분 |

---

## 4. 경로별 1차 대응 설계

### 4.1 경로 A: CleverOne → EzServer → CleverSpace

```
CleverOne                    EzServer (EPI)                 CleverSpace
   │  POST /ezcloud/cases/upload (버전 헤더 추가)              │
   │ ─────────────────────────► │  validate-limits (신규)     │
   │                            │ ───────────────────────────►│
   │                            │  upload/share API           │
   │  MQTT (clever_space_error_codes)                         │
   │ ◄───────────────────────── │                             │
   │  MessagingDialog 표시       │                             │
```

| 항목 | 담당 | 내용 |
|------|------|------|
| Client 식별 | CleverOne → EPI | `X-Ewoosoft-Client` 또는 User-Agent 확장 (제품/버전/OS) |
| 헤더 전달 | EPI → CleverSpace | EPI HTTP client가 CleverOne 식별 정보 **대리 전달** (또는 EPI 자체 버전 + originating client) |
| 사전 검증 | EPI | 업로드/공유 **직전** `validate-limits` (PLAN-1191) |
| Error 전달 | EPI → CleverOne MQTT | MMI code(400110~116 등)를 `clever_space_error_codes`에 포함 — **이미 구조 존재**, code 목록·매핑 갱신 |
| Error 표시 | CleverOne | `MessagingDialog` switch 확장(400116), unknown → “업데이트 필요” fallback |

EzServer 수정 **1곳(EPI)** 으로 경로 A를 타는 **모든 Imaging App**(CleverOne, EzDent-i 등 EPI 사용 제품)에 사전 검증·error 전달을 통일할 수 있다.

### 4.2 경로 B: CleverOne → CleverSpace (Direct)

```
CleverOne (ESLinkageCloudPlatform)
   │  OneID OAuth, GET /organization-data/upload/limit  (기존)
   │  POST /tenants/subscriptions/validate-limits       (v1.3 신규)
   │  GET tenant/member (공유 UI)
   ▼
CleverSpace / OneID
```

| 항목 | 담당 | 내용 |
|------|------|------|
| Client 식별 | ESLinkageCloudPlatform | `EzCloudLinker`/`OneIdLinker`의 `strAgent`를 **버전 포함** 문자열로 확장 |
| 사전 검증 | ESLinkageCloudPlatform | `CheckUploadCondition`에 `validate-limits` **병행** (upload/limit만으로는 v1.3 quota 부족) |
| 서버 거부 | CleverSpace | min client version middleware (방법 2) — **Direct만으로는 여기서 차단 가능** |
| Error | HTTP 응답 | Direct API 호출 실패 시 CleverOne UI 처리 (MQTT 아님) |

경로 B는 **CleverSpace + ESLinkageCloudPlatform** 수정이 필요하다. 서버만 고쳐서는 CleverOne이 보내는 헤더 없이는 버전을 알 수 없다.

### 4.3 EzServer 이중 역할 정리

| EzServer 동작 | 1차 조치 |
|---------------|----------|
| CleverOne의 Server | (선택) EPI min version API 제공 — CleverOne `CheckServerVersion` 확장 |
| CleverSpace의 Client | validate-limits 호출, CleverOne origin header 전달, error code MQTT relay |
| CleverOne의 MQTT Server | payload 스펙 유지, error code 필드 문서화 |

---

## 5. 1차 vs 2차 로드맵

### 5.1 1차 — 최소 수정 (v1.3.0: EzServer v6.5.0, CleverOne v1.5.5, PLAN-1191)

**목표:** silent failure 제거, 한도 초과·권한 오류의 **일관된 메시지**, unknown code **fallback**.

**권장 조합: 방법 2 + 4 + 1**

| 순서 | 작업 | 경로 | 주체 |
|------|------|------|------|
| A | Client 식별 헤더 스펙 합의 | A+B | 전사(VKS 논의 tick) |
| B | CleverSpace `validate-limits` 구현 | A+B | CleverSpace |
| C | EPI: upload/share 전 validate-limits | **A** | EzServer |
| D | ESLinkageCloudPlatform: Direct validate-limits + 헤더 | **B** | ESLinkageCloudPlatform |
| E | Error code 매핑 (400116, 400101 legacy, fallback) | A primarily | CleverOne, EPI |
| F | CleverSpace 호환성 매트릭스 v0.1 | 문서 | PM/아키텍처 |
| G | unknown error → 업데이트 안내 UX | A+B | CleverOne |

### 5.2 2차 — 구조 개선

**목표:** VKS 회의록 “연동 기능은 자동 업데이트/호환” + Tom idea(모듈 단위 업데이트).

**권장 조합: 방법 3 + 4 + 1**

| 순서 | 작업 |
|------|------|
| 1 | `/.well-known/server-configuration.json`에 `release`, `min-client-versions`, `features` |
| 2 | EzServer Gateway — Direct API **점진 EPI 흡수** |
| 3 | ESLinkageCloudPlatform **부분 업데이트** 채널 |
| 4 | 호환성 매트릭스 CI gate (EzServer Releases CSV 수준) |

```
[1차]  헤더 표준 ─┬─ validate-limits (CleverSpace)
                 ├─ EPI 연동 (경로 A)
                 ├─ ESLinkageCloudPlatform (경로 B)
                 └─ error map + 호환표 + fallback
                        ↓
[2차]  well-known capability → Gateway → 모듈 단위 업데이트
```

---

## 6. 권장안 요약

1. **4방안 중 1개 선택이 아니라 2+4+1 조합**이 VKS·PLAN-1191·2경로 구조에 가장 맞다.
2. **서버(CleverSpace)가 제약의 source of truth** — `validate-limits`, min version, error code 발급. **클라이언트는 사전 조회(1)로 UX**를 부드럽게 한다.
3. **EzServer는 1차에서 “CleverSpace 앞단 게이트”** 역할을 강화하면 경로 A 다수 클라이언트를 **한 번에** 올릴 수 있다. **경로 B는 ESLinkageCloudPlatform 필수 수정.**
4. v1.3 **400116** 등 MMI code는 CleverOne switch **하드코딩 확장(단기)** + error registry **(중기)**.
5. EzServer PMS `/versions` 패턴을 CleverSpace **compatibility endpoint** 또는 well-known 확장으로 **대칭 구현** 검토(2차).

---

## 7. 다음 액션

| 우선순위 | Action | 담당 후보 |
|----------|--------|-----------|
| P0 | Client 식별 헤더 스펙 1p (User-Agent vs `X-Ewoosoft-Client`, 경로 A/B/EPI 전달 규칙) | Thomas / Raymond |
| P0 | MMI error code ↔ CleverOne/EPI 매핑표 (400116 포함) | Thomas + CleverSpace |
| P1 | `validate-limits` **호출 주체·시점** 확정 (EPI only vs Direct also) | Jay / CleverSpace |
| P1 | CleverSpace 호환성 매트릭스 v0.1 (EzServer Releases CSV 컬럼 참고) | Raymond |
| P1 | ESLinkageCloudPlatform `CheckUploadCondition` → validate-limits | ESLinkageCloudPlatform |
| P2 | well-known capability / Gateway 로드맵 | 아키텍처 |

---

## 부록 A: 분석에 사용한 문서

| 문서 | 용도 |
|------|------|
| VKS | VKS 과제 요청·이슈·2경로·논의사항·개선방안 검토 범위 |
| PLAN-1191.xml, EZSV-2506.xml | v1.3 scope, validate-limits, 타겟 버전 |
| Confidential_OneID_v1 (*.csv) | OAuth, tenant — client version API **없음** 확인 |
| Confidential_EzCloud_v1.1_RestApi (*.csv) | API·error v1.1 baseline, upload/limit |
| Confidential_CleverSpace_v1.3.0_MMI_Kor_rev2_ErrorCode.png | Desktop MQTT error code |
| Confidential_20260105_CleverSpace v1.3_기능 요구 사항 정의서 (*.csv) | P1 한도 제한 요구 |
| Confidential_EzServer_PMS_Integration_v6.2_SRS.md | EPI upload/share 시퀀스, API 목록 |
| EzServer Releases CSV | 호환성 매트릭스 참고 모델 |

## 부록 B: 참고 코드 위치

| 내용 | 경로 |
|------|------|
| CleverOne EzServer 버전 체크 | `cleveronegroup/cleverone/src/Main/CleverOneInitializer.cpp` |
| CleverOne CleverSpace 연동·MQTT | `cleveronegroup/cleverone/src/Common/EzCloud/EzCloudController.cpp` |
| CleverOne MQTT error switch | `cleveronegroup/cleverone/src/Common/EzCloud/MessagingDialog.cpp` |
| 경로 A/B 분기 (upload vs limit) | `common/ESLinkageCloudPlatform/EzCloudService/src/EzCloudServiceHelper.cpp` |
| UserAgent (`strAgent`) | `common/ESLinkageCloudPlatform/.../EzCloudLinker.cpp`, `OneIdLinker.cpp` |
| EPI EzServer API 래퍼 | `common/ESLinkageCloudPlatform/.../EzServerLinker.cpp` |
| EPI CleverSpace error → MQTT | `ezserver_pms_integration/src/upload_manager/upload_manager_context.rs` |
| EzServer PMS version check | `ezserver_pms_integration/src/epi_api_server/handler/post_clinics.rs` |
| CleverSpace error enums | `ezcloud/packages/apis/api-types/src/errors/*.ts` |
