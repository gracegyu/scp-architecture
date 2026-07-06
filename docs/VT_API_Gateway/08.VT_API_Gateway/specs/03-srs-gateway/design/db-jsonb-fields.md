# DB `jsonb` 필드 계약 (형식·예시·검증)

DBML(`vt-api-gateway.dbml`)의 `jsonb` 컬럼은 구조가 코드로 강제되지 않으므로, **구현 가능한 계약**(형식·예시·검증·기본값)을 여기서 정의한다. DBML은 이 파일을 SSOT로 참조(컬럼 주석에 shape 요약 + 링크). 값의 정확한 수치가 미결이면 해당 Appendix B 항목을 링크한다.

- 시간=Unix ms(bigint), 문자열=UTF-8. 여기 정의는 **애플리케이션 계층 검증**(예: class-validator/zod) 대상 — DB는 jsonb로만 저장.
- 경로/호스트 매칭 등 런타임 의미는 각 절에 명시한다.
- 관례: JSON 키는 camelCase(SRS §1.3 DTO 규칙과 동일).

---

## `policy` (OPA 입력, FR-INT-03)

`(scope_type, scope_id, connector)` 1행이 그 스코프가 해당 connector로 호출할 때의 **허용 규칙**을 담는다. **주체 = device**(§1.2). 요청 시 OPA가 `(target, method, path, scope, 목적지)`를 실효 정책과 대조해 allow/deny.

- **`scope_type`(global | clinic | device) + `scope_id`** — 정책 부착 스코프. global=`scope_id` NULL / clinic=`clinic_id` / device=`device_id`. **다형 참조라 하드 FK 없음**(discriminator + 앱레벨 무결성). 구 `tenant`(clinic 하드 FK)를 device-중심으로 일반화(clinic-less device 수용, §6.4.1).
- **`connector`** = 아웃바운드 대상 토큰(= `connector.name` = `upstream_registry.target_id`, 예 `axs`). 인바운드 webhook의 `provider`와 동일 party이나 축이 다르며 통합 안 함(§6.4.1).
- **평가 순서(주체 device 기준)**: `device` → 그 device의 `clinic` → `global` 순으로 판정(deny-by-default). **clinic = clinic-bound device의 상한(ceiling)**, `device`는 그 안에서 narrowing, `global`=전역 기본. 규칙=**SRS §7.5.3**, 차원별 병합=OPA(Rego)/LLD. **v1.0은 clinic+global 행만 사용**(모든 device가 clinic-bound).
- 적용대상(스코프)마다 다를 수 있어 **관리 UI(③-C)+관리 API(§7.9)** 필요 — Appendix B #32.

### `allowed_endpoints` — 허용 (method, path) 목록
GW는 upstream으로 verbatim 프록시하므로(§4.1.2), **정책은 (method + path)** 로 허용 범위를 판정한다(§4.1.2 규칙3).

```json
[
  { "methods": ["GET"],          "pathPattern": "/v1/patients/**" },
  { "methods": ["POST", "PUT"],  "pathPattern": "/v1/studies/*/files" },
  { "methods": ["*"],            "pathPattern": "/v1/orders/**" }
]
```

- **타입**: 객체 배열. 배열 내 **하나라도 매칭되면 허용**(OR).
- `methods`: HTTP 메서드 배열. `["*"]` = 모든 메서드. 허용값 `GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS|*`.
- `pathPattern`: 글롭 패턴. **`*` = 경로 세그먼트 1개**(슬래시 미포함), **`**` = 0개 이상 세그먼트**. 반드시 `/`로 시작. upstream 요청 경로(host 교체 후, 쿼리스트링 제외)에 매칭.
- **기본값(fail-closed)**: 배열이 비었거나 매칭 없음 → **deny**. (허용은 명시적으로만.)
- **검증**: 배열≥0, 각 원소 `methods`(비어있지 않음·허용값), `pathPattern`(`/` 시작).

### `scopes` — 허용 OAuth scope 집합
요청 토큰의 scope ⊆ 이 집합이어야 통과.

