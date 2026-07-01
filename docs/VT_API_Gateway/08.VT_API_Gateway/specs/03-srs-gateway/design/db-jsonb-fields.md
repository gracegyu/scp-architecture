# DB `jsonb` 필드 계약 (형식·예시·검증)

DBML(`vt-api-gateway.dbml`)의 `jsonb` 컬럼은 구조가 코드로 강제되지 않으므로, **구현 가능한 계약**(형식·예시·검증·기본값)을 여기서 정의한다. DBML은 이 파일을 SSOT로 참조(컬럼 주석에 shape 요약 + 링크). 값의 정확한 수치가 미결이면 해당 Appendix B 항목을 링크한다.

- 시간=Unix ms(bigint), 문자열=UTF-8. 여기 정의는 **애플리케이션 계층 검증**(예: class-validator/zod) 대상 — DB는 jsonb로만 저장.
- 경로/호스트 매칭 등 런타임 의미는 각 절에 명시한다.
- 관례: JSON 키는 camelCase(SRS §1.3 DTO 규칙과 동일).

---

## `policy` (OPA 입력, FR-INT-03)

`(tenant, connector)` 1행이 그 테넌트가 해당 connector로 호출할 때의 **허용 규칙**을 담는다. 요청 시 OPA가 `(target, method, path, scope, 목적지)`를 이 행과 대조해 allow/deny.

- **`tenant` = `clinic_id`**(FK → `clinic_region_mapping`). 테넌트 단위는 **클리닉**이다(device 단위 아님 — 10만대 granularity 회피). **`tenant = NULL`** 은 그 connector의 **전역 기본 정책**이다.
- **`connector`** = 아웃바운드 대상 토큰(= `connector.name` = `upstream_registry.target_id`, 예 `axs`). 인바운드 webhook의 `provider`와 동일 party이나 축이 다르며 통합 여부는 R8(§6.4.1).
- **평가 순서**: `(clinic_id, connector)` 매칭 우선 → 없으면 `(NULL, connector)` 전역 기본. 둘 다 없으면 **deny(fail-closed)**.
- 적용대상(클리닉)마다 다를 수 있어 **관리 UI(③-C)+관리 API(§7.9)** 필요 — Appendix B #32.

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

### `egress` — 아웃바운드 목적지·고정 IP 규칙
connector로 나가는 호출의 네트워크 제약(§7.5.3).

```json
{
  "allowedHosts": ["api.axs.straumann.com"],
  "allowedCidrs": ["198.51.100.0/24"],
  "allowedPorts": [443],
  "requireStaticEgressIp": true
}
```

- `allowedHosts`: 허용 FQDN 배열(정확 일치; 와일드카드 미지원 — 필요 시 별도 결정).
- `allowedCidrs`: 허용 목적지 CIDR 배열(IPv4/IPv6).
- `allowedPorts`: 허용 포트 배열(정수). 생략 시 `[443]`.
- `requireStaticEgressIp`: true면 고정 egress IP(NAT) 경유 강제.
- **검증**: host=FQDN, cidr=유효 CIDR, port=1–65535. `allowedHosts`·`allowedCidrs` 둘 다 비면 egress deny(fail-closed).

> **⚠️ egress 정의 중복(설계 정리 필요)**: 현재 egress 관련이 **3곳**에 있다 — `policy.egress`(OPA 규칙), `connector.egress_allowlist`(external 자격/주소), `upstream_registry.egress_allowlist`(프록시 라우팅). SSOT 이원화 위험 → 하나를 권위로 정하고 나머지는 참조/제거 필요. **Appendix B #31**로 추적.

---

## `connector` (external 자격/주소)

### `egress_allowlist`
```json
{ "hosts": ["api.axs.straumann.com"], "cidrs": ["198.51.100.0/24"], "ports": [443] }
```
- `policy.egress`와 동일 구조(위 ⚠️ 참조 — SSOT 정리 대상). 여기서는 connector 실제 호출 시 적용할 egress 목적지.

---

## `upstream_registry` (target-routed proxy, ADR-11)

### `egress_allowlist`
- external(C) target일 때만 사용. 구조는 `connector.egress_allowlist`와 동일(위 ⚠️).

### `retry_policy` — 프록시 재시도 설정(§7.5.4)
```json
{
  "retryOn": ["connect_failure"],
  "maxRetries": 1,
  "backoff": { "type": "exponential", "baseMs": 50, "maxMs": 500 },
  "budgetRatio": 0.1
}
```
- `retryOn`: 재시도 트리거 배열. **v1.0=`["connect_failure"]` 한정**(연결 실패만; 비멱등 POST의 응답단계 재시도 금지, §7.5.4).
- `maxRetries`: 정수 상한.
- `backoff`: `{ type: "exponential"|"fixed", baseMs, maxMs }`.
- `budgetRatio`: 전체 요청 대비 재시도 허용 비율(재시도 폭주 방지).
- **검증**: `retryOn` ⊆ {connect_failure}(v1.0), `maxRetries`≥0, ms≥0.
- **수치 미결**: 정확한 값·서킷 포함 범위 = **Appendix B #25**(정책 골격만 확정).

---

## `webhook_provider` (유연 수신 config, FR-WH-01/02)

### `source_ip_allowlist` — 허용 소스 CIDR(옵션·방어심층)
```json
["203.0.113.0/24", "198.51.100.7/32"]
```
- **타입**: CIDR 문자열 배열. 발신자 **식별은 Host/SNI**(inbound_host)가 하고, 이 목록은 **옵션 방어심층**(비어 있으면 IP 체크 생략, §7.6.2).
- **검증**: 각 원소 유효 CIDR.

---

## 변경 이력
| 일시 | 내용 |
| --- | --- |
| 2026-07-01 | 신설 — DB jsonb 컬럼(policy 3개·connector/upstream egress·retry_policy·webhook source_ip) 형식·예시·검증 정의. egress 3중복 → Appendix B #31 |
