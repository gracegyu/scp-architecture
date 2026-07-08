# ③-C Sub-SRS — GW Console (4단계, ③ 하위)

> **이 파일의 역할 = 승격용 구조화 씨앗(seed).** ③ SRS 작업 중 이 문서로 갈 내용을 **최종 목차에 대응되게** 미리 정리해 둔다(발견 즉시 캡처·인사이트 유실 방지). 정식 Sub-SRS/문서 집필은 **의존하는 ③ SRS 절이 baseline된 뒤 승격**한다 — 몰아쓰기가 아니라 "옮겨 붙이고 살 붙이기". 승격 트리거: ① ③ 해당 절 동결 + ② 소유권 확정(GW 공통 아님) + ③ 레포/템플릿 존재. 근거: ③이 흔들리는 동안 자식 문서를 미리 쓰면 개명·재번호가 수십 절로 번져 유지면이 폭발한다.

- 상태: 미작성 (③ SRS baseline 후)
- 문서 유형: Sub-SRS
- 범위: Admin 역할·권한·직원 IdP(Entra) 연계, 매핑/클리닉/상태/온보딩 화면·플로우 (관리 API는 ③ SRS/Swagger)
- 레포(추천): vt-api-gateway-console (미생성)
- 공식 등록처: console repo 생성 시 그 repo, 미생성 시 vt-api-gateway `docs/`

> **씨앗 — 호환성 매트릭스는 Console에서 편집하지 않는다(뷰어만).** 매트릭스 저작은 **git 레포 소스 파일 + PR + CI**(§7.7.5·안전 크리티컬·릴리스 결합)이고, **Console은 현재 실효 매트릭스를 well-known(`/.well-known/{env}/server-configuration.json`)에서 읽어 표시하는 읽기 전용 뷰어**(+선택적 스키마 검증·미리보기)만 만든다. **한-행 편집 UI·임의 JSON 업로드 저작면은 만들지 않음**(런타임 가변 저장소 재도입 금지). 긴급 클라이언트 차단은 매트릭스가 아니라 Config push(§7.8.4) UI 소관.

---

## 작성 가이드 — upstream(예: AXS) 연동 등록 (③ SRS/DBML/OpenAPI 근거)

> Console Sub-SRS 작성 시 참고. **정본 = ③ GW SRS §7.6·§7.5·§7.1.3·DBML·admin OpenAPI**. 아래는 "AXS 같은 upstream 하나를 붙일 때 무엇을 어디에 등록하고 Console이 어떤 화면으로 하는가"의 요약.

### 1) upstream 하나 등록 시 생성되는 DB 레코드

**A. `upstream` 1 레코드** — "upstream을 붙인다"의 본체(구 upstream_registry·connector·webhook_provider 병합, 한 행에 라우팅+자격+webhook 수신):

| 테이블 | 담는 것 | AXS 예시 값 | admin API |
| --- | --- | --- | --- |
| `upstream` | **① 라우팅**(모든 대상)+**② 아웃바운드 자격**(외부 C·nullable)+**③ 인바운드 webhook**(발신 대상·nullable) | target_id=`axs`, host=`api.eu.axs.straumann.com`, profile=`external`, connect/response/total=`3000/10000/12000`, credentialRef=`kms://alias/axs-oauth-client`, egressAllowlist=`{hosts:[api.eu.axs…],ports:[443],requireStaticEgressIp:true}`, inboundHost=`axs.webhook.gw.vatech.com`, sigScheme=`hmac-sha512`, secretRef=`kms://alias/axs-webhook-hmac`, eventIdPath=`$.messageId`, orgIdPath=`$.organizationId`, eventTypePath=`$.eventType` | `POST /admin/v1/upstreams` |

- **내부 backend**(cleverspace)는 ① 라우팅만 채우고 ②③은 비움. **call-only 외부**는 ①②만, **webhook만 받는 upstream**은 ①③(host 없으면 라우팅 생략).

**B. 정책 1행 이상** — 이 upstream으로 무엇을 호출 허용할지(없으면 deny-by-default):

