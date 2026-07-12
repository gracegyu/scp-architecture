# GW API 표면 · Console CRUD 매트릭스 (설계 추적)

> **상태: 재구성 반영 완료(2026-07-08)** — operator=`/v1/admin/*`·device-self=`/v1/*`(+`/me`)·`/v1/region/resolve` 제거·clinic GET/list 신설·`Clinic` 스키마 추가. **clinic↔device 관계 일급화**(nested `GET /v1/admin/clinics/{clinicId}/devices` + `Device.clinic` 요약 임베드·#47). OpenAPI redocly valid(**55 ops**·7/9~10 policy·regions·client-inventory 리뷰 신설분 반영). **7/9 R2 A**: 운영자 인가=GW 자체(operator·operator_role·RBAC 관리 API 7종 신설).
>
> **목적**: GW API를 **청중 면(plane)** 과 **엔티티별 CRUD+list**로 정리해, **GW Console(operator UI) 구현**·**device 연동**에 필요한 API 조합을 한눈에 추적한다. 계약 정본은 `design/openapi/vt-api-gateway.openapi.yaml`이고 본 문서는 그 **조감·추적**.
> `dbml`·`redis`·`db-jsonb-fields`와 나란한 설계 산출물.

## 청중 면(plane) — 2면 + 공개 (namespace=auth 일치)

| plane | 경로 prefix | 인증 | 호출자 |
| --- | --- | --- | --- |
| **device-self** | `/v1/*` (자기 것은 `/me`) | `deviceAuth`(private_key_jwt) | EzServer(+ 클리닉 로컬 Console) |
| **operator** | `/v1/admin/*` | `operatorAuth`(Entra OIDC)+RBAC | GW Console(Admin·C/S) |
| **public** | `/v1/auth`·`/v1/enroll`·`/v1/webhooks`·`/.well-known` | `security:[]` / webhookHmac | 부트스트랩·외부 발신자 |

> 원칙: **device는 자기 것만**(`/me`·id 없음·격리 자명), **operator는 아무 것이나**(id + **list·pagination**). 같은 엔티티라도 두 면은 별도 엔드포인트. 네임스페이스=버전 우선(`/v1/admin/*`, #4b 확정).

## 상태 범례
✅ 구현됨(OpenAPI 반영) · 🟡 재구성 필요 · ✗ 갭(신설 필요) · — 해당 없음

## 엔티티별 CRUD+list

| 엔티티 | operator list | op read | op create | op update | op delete | device-self | 상태·비고 |
| --- | :---: | :---: | :---: | :---: | :---: | --- | --- |
| **device** | ✅ | ✅ | ✅(예외·주=enroll) | ✅(lifecycle·kill) | ✗(=revoke) | heartbeat·token·enroll·config(gw1.1) | ✅ `/v1/admin/devices` · **clinic별 nested list `/v1/admin/clinics/{clinicId}/devices`(1:N·#47)** · 응답에 `clinic` 요약 임베드 |
| **clinic** | ✅ | ✅ | ✅ | ✅ | ✗(canonical·비삭제) | `GET/PATCH /v1/clinics/me` · `PUT /v1/clinics/me/region` · `POST /v1/clinics/me/org-bindings` | ✅ op `/v1/admin/clinics`(list/read/create/update)·device-self `/me` 분리 완료 · **하위 device 목록=`/{clinicId}/devices`** |
| **target** | ✅ | ✅ by-id | ✅ upsert | ✅ upsert | ✅(참조 시 409) | — | ✅ `/v1/admin/targets`(목록·무페이지네이션=소규모 카탈로그) + `/{targetId}`(단건·DELETE)·upsert 200/201 |
| **policy** | ✅ | (list) | ✅ upsert | ✅ upsert | ✅ | — | ✅ `/v1/admin/policies`(목록 필터 scope/target·**limit/cursor**) + `/{id}`(DELETE)·**upsert 200/201(결과 Policy 반환·id=GW surrogate)**·read=list-only(by-id 조회 없음·의도) |
| **org_mapping** | ✅ | (list) | ✅(교정) | ✅ | ✅ | `POST /v1/clinics/me/org-bindings`(자가 등록) | ✅ 자가등록=`/v1/clinics/me/org-bindings`·교정=`/v1/admin/org-mappings` |
| **region_catalog** | ✅ `GET /v1/admin/regions` | (list) | ✅(409 중복) | ✅ PUT/{id} | ✅(참조·default 시 409·gw1.2) | **`GET /v1/regions`**(deviceAuth·선택지) | ✅ 관리=`/v1/admin/regions`(**operator GET list 신설**+POST/PUT/DELETE) · device read=`/v1/regions`(별개 면) |
| **config** | ✅ | ✅ | ✅ put | ✅ | ✅ | `GET /v1/fleet/config`(gw1.1) | ✅ `/v1/admin/config` |
| **webhook_event** | ✅ search | ✅ by-id(메타) | — | — | — | — | ✅ read-only(검색 `/webhook-events` + 단건 `/{eventId}` **메타** + 본문 `/{eventId}/payload` **break-glass·GW중개·redact**·GW가 `payload_encrypted` 복호화→masking, Console 직접 DB/KMS 접근 금지, 7/9 R7) |
| **fleet_state** | ✅ | — | — | — | — | `POST /v1/fleet/heartbeat`(device push) | ✅ read-only(`/v1/admin/fleet`·heartbeat·버전·OS·online) |
| **client_inventory** | ✅ 횡단 `/v1/admin/clients` + by-clinic | — | — | — | — | (관측·Vatech-* 헤더) | ✅ read-only(**전 클리닉 `/v1/admin/clients`**(캠페인) + 드릴다운 `/v1/admin/clinics/{clinicId}/clients`·앞단 SW 버전·OS presence·§7.8.5·식별id 없음=튜플·대수 아님) |
| **audit_log** | ✅ search | — | — | — | — | — | ✅ append-only(`/v1/admin/audit`) |
| **operator** | ✅ | ✅ by-id | (JIT·SSO 자동) | ✅ status(정지/복구) | ✗(=suspended) | `GET /v1/admin/me`·`POST …/me/access-requests`(본인 권한 요청) | ✅ RBAC(7/9 R2 A·authN=Entra SSO/authz=GW): `/v1/admin/operators`·`/{id}`·상태 PATCH |
| **operator_role** | ✅(승인 큐 `/access-requests`) | — | ✅ Admin 부여 `POST …/{id}/roles` | ✅ 승인/거부/회수 `PATCH …/roles/{grantId}` | ✗(=revoked) | 요청 `POST …/me/access-requests` | ✅ 역할=앱상수·스코프(CS=global)·요청→승인 lifecycle |

## 재구성 완료 내역 (2026-07-08)

1. **clinic — device-self(`/me`) + operator(id+list) 분리** (최대 작업, 완료):
   - device: `GET /v1/clinics/me`(내 clinic·region read-back) · `PATCH /v1/clinics/me`(LMP info 동기화) · `PUT /v1/clinics/me/region`(자가 region·#4a) · `POST /v1/clinics/me/org-bindings`(자가등록)
   - operator: `GET /v1/admin/clinics`(**list+pagination**) · `GET /v1/admin/clinics/{clinicId}` · `POST /v1/admin/clinics`(생성/교정) · `PATCH /v1/admin/clinics/{clinicId}` · `PUT /v1/admin/clinics/{clinicId}/region`
   - 기존 dual-auth `PATCH /v1/clinics/{clinicId}` 폐기(위로 분해 완료)
2. **operator device를 `/v1/admin/devices`로 이동**(list/read/create/update). kill 포함 전부 `/v1/admin`.
3. **`/v1/region/resolve` 제거** — device read-back은 `GET /v1/clinics/me`로 대체(내부 resolver FR-RGN-01은 §7.3 문서로 유지). `RegionResolveResponse`→`Clinic` 스키마.
4. **org-binding 자가등록 `/v1/clinics/me/org-bindings`**(device-self)·operator 교정은 `/v1/admin/org-mappings`.

## 결정 반영(#4)
- **#4a 리전 자가변경**: v1.0 device-self 허용(EzServer=C/S 운영·단일 리전이라 국경 간 없음)+전건 감사. **국경 간 주권 가드레일=gw/1.2 TBD**. 태그 `[v1.0 · gw/1.2 확장]`.
- **#4b 네임스페이스**: operator 전부 `/v1/admin/*`(버전 우선) · device-self+public `/v1/*`. `GET /v1/regions`(client read)만 예외로 `/v1`.

## 버전 태그 규약 (summary 말미)
`[v1.0]` · `[gw/1.1+]` · `[v1.0 · gw/1.2 확장]`(멀티리전 관련) · `[gw/1.2]`

> 갱신: OpenAPI 재구성 시 본 매트릭스 동기화. 최종 계약=OpenAPI, 본 문서=추적.
