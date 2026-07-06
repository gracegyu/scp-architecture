# ③-C Sub-SRS — GW Console (4단계, ③ 하위)

- 상태: 미작성 (③ SRS baseline 후)
- 문서 유형: Sub-SRS
- 범위: Admin 역할·권한·OneID 연계, 매핑/클리닉/상태/온보딩 화면·플로우 (관리 API는 ③ SRS/Swagger)
- 레포(추천): vt-api-gateway-console (미생성)
- 공식 등록처: console repo 생성 시 그 repo, 미생성 시 vt-api-gateway `docs/`

---

## 작성 가이드 — provider(예: AXS) 연동 등록 (③ SRS/DBML/OpenAPI 근거)

> Console Sub-SRS 작성 시 참고. **정본 = ③ GW SRS §7.6·§7.5·§7.1.3·DBML·admin OpenAPI**. 아래는 "AXS 같은 provider 하나를 붙일 때 무엇을 어디에 등록하고 Console이 어떤 화면으로 하는가"의 요약.

### 1) provider 하나 등록 시 생성되는 DB 레코드 (여러 테이블에 걸침)

**A. 연동 코어 3행 (provider당 1행씩)** — 이게 "provider를 붙인다"의 본체:

| 테이블 | 역할(왜 필요) | AXS 예시 값 | admin API |
| --- | --- | --- | --- |
| `upstream_registry` | **라우팅** — `axs.gw.vatech.com` → 실제 host·profile·timeout | target_id=`axs`, host=`api.eu.axs.straumann.com`, profile=`external`, connect/response/total=`3000/10000/12000` | `POST /admin/v1/upstreams` |
| `connector` | **외부 호출 자격·egress**(외부 C만) | name=`axs`, credentialRef=`kms://alias/axs-oauth-client`, egressAllowlist=`{hosts:[api.eu.axs…],ports:[443],requireStaticEgressIp:true}` | `POST /admin/v1/connectors` |
| `webhook_provider` | **이벤트 수신 config**(그 provider가 우리에게 push) | provider=`axs`, inbound_host=`axs.webhook.gw.vatech.com`, sig_scheme=`hmac-sha512`, secret_ref=`kms://alias/axs-webhook-hmac`, event_id_path=`$.messageId`, org_id_path=`$.organizationId`, event_type_path=`$.eventType` | `POST /admin/v1/webhook-providers` |

**B. 정책 1행 이상** — 이 connector로 무엇을 호출 허용할지(없으면 deny-by-default):

| 테이블 | 역할 | 예시 | admin API |
| --- | --- | --- | --- |
| `policy` | 허용 endpoint·scope(scope=global/clinic/device) | scope_type=`global`, connector=`axs`, allowed_endpoints=`[{methods:[GET],pathPattern:/v1/patients/**}]`, scopes=`[axs:patient.read]` | **정책 관리 API 미정의(Appendix B #32)** — 정의 후 |

**C. 클리닉별 N행** — 그 provider 연동을 쓰는 **각 클리닉마다**(provider 등록과 별개·클리닉 온보딩 흐름):

| 테이블 | 역할 | 예시 | 생성 경로 |
| --- | --- | --- | --- |
| `org_mapping` | (provider,org_id)→clinic **분배 역조회 키** | provider=`axs`, external_org_id=`0040694997`, clinic_id=`CLINIC-0040694997` | 자가 등록(§2.3.5) + `POST /admin/v1/org-mappings`(교정) |
| `delivery_channel` | 그 클리닉에 이벤트 전달 방식 | clinic_id=`CLINIC-…`, channel_type=`mqtt_edge`, endpoint=`gw/clinic/CLINIC-…/webhook` | 클리닉 enroll 시 생성(§7.6.5/6) |

→ **정리**: "AXS를 등록" = **코어 3행(upstream+connector+webhook_provider) + policy** 를 Console에서 등록하고, org_mapping/delivery_channel은 **클리닉이 붙을 때** 채워진다.

### 2) Console UI 가이드 (화면·플로우)

- **[연동(Provider) 추가] 마법사** — 한 흐름에서 3섹션 입력 → 저장 시 코어 3 POST를 순차 호출:
  1. **라우팅**(upstream): target_id·host·profile(internal/external)·timeout
  2. **외부 자격**(connector, profile=external일 때만): endpoint·credential(→KMS 저장, **원문 미표시·마스킹**)·egress allowlist(hosts/cidrs/ports/고정IP)
  3. **이벤트 수신**(webhook_provider): inbound_host·sig_scheme·secret(→KMS)·`*_path`(event_id/org_id/event_type JSONPath)
- **[연동 목록/상세]**: GET으로 provider 목록·상태(enabled). 상세에서 3섹션 편집(POST upsert)·**삭제**(DELETE 3종).
- **[정책 편집]**: connector별 allowed_endpoints·scopes(Appendix B #32 정책 관리 UI와 통합).
- **[Org 매핑 관리]**: (provider,org_id)→clinic 목록·교정(POST /admin/v1/org-mappings). 1차 입력은 자가 등록.
- **보안·감사**: credential/secret은 KMS 저장·화면 마스킹(원문 미노출), 모든 변경은 감사(action=`connector.update`·`upstream.register`·`webhook_provider.upsert` 등, §7.9.3). 권한=Admin(§7.9.2).

### 3) admin API 호출 순서 (Console 오케스트레이션)

- 등록: `connectors`(자격) → `upstreams`(라우팅) → `webhook-providers`(수신) → (정책) → (클리닉 붙을 때 `org-mappings`).
- 삭제: 역순 `webhook-providers/{provider}` → `upstreams/{targetId}` → `connectors/{name}` DELETE.
- **원자성**: provider 등록은 **3~4 테이블에 걸친 다중 쓰기**라 부분 실패 가능 → 백엔드 **트랜잭션 또는 saga(보상)** 필요. 상세는 LLD. (composite "register-provider" 단일 엔드포인트는 미도입 — 테이블 분리 유지·Console이 순서 오케스트레이션.)