| 테이블 | 역할 | 예시 | admin API |
| --- | --- | --- | --- |
| `policy` | 허용 endpoint·scope(scope=global/clinic/device) | scope_type=`global`, target_id=`axs`, allowed_endpoints=`[{methods:[GET],pathPattern:/v1/patients/**}]`, scopes=`[axs:patient.read]` | **정책 관리 API 미정의(Appendix B #32)** — 정의 후 |

**C. 클리닉별 N행** — 그 upstream 연동을 쓰는 **각 클리닉마다**(upstream 등록과 별개·클리닉 온보딩 흐름):

| 테이블 | 역할 | 예시 | 생성 경로 |
| --- | --- | --- | --- |
| `org_mapping` | (target_id,org_id)→clinic **분배 역조회 키** | target_id=`axs`, external_org_id=`e407b34d-c4b0-4db3-bbcd-cc11770eae7b`(AXS organizationId·UUID), clinic_id=`d3f1a9c07b6e4258af31c9d2e0b4a687`(LMP 32자) | 자가 등록(§2.3.4) + `POST /admin/v1/org-mappings`(교정) |

- **분배 채널 레코드 없음**: 클리닉 분배는 clinic→MQTT 토픽(`gw/clinic/{clinicId}/webhook`·§7.6.6) 규약 도출이라 저장 테이블 없음(구 delivery_channel 삭제).

→ **정리**: "AXS를 등록" = **`upstream` 1 레코드 + policy** 를 Console에서 등록하고, org_mapping은 **클리닉이 붙을 때** 채워진다.

### 2) Console UI 가이드 (화면·플로우)

- **[연동(Upstream) 추가] 화면** — 한 폼(3섹션) 입력 → 저장 시 **`POST /admin/v1/upstreams` 1회**:
  1. **라우팅**(모든 대상): target_id(토큰)·host·profile(internal/external)·timeout
  2. **아웃바운드 자격**(profile=external일 때만): credential(→KMS 저장, **원문 미표시·마스킹**)·egress allowlist(hosts/cidrs/ports/고정IP)
  3. **인바운드 webhook**(이벤트 받는 upstream만): inbound_host·sig_scheme·secret(→KMS)·`*_path`(event_id/org_id/event_type JSONPath)
- **[연동 목록/상세]**: GET으로 upstream 목록·상태(enabled). 상세에서 편집(POST upsert)·**삭제**(`DELETE /admin/v1/upstreams/{targetId}`).
- **[정책 편집]**: upstream별 allowed_endpoints·scopes(Appendix B #32 정책 관리 UI와 통합).
- **[Org 매핑 관리]**: (target_id,org_id)→clinic 목록·교정(POST /admin/v1/org-mappings). 1차 입력은 자가 등록.
- **보안·감사**: credential/secret은 KMS 저장·화면 마스킹(원문 미노출), 모든 변경은 감사(action=`upstream.upsert`·`upstream.delete`, §7.9.3). 권한=Admin(§7.9.2).

### 3) admin API 호출 순서 (Console)

- 등록: **`POST /admin/v1/upstreams`(1회)** → (정책) → (클리닉 붙을 때 `POST /admin/v1/org-mappings`).
- 삭제: `DELETE /admin/v1/upstreams/{targetId}`.
- **원자성**: upstream 등록은 이제 **단일 레코드 upsert**라 원자적(구 3표 다중 쓰기 문제 해소). credential·secret은 KMS 저장 후 참조만 DB에 — KMS 쓰기+DB 쓰기 2단계라 실패 처리(보상)만 LLD.

---

## 작성 가이드 — clinic·device 화면 구성 (2 리소스 유지·통합 안 함)

> 정본 결정 = ③ Appendix B **#47**(clinic·device API 분리 유지·통합 기각). 아래는 "왜 두 화면이고, Console에서 어떻게 정리해 중복감을 없애는가"의 UI 씨앗. **API는 두 리소스 그대로**(`/v1/admin/devices`·`/v1/admin/clinics`), 정리는 **표현 계층에서만**.

### 배경 — 왜 통합 안 하나 (요약)
- device·clinic은 **다른 엔터티**: SoT(clinic=LMP 32자 / device=GW UUIDv7)·생성경로·**lifecycle(device만)**·관계역할(clinic=정책/config scope 앵커·org_mapping 라우팅 키·region 원천)이 상이.
- **현 1:1은 배포 우연**이지 모델 제약 아님(모델=device 주체·clinic 선택적 그룹·**1:N**·clinic-less). 통합하면 clinic-less device·device 0/N개 clinic·두 키스페이스 혼재가 깨짐.
- 겹쳐 보이는 건 "한 물리 박스를 두 곳에서 본다"는 것뿐 — **오퍼레이션은 거의 안 겹침**.

### UI 원칙 (중복감 해소의 핵심)
1. **주 워크스페이스 = Fleet/Device 뷰**(device가 주체). 목록 컬럼: device·**clinic(이름/id)**·region·status. 1:1인 지금 운영자는 주로 여기 머묾.
2. **보조 워크스페이스 = Clinic 뷰**(그룹·라우팅 관점). 목록 컬럼: clinic·**device 수**·region·**AXS org-binding 상태**. 1:N이 오면 여기서 자연 확장.
3. **편집면 단일화(가장 중요)** — 같은 필드를 두 화면에서 고치지 않는다:
   - **region·org-binding·clinic 정보 교정 = Clinic 화면에서만** (`PATCH /admin/clinics/{id}`·`PUT …/region`·org-binding).
   - **device lifecycle·kill·키 = Device 화면에서만** (`PATCH /admin/devices/{id}`·`…/kill`).
4. **양방향 드릴스루**: Device 상세에 **소속 clinic 카드**(region·org-binding·정책 스코프 요약 + "clinic 관리로 이동" 링크) / Clinic 상세에 **소속 device 목록**(1:N).

### 화면 스케치
- **Device 상세** 탭: [상태·lifecycle] · [인증·키] · [소속 clinic 카드(읽기+링크)].
- **Clinic 상세** 탭: [clinic 정보·region] · [org-bindings] · [소속 device 목록] · [clinic-scope 정책·config].

### 관계 일급화 (③ API — 반영 완료 2026-07-08)
- ✅ `Device` 응답에 **`clinic` 요약 임베드**(clinicId·name·region·nullable·읽기전용) → device 화면이 clinic 2차 조회 없이 카드 렌더. clinic-less면 null.
- ✅ **`GET /v1/admin/clinics/{clinicId}/devices`**(clinic의 device 하위목록·1:N) 신설 → Clinic 상세의 "소속 device 목록" 탭이 이 엔드포인트를 사용. (OpenAPI op 42·redocly valid.)
- 콘솔 구현 시: device 카드=임베드 `clinic` 사용(별도 콜 불필요)·clinic 상세 device 탭=nested list 사용.

### device-self 층 유의 (섞지 말 것)
- `/v1/clinics/me/*`(device가 자기 clinic read-back·region·org-binding 자가 등록)는 **디바이스 self 평면**이고 위 operator 화면과 **actor가 다름**. Console(operator)과 EzServer Console(device-self)을 혼동해 한 화면에 합치지 않는다.