```json
["axs:patient.read", "axs:study.write", "axs:upload"]
```

- **타입**: 문자열 배열(집합). 소문자 `provider:resource.action` 관례.
- **검증**: 각 원소 비어있지 않은 토큰. 중복 무시.
- **기본값**: 빈 배열 = 어떤 scope도 불허(fail-closed).

---

## `connector` (external 자격/주소) — **egress SSOT (#31)**

### `egress_allowlist` — 아웃바운드 목적지·고정 IP 규칙
외부(C) connector 호출의 네트워크 제약(§7.5.3). **egress의 단일 SSOT** — `policy`·`upstream_registry`에 중복 두지 않는다(2026-07-06, #31 해소). OPA egress 판정과 네트워크(고정 EIP whitelist·SG)가 모두 이 값을 참조.

```json
{
  "hosts": ["api.axs.straumann.com"],
  "cidrs": ["198.51.100.0/24"],
  "ports": [443],
  "requireStaticEgressIp": true
}
```

- `hosts`: 허용 FQDN 배열(정확 일치; 와일드카드 미지원 — 필요 시 별도 결정).
- `cidrs`: 허용 목적지 CIDR 배열(IPv4/IPv6).
- `ports`: 허용 포트 배열(정수). 생략 시 `[443]`.
- `requireStaticEgressIp`: true면 고정 egress IP(NAT) 경유 강제(구 `policy.egress`에서 이관).
- **검증**: host=FQDN, cidr=유효 CIDR, port=1–65535. `hosts`·`cidrs` 둘 다 비면 egress deny(fail-closed).
- **external(C) connector에만** 적용 — 내부(B)는 내부망이라 egress allowlist 불요(§4.1.1).

---

## `upstream_registry` (target-routed proxy, ADR-11)

> **jsonb 필드 없음.** egress는 **`connector.egress_allowlist`(SSOT, #31)** 로 이관, 재시도·서킷은 **service mesh(istio) egress**(7/2 R4·GitOps), 연결 timeout(`connect_timeout_ms`/`response_timeout_ms`/`total_deadline_ms`)은 **GW 책임 스칼라 컬럼**(D1~D3·§7.5.4). 즉 upstream_registry는 라우팅(target→host)·enabled·timeout 스칼라만(jsonb 없음). timeout 수치=Appendix B #25.

---

## `webhook_provider` (유연 수신 config, FR-WH-01/02)

### `source_ip_allowlist` — 허용 소스 CIDR(옵션·방어심층)
```json
["203.0.113.0/24", "198.51.100.7/32"]
```
- **타입**: CIDR 문자열 배열. 발신자 **식별은 Host/SNI**(inbound_host)가 하고, 이 목록은 **옵션 방어심층**(비어 있으면 IP 체크 생략, §7.6.2).
- **검증**: 각 원소 유효 CIDR.

---

## `config` (중앙 Config 값 — jsonb + 키 레지스트리, §7.8.4)

`config` 테이블 1행 = `(scope_type, scope_id, config_key)` → `config_value`(jsonb). `config_value`는 구조가 코드로 강제되지 않으므로, **키별 값 타입·허용범위를 앱 레벨 키 레지스트리(스키마)** 로 검증한다. device 실효 config는 **키별 가장 구체 스코프 우선**(device > clinic > region > global, override 병합).

### `config_key` — 네임스페이스 규약
```
gw.heartbeat.interval_seconds        gw.heartbeat.offline_threshold_multiplier        device.upload.max_concurrency
```
- **형식**: `^(gw|device)\.[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$` (점 구분 소문자·언더스코어).
- **네임스페이스**: `gw.*` = **GW가 소비**(GW 동작·응답에 반영) · `device.*` = **device로 전달**(GW 비해석, device가 적용).
- **키 레지스트리(초기 seed — 앱 레벨 상수, 확장 가능·비열거적)**: 아래는 **현재 예상되는 항목의 예시**이며 **완전한 목록이 아니다**. 새 설정은 개발 시 이 표(=앱 레벨 상수)에 한 줄씩 추가하면 되고, `config_key`가 DB enum이 아니라 **마이그레이션 없이** 늘어난다. 각 키는 `type`·허용범위·기본값(fallback)·소비자를 명시한다.

  | config_key | 타입 | 허용범위/enum | 기본값(fallback) | 소비자 | 비고 |
  | --- | --- | --- | --- | --- | --- |
  | `gw.heartbeat.interval_seconds` | integer(초) | 60~86400 | `.env` `DEFAULT_HEARTBEAT_INTERVAL_SECONDS`(정본 기본=Appendix B #34) | GW | heartbeat 응답 `nextIntervalSeconds`로 하달(§7.8.1) |
  | `gw.heartbeat.offline_threshold_multiplier` | number | 1.5~10 | 3 | GW | `now-last_heartbeat > interval×배수`면 offline 판정 |
  | `device.log.level` | string(enum) | `error\|warn\|info\|debug` | `info` | device | 로그 상세도 원격 조정 |
  | `device.upload.max_concurrency` | integer | 1~8 | 2 | device | 동시 업로드 수 |
  | `device.upload.chunk_size_bytes` | integer | 1048576~67108864 | 8388608(8MiB) | device | 멀티파트 청크 크기 |
  | `device.telemetry.metrics_enabled` | boolean | true/false | true | device | heartbeat metrics 전송 on/off |
  | `device.feature_flags` | object(bool 맵) | `{ "<flag>": true\|false }` | `{}` | device | 확장형 기능 토글(개별 flag는 device측 정의) |

- **DB enum이 아니다** — 신규 키는 기능 추가로 계속 늘어, 앱 레벨 상수 집합 + 위 정규식으로 검증하고 신규 키는 상수만 추가한다. 등록되지 않은 키·범위 밖 값은 관리 API(`PUT /admin/v1/config`)에서 거부한다.

### `config_value` — 값 형식
```json
3600
```
```json
{ "maxConcurrency": 4, "chunkSizeBytes": 8388608 }
```
- **타입**: jsonb 스칼라(number/string/boolean) 또는 객체. 키 레지스트리가 키별 기대 타입을 정의.
- **검증**: 해당 `config_key`의 레지스트리 스키마와 타입·범위 일치. **PHI 금지**(§6.4).
- **버전**: 행의 `version`(bigint)은 변경 시 증가. 한편 device에 주는 **실효 `configVersion`은 콘텐츠 해시**(string) — 기여 항목을 `(config_key, config_value, 기여 행 version)`로 정렬·canonical JSON 직렬화 후 SHA-256 hex. 값·기여 스코프·행 version 중 하나라도 바뀌면 해시가 바뀌고 아니면 안정적이다. device는 `appliedConfigVersion`과 **동등성만 비교**해 drift 판정. (행 version 최댓값·전역 카운터는 쓰지 않음 — §7.8.4.)

### 스코프·해석
- **`scope_type`(global | region | clinic | device) + `scope_id`** — global=NULL / region=`region_id` / clinic=`clinic_id` / device=`device_id`. **다형 참조·하드 FK 없음**(policy와 동일 방식).
- **실효 config**: 각 키를 **가장 구체 스코프 값으로 확정**(device > clinic > region > global). 정책의 deny-by-default와 달리 **override 병합**(키 단위 최우선 승자).

---

## `audit_log` (문자열 규약 — jsonb 아님, 필드 형식 SSOT)

`action`·`actor`는 자유 문자열이지만 **일관 조회·감사 리포트를 위해 명명 규약을 강제**한다(앱 레벨 검증, DB enum 아님 — 확장성). `result`는 값이 한정적이라 **DB enum**(`audit_result`, DBML)이다.

### `action` — `resource.verb` (소문자·점 구분)
```
region.change   device.approve   credential.rotate   policy.update
```
- **형식**: `^[a-z][a-z0-9]*(\.[a-z][a-z0-9]*)+$` (소문자 `resource`.`verb`, 최소 1개 점).
- **표준 목록(초기 — 앱 레벨 상수, 확장 가능)**: `region.change` · `device.approve` · `device.suspend` · `device.revoke` · `enroll.rotate` · `credential.issue` · `credential.rotate` · `policy.create` · `policy.update` · `policy.delete` · `orgmapping.upsert` · `upstream.register` · `connector.update` · `killswitch.toggle` · `config.publish`.
- **DB enum이 아니다** — 감사 동작은 기능 추가로 계속 늘어 enum이면 매번 마이그레이션이 필요하다. 대신 **앱 레벨 상수 집합**으로 관리하고 위 정규식으로 검증하며, 신규 action은 상수만 추가한다. **자유 오타 문자열(예 `리전변경`)은 금지**.

### `actor` — `type:id`
```
user:oneid-8f3a…      system:token-refresh      device:0192abcd-…
```
- **형식**: `^(user|system|device):.+$` — 모호한 "운영자/시스템"을 접두사로 구분한다.
  - `user:{oneidSub}` — 사람(운영자/Admin/C-S). OneID subject.
  - `system:{component}` — 자동 주체(예 `system:token-refresh` · `system:webhook-dispatcher` · `system:enroll`).
  - `device:{deviceId}` — 디바이스 개시 동작.

### `result` — enum (`audit_result`, DBML)
- `success`(수행됨) · `denied`(권한·정책 거부) · `failure`(시도했으나 실패). 값 확장은 DBML enum 수정으로만.

---

## 변경 이력
| 일시 | 내용 |
| --- | --- |
| 2026-07-01 | 신설 — DB jsonb 컬럼(policy 3개·connector/upstream egress·retry_policy·webhook source_ip) 형식·예시·검증 정의. egress 3중복 → Appendix B #31 |
| 2026-07-02 (R4) | `upstream_registry.retry_policy` 형식 섹션 제거 — **재시도·서킷=service mesh(istio) 담당**(GW 미소유). **단 GW→provider 연결 timeout(connect/response/total_deadline)은 GW 책임이라 스칼라 컬럼 유지**(D1~D3, §7.5.4). jsonb 대상은 egress_allowlist만 |
| 2026-07-06 | `policy` 키를 `(tenant=clinic)` → **`(scope_type{global\|clinic\|device}, scope_id, connector)`** 로 일반화 — 주체=device·clinic=선택적 그룹(§1.2·§6.4.1), 실효정책 device→clinic→global. jsonb 필드(allowed_endpoints·scopes) 형식은 불변 |
| 2026-07-06 (#31) | **egress SSOT 일원화** — `connector.egress_allowlist` 단일 SSOT(+requireStaticEgressIp 이관). `policy.egress`·`upstream_registry.egress_allowlist` 섹션·컬럼 제거. egress=외부(C) 대상 속성(per-tenant authz 아님), OPA/네트워크가 connector 참조 |
| 2026-07-06 | **`audit_log` 문자열 규약 신설** — `action`=`resource.verb` 명명 규약(free string·정규식·표준 목록·앱 레벨 상수, DB enum 아님) · `actor`=`type:id`(user/system/device) · `result`=DB enum `audit_result`(success/denied/failure). §7.9.3에서 참조 |
| 2026-07-06 | **`config` 값 계약 신설(§7.8.4 중앙 Config)** — `config_key` 네임스페이스 규약(`gw.*` GW 소비 / `device.*` 전달·정규식·**키 레지스트리 seed 7종**: heartbeat interval/threshold·log.level·upload concurrency/chunk·telemetry·feature_flags, type/범위/기본값/소비자·확장형·미등록/범위밖 거부) · `config_value` jsonb 형식·검증(PHI 금지) · **실효 `configVersion`=콘텐츠 해시(SHA-256, 행 version 최댓값 아님)** · 스코프(global/region/clinic/device)·실효 해석(키별 가장 구체 우선 override). DBML `config` 테이블 신설과 정합 |
