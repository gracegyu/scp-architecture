# ③-C Sub-SRS — GW Console (4단계, ③ 하위)

> **이 파일의 역할 = 승격용 구조화 씨앗(seed).** ③ SRS 작업 중 이 문서로 갈 내용을 **최종 목차에 대응되게** 미리 정리해 둔다(발견 즉시 캡처·인사이트 유실 방지). 정식 Sub-SRS/문서 집필은 **의존하는 ③ SRS 절이 baseline된 뒤 승격**한다 — 몰아쓰기가 아니라 "옮겨 붙이고 살 붙이기". 승격 트리거: ① ③ 해당 절 동결 + ② 소유권 확정(GW 공통 아님) + ③ 레포/템플릿 존재. 근거: ③이 흔들리는 동안 자식 문서를 미리 쓰면 개명·재번호가 수십 절로 번져 유지면이 폭발한다.

- 상태: 미작성 (③ SRS baseline 후)
- 문서 유형: Sub-SRS
- 범위: Admin 역할·권한·OneID 연계, 매핑/클리닉/상태/온보딩 화면·플로우 (관리 API는 ③ SRS/Swagger)
- 레포(추천): vt-api-gateway-console (미생성)
- 공식 등록처: console repo 생성 시 그 repo, 미생성 시 vt-api-gateway `docs/`

---

## 작성 가이드 — upstream(예: AXS) 연동 등록 (③ SRS/DBML/OpenAPI 근거)

> Console Sub-SRS 작성 시 참고. **정본 = ③ GW SRS §7.6·§7.5·§7.1.3·DBML·admin OpenAPI**. 아래는 "AXS 같은 upstream 하나를 붙일 때 무엇을 어디에 등록하고 Console이 어떤 화면으로 하는가"의 요약.

### 1) upstream 하나 등록 시 생성되는 DB 레코드

**A. `upstream` 1 레코드** — "upstream을 붙인다"의 본체(구 upstream_registry·connector·webhook_provider 병합, 한 행에 라우팅+자격+webhook 수신):

| 테이블 | 담는 것 | AXS 예시 값 | admin API |
| --- | --- | --- | --- |
| `upstream` | **① 라우팅**(모든 대상)+**② 아웃바운드 자격**(외부 C·nullable)+**③ 인바운드 webhook**(발신 대상·nullable) | target_id=`axs`, host=`api.eu.axs.straumann.com`, profile=`external`, connect/response/total=`3000/10000/12000`, credentialRef=`kms://alias/axs-oauth-client`, egressAllowlist=`{hosts:[api.eu.axs…],ports:[443],requireStaticEgressIp:true}`, inboundHost=`axs.webhook.gw.vatech.com`, sigScheme=`hmac-sha512`, secretRef=`kms://alias/axs-webhook-hmac`, eventIdPath=`$.messageId`, orgIdPath=`$.organizationId`, eventTypePath=`$.eventType` | `POST /admin/v1/upstreams` |

- **내부 backend**(cleverspace·oneid)는 ① 라우팅만 채우고 ②③은 비움. **call-only 외부**는 ①②만, **webhook만 받는 upstream**은 ①③(host 없으면 라우팅 생략).

**B. 정책 1행 이상** — 이 upstream으로 무엇을 호출 허용할지(없으면 deny-by-default):

| 테이블 | 역할 | 예시 | admin API |
| --- | --- | --- | --- |
| `policy` | 허용 endpoint·scope(scope=global/clinic/device) | scope_type=`global`, target_id=`axs`, allowed_endpoints=`[{methods:[GET],pathPattern:/v1/patients/**}]`, scopes=`[axs:patient.read]` | **정책 관리 API 미정의(Appendix B #32)** — 정의 후 |

**C. 클리닉별 N행** — 그 upstream 연동을 쓰는 **각 클리닉마다**(upstream 등록과 별개·클리닉 온보딩 흐름):

| 테이블 | 역할 | 예시 | 생성 경로 |
| --- | --- | --- | --- |
| `org_mapping` | (target_id,org_id)→clinic **분배 역조회 키** | target_id=`axs`, external_org_id=`0040694997`, clinic_id=`CLINIC-0040694997` | 자가 등록(§2.3.4) + `POST /admin/v1/org-mappings`(교정) |

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
