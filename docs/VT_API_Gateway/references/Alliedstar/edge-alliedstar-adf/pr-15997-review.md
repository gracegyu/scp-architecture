# PR 15997 리뷰 대응 — VT Edge device 수용 · Alliedstar 커넥터 FR-INT-08 (1라운드)

- PR: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/15997
- 리뷰: Thomas — Nemesis 자동 리뷰 7건(인라인 6 + 요약 1) · Claude Code review 6건
- 판단 기준: **시연 1회용 — 일을 키우지 않는다.** 문서 정합은 반영, 운영 수준 장치는 위험 수용·1차로 명시
- 일부 지적(timeout·egress)은 리뷰 시점 이후 커밋에서 이미 반영됨 — 답변에 그 사실을 적음

## 요약

| 스레드 | 출처 | 지적 | 판단 |
| --- | --- | --- | --- |
| 104526 | Nemesis | 표의 `internal_bypass` 예시 target 을 "Alliedstar 커넥터(§7.5.8)"로 바… | 수용 |
| 104527 | Nemesis | "내부 target 규약 ③b"를 근거로 device 토큰을 그대로 전달한다고 썼습니다. 그런데 본문의 ③b… | 부분 수용 |
| 104528 | Nemesis | 원내 범위 보호를 `getCaseDetail` 에만 정의했습니다. 그런데 업무 API 표에는 caseCode… | 부분 수용 |
| 104529 | Nemesis | `createCase` 가 타임아웃되면 `result=unknown` 으로 남기는데, 이때는 `case_co… | 수용(②) |
| 104530 | Nemesis | 여기 적힌 timeout 은 VTG core→커넥터 구간의 target timeout(§7.5.4)뿐입니다.… | 이미 반영 + 일부 수용 |
| 104531 | Nemesis | 업체 API 열의 표기가 섞여 있습니다. `open/order/*` 는 앞에 `/` 가 없고 `/open/v… | 수용 |
| 104534 | Claude Code | "2xx 가 아닌 응답 → 502 `TARGET_UNREACHABLE`"로 묶으면, 업체가 요청을 **처리한… | 부분 수용 |
| 104535 | Claude Code | "egress 허용 목록에 그 host 만 둔다(§7.5.3)"는 지금 문장으로는 보장 수단이 없습니다. §… | 이미 정정 + 위험 수용 |
| 104536 | Claude Code | `TARGET_TIMEOUT` 은 출처가 두 곳입니다.… | 수용 |
| 104537 | Claude Code | "커넥터는 재시도하지 않는다"와 "재시도·서킷은 mesh(istio) 담당"(§7.5.4·§7.7.4)이 함… | 위험 수용(시연) |
| 104538 | Claude Code | 커넥터 전용 최소 권한 DB 계정을 1차로 미루면, 시연 동안 커넥터는 core 와 같은 계정으로 `devi… | 위험 수용 명시 + 수용 |
| 104539 | Claude Code | core 의 `apps/core/src/compat/header.middleware.ts` 는 `Vatech… | 수용 |
| 104533 | Nemesis | ## Code Review (Other)… | 회신 |

## 스레드 104526

- 작성자: 민진우(Thomas) · 위치: `/docs/specs/SRS.md:2359`

**원문**

> From Nemesis(v0.9.5, 🆔mwa0b4d81ku),
> **🔧 수정 필요**
>
> 표의 `internal_bypass` 예시 target 을 "Alliedstar 커넥터(§7.5.8)"로 바꿨지만, 같은 절의 서술 두 곳은 그대로 "**v1.0 확정 사용처 없음**"이라고 적고 있습니다. 하나는 바로 위 요약(L2353)이고, 다른 하나는 바로 아래 `internal_bypass` (상세)(L2362)입니다. 한 절 안에서 표와 서술이 서로 다른 말을 하고 있으므로 통제 문서(IEC 62304 추적성) 기준으로 정합이 맞지 않습니다. 두 서술도 "v1.0 사용처 = Alliedstar 커넥터(ADF 시연·§7.5.8) · CleverSpace 는 ③b P0 후"로 고쳐야 합니다.

**판단 — 수용** · 문서 정합 — §7.5.1 의 `internal_bypass` 서술 두 곳을 표와 맞춘다.

**답변**

> 반영했습니다. §7.5.1 요약과 `internal_bypass` 상세 두 곳을 "v1.0 사용처 = Alliedstar 커넥터(ADF 시연 · §7.5.8) · CleverSpace 는 신원 전달 결정 후"로 고쳐 표와 맞췄습니다.

## 스레드 104527

- 작성자: 민진우(Thomas) · 위치: `/docs/specs/SRS.md:2583`

**원문**

> From Nemesis(v0.9.5, 🆔mwa0b4d81ku),
> **💡 권장**
>
> "내부 target 규약 ③b"를 근거로 device 토큰을 그대로 전달한다고 썼습니다. 그런데 본문의 ③b 는 GW→CleverSpace 홉으로 정의돼 있고, 그 신원 전달 방식은 "미정(P0)"이며 실제 소비처는 v1.1 입니다(§2.3.0·§7.1.5·§7.5.1 L2362). 이 줄은 사실상 "내부 B target 은 device 토큰을 verbatim 전달한다"(③b 차선안)를 v1.0 에서 Alliedstar 에 먼저 채택하는 결정입니다. Appendix B #57 이나 §7.5.1 에 이 결정과 범위를 밝혀 두기를 권합니다. 예: "③b P0 는 CleverSpace 에 대해서는 여전히 미정이고 Alliedstar 는 verbatim 안을 적용한다."
> 또 §7.1.5 의 신뢰 모델에는 전제가 있습니다. 검증 주체의 라우트에 GW 말고 다른 ingress 가 없어야 한다는 것입니다. verbatim 토큰은 bearer 라서 GW 를 거쳤다는 증명이 되지 않기 때문입니다. 따라서 "클러스터 내부 전용"(L2581)만으로는 부족합니다. VTG core 만 커넥터에 닿을 수 있도록 하는 수단(NetworkPolicy·mesh AuthorizationPolicy 등)을 요구사항으로 적어 두는 것이 안전합니다.

**판단 — 부분 수용** · ③b 결정 범위 명시는 문서 한 줄이라 반영. 커넥터 ingress 를 core 로만 제한하는 인프라 장치(NetworkPolicy 등)는 시연 범위에서는 위험 수용 — 클러스터 내부 Service 이고 유효한 device 토큰이 있어야 한다. 1차로.

**답변**

> 반영했습니다. 결정 기록 57번과 §7.5.1 에 "내부 target 에 device 토큰을 그대로 전달하는 방식은 Alliedstar 커넥터에 한해 v1.0 에서 먼저 적용하고, CleverSpace 의 신원 전달 방식은 여전히 미정"이라고 범위를 밝혔습니다. 커넥터에 core 만 닿게 하는 장치(NetworkPolicy·mesh 인가 정책)는 이번 시연에서는 넣지 않고 위험을 받아들이는 것으로 적었습니다. 커넥터는 외부 노출이 없는 클러스터 내부 Service 이고, 호출하려면 유효한 device 토큰이 있어야 하기 때문입니다. 운영 단계(1차)에서 요구사항으로 올리겠습니다.

## 스레드 104528

- 작성자: 민진우(Thomas) · 위치: `/docs/specs/SRS.md:2604`

**원문**

> From Nemesis(v0.9.5, 🆔mwa0b4d81ku),
> **💡 권장**
>
> 원내 범위 보호를 `getCaseDetail` 에만 정의했습니다. 그런데 업무 API 표에는 caseCode·orderCode 만으로 대상을 고를 수 있는 API 가 더 있습니다. `getCaseTreatmentPdf`·`caseShow`·`v3/case/refreshCommand`·`getOrderDetail`·`getOrderTreatmentPdf`·`setOrderStatus`·`sendOrder` 등입니다. 이 API 들을 업체가 `openid` 로 원내 범위를 거르는지 명시돼 있지 않습니다. 거르지 않는다면 한 원내가 다른 원내의 케이스·주문을 조회하거나 변경할 수 있습니다. "openid 로 업체가 범위를 거르는 API"와 "커넥터가 대장으로 확인해야 하는 API"를 API 별로 구분해 표에 적고, 그에 맞는 TC 를 추가하기를 권합니다.

**판단 — 부분 수용** · 업체 문서상 나머지 API 는 모두 `openid` 가 필수라 업체가 원내 범위를 거른다. `openid` 없이 caseCode 만 받는 것은 `getCaseDetail` 하나. 표에 원내 범위 열을 추가하는 정도로 반영. 시연은 createCase·refreshCommand 만 쓰므로 TC 추가는 하지 않음.

**답변**

> 업체 공식 문서를 다시 대조했습니다. 말씀하신 `getCaseTreatmentPdf`·`caseShow`·`refreshCommand`·`getOrderDetail`·`getOrderTreatmentPdf`·`setOrderStatus`·`sendOrder` 는 모두 `openid` 가 필수 파라미터라 업체가 그 사용자 범위로 거르고, 커넥터는 연결된 `openid` 만 넣습니다. `openid` 없이 `caseCode` 만으로 조회되는 것은 `getCaseDetail` 하나뿐이라 대장 확인을 거기에만 두었습니다. 이 판단이 드러나도록 업무 API 표에 API 별 원내 범위 열을 추가했습니다. 이번 시연은 `createCase`·`refreshCommand` 만 쓰므로 별도 TC 는 추가하지 않았습니다.

## 스레드 104529

- 작성자: 민진우(Thomas) · 위치: `/docs/specs/SRS.md:2605`

**원문**

> From Nemesis(v0.9.5, 🆔mwa0b4d81ku),
> **💡 권장**
>
> `createCase` 가 타임아웃되면 `result=unknown` 으로 남기는데, 이때는 `case_code` 를 알 수 없습니다(DBML L477 "성공 시"). 그 뒤 Edge 가 `listCases` 로 실제 생성 여부를 확인해도 대장에는 그 clinic 의 `case_code` 가 없습니다. 그래서 L2604 규칙에 따라 해당 케이스의 `getCaseDetail` 은 계속 403 이 됩니다. 업체에 생성된 정당한 케이스를 끝내 조회할 수 없는 상태가 됩니다. 두 가지 중 하나를 정해 두기를 권합니다. ① `listCases`(openid 범위) 응답에서 `externalCaseCode` 로 unknown 행을 맞춰 `case_code` 를 채운다. ② 시연 범위에서는 이 한계를 받아들인다고 비목표에 명시한다.

**판단 — 수용(②)** · 시연은 getCaseDetail 을 쓰지 않음(범위 = 케이스 생성·촬영 실행). unknown 맞추기는 1차 비목표로 명시.

**답변**

> 이번 시연 범위가 케이스 생성과 촬영 실행까지로 정해져 `getCaseDetail` 을 쓰지 않으므로, 두 번째 안으로 정리했습니다. 결과가 불명인 케이스를 `listCases` 의 `externalCaseCode` 로 나중에 맞추는 것은 1차 범위로 §7.5.8 범위 밖에 적었습니다.

## 스레드 104530

- 작성자: 민진우(Thomas) · 위치: `/docs/specs/SRS.md:2610`

**원문**

> From Nemesis(v0.9.5, 🆔mwa0b4d81ku),
> **💡 권장**
>
> 여기 적힌 timeout 은 VTG core→커넥터 구간의 target timeout(§7.5.4)뿐입니다. 커넥터→업체 호출의 timeout 은 정의돼 있지 않습니다. 커넥터 쪽 업체 timeout 이 VTG 응답 timeout(15초)보다 짧지 않으면 문제가 생깁니다. VTG core 가 먼저 자기 504 를 돌려주고 커넥터 호출을 취소하면(§7.5.4 취소 전파), 커넥터가 504 를 반환하거나 대장에 `result=unknown` 을 기록하는 과정이 실행되지 않을 수 있습니다. TC-ASC-10(UnitTCL L548)도 "> 15초"를 기준으로 하지만, 이것이 어느 쪽 timeout 인지 모호합니다. 해결 방법은 두 가지입니다. 커넥터의 업체 호출 timeout 을 별도 값으로 정하되 VTG response timeout 보다 작게 하는 불변식을 둡니다(예: 업체 12초 < VTG 15초). 그리고 커넥터가 상위 요청이 취소되더라도 unknown 기록을 마치도록 요구사항에 넣습니다.

**판단 — 이미 반영 + 일부 수용** · 커넥터→업체 제한(14초) < VTG 응답(15초) 불변식은 554940b 에서 반영됨. TC-ASC-10 도 14초 기준으로 정정됨. "상위 요청이 취소돼도 unknown 기록을 마친다" 한 줄 추가.

**답변**

> 커넥터의 업체 호출 제한을 별도 값(기본 14초)으로 두고 VTG 응답 시간(15초)보다 짧게 한다는 불변식은 이후 커밋에서 이미 반영했고, TC-ASC-10 도 커넥터 제한 기준으로 고쳤습니다. 말씀하신 대로 "상위 요청이 취소되더라도 커넥터는 대장에 결과 불명 기록을 마친다"는 문장을 시간 제한 항목에 추가했습니다.

## 스레드 104531

- 작성자: 민진우(Thomas) · 위치: `/docs/specs/SRS.md:2592`

**원문**

> From Nemesis(v0.9.5, 🆔mwa0b4d81ku),
> **💡 권장**
>
> 업체 API 열의 표기가 섞여 있습니다. `open/order/*` 는 앞에 `/` 가 없고 `/open/v3/case/refreshCommand` 는 `/` 가 있습니다. DBML `alliedstar_job.method` 예시도 `open/order/createCase` 형식입니다. 커넥터의 경로 매핑과 대장 `method` 값이 이 표를 근거로 구현되므로 표기를 하나로 맞추기를 권합니다.

**판단 — 수용** · 표기 통일 — 업체 경로를 `open/...`(앞 `/` 없음)으로 맞추고 v3 경로도 같은 규칙.

**답변**

> 반영했습니다. 업체 API 열을 앞에 `/` 가 없는 `open/...` 형식으로 통일했고 `open/v3/case/refreshCommand` 도 같은 규칙으로 고쳤습니다. 대장 `method` 예시와도 맞습니다.

## 스레드 104534

- 작성자: 민진우(Thomas) · 위치: `/docs/specs/SRS.md:2620`

**원문**

> From Claude Code review,
> **🔧 수정 필요**
>
> "2xx 가 아닌 응답 → 502 `TARGET_UNREACHABLE`"로 묶으면, 업체가 요청을 **처리한 뒤에** 5xx 를 돌려준 경우까지 "업체에 닿지 못했다"는 뜻의 코드가 됩니다. 이때 `createCase`·`createPatient`·`sendOrder`·`setOrderStatus` 는 이미 실행됐을 수 있습니다. L2623 이 "Edge 는 `errorCode` 로 판단한다"고 했으므로, Edge 는 `TARGET_UNREACHABLE` 을 보고 다시 만들어도 된다고 판단하기 쉽습니다. 그러면 중복 생성으로 이어집니다.
>
> 제안:
> - `TARGET_UNREACHABLE` 은 요청을 보내지 못한 연결 실패(거부·DNS·TLS)에만 씁니다.
> - 요청을 보낸 뒤 받은 비2xx 는, 부작용이 있는 위 4개 API 에 한해 `TARGET_TIMEOUT` 과 같은 "결과 불명"으로 처리하고 대장에 `result=unknown` 을 남깁니다.
> - 지금 대장 규칙은 비2xx 일 때 무엇을 남기는지 정의하지 않습니다. 이 경우의 TC(업체 500 응답 시 `createCase` 처리)도 추가해 주세요.
>

**판단 — 부분 수용** · 오류 코드 체계는 바꾸지 않음(구현 변경 없음). 대신 Edge 규칙을 넓힘: 부작용 있는 4개 API 는 502·504 모두 재생성 금지·listCases 확인. 대장은 요청을 보낸 뒤의 비2xx 를 unknown 으로 남긴다(구현과 일치)는 것을 명시. TC-ASC-10 에 업체 500 케이스 추가.

**답변**

> 지적하신 위험(업체가 처리한 뒤 5xx 를 돌려준 경우 Edge 가 다시 만드는 것)에 동의합니다. 다만 시연 일정상 오류 코드 체계를 나누기보다 Edge 규칙을 넓히는 쪽으로 정리했습니다. `createCase`·`createPatient`·`sendOrder`·`setOrderStatus` 는 502 든 504 든 다시 만들지 말고 `listCases` 로 확인한다고 적었고, 요청을 보낸 뒤 받은 2xx 가 아닌 응답은 대장에 결과 불명으로 남긴다는 규칙을 명시했습니다(현재 구현과 같습니다). TC-ASC-10 에 업체 500 응답 시 `createCase` 처리를 추가했습니다.

## 스레드 104535

- 작성자: 민진우(Thomas) · 위치: `/docs/specs/SRS.md:2609`

**원문**

> From Claude Code review,
> **🔧 수정 필요**
>
> "egress 허용 목록에 그 host 만 둔다(§7.5.3)"는 지금 문장으로는 보장 수단이 없습니다. §7.5.3 의 `target.egress_allowlist` 는 **VTG core 가 외부(C) target 을 부를 때** PDP·Istio 가 판정하는 값이고, 내부(B) target 은 "egress allowlist 불요"로 정의돼 있습니다. 커넥터는 `internal_bypass` target 뒤의 별도 워크로드이고 업체를 직접 호출하므로, 이 판정을 지나지 않습니다.
>
> 제안: 커넥터 워크로드 기준의 egress 제한(Istio ServiceEntry·Sidecar egress 또는 NetworkPolicy 로 `ALLIEDSTAR_API_HOST` 만 허용, fail-closed)을 요구사항으로 적어 주세요. 그리고 OnePager(PR 15974) §8.5 I6 의 인프라 작업과 연결해 주세요.
>

**판단 — 이미 정정 + 위험 수용** · 8aefb88 에서 "커넥터 파드 egress 정책(인프라)"으로 정정됨. 그런데 Jack 확인상 현재 클러스터는 egress 를 제한하지 않음 → 시연은 업체 host 를 설정으로 고정하는 것으로 갈음, 인프라 egress 제한은 1차로 명시.

**답변**

> 이 문장은 이후 커밋에서 "업체 host 로 나가는 egress 는 커넥터 파드의 egress 정책(인프라)"으로 이미 고쳤습니다. 다만 인프라 확인 결과 현재 클러스터는 외부 egress 를 제한하지 않고 있어, 이번 시연에서는 커넥터가 호출하는 host 를 설정(`ALLIEDSTAR_API_HOST`)으로 고정하는 것으로 갈음하고, 커넥터 워크로드의 egress 제한은 1차 요구사항으로 적었습니다.

## 스레드 104536

- 작성자: 민진우(Thomas) · 위치: `/docs/specs/SRS.md:2623`

**원문**

> From Claude Code review,
> **💡 권장**
>
> `TARGET_TIMEOUT` 은 출처가 두 곳입니다.
> - 커넥터가 업체를 기다리다 낸 504: `Vatech-Error-Origin: target`. 이 경우 대장에 `unknown` 이 남습니다.
> - VTG core 가 커넥터를 기다리다 낸 504: `gateway`(§7.7.4). 커넥터가 멈췄거나 전체 20초를 넘긴 경우로, 대장에 **아무것도 남지 않았을 수** 있습니다.
>
> Edge 가 취할 행동(재생성 금지, `listCases` 로 확인)은 두 경우가 같으므로 계약은 그대로 둬도 됩니다. 다만 "`TARGET_TIMEOUT` 이면 대장에 unknown 행이 있다"고 가정하지 않는다는 점을 한 줄 적어 두길 권합니다. unknown 행을 나중에 맞추는 방법(L2605 코멘트)을 정할 때, 대장에 행이 없는 경우도 함께 다뤄야 합니다.
>

**판단 — 수용** · 한 줄 추가 — TARGET_TIMEOUT 이어도 대장에 행이 없을 수 있다.

**답변**

> 반영했습니다. `TARGET_TIMEOUT` 은 커넥터가 낸 것일 수도 VTG core 가 낸 것일 수도 있어, 후자는 대장에 행이 없을 수 있다는 점을 한 줄 적었습니다. Edge 의 행동(다시 만들지 않고 `listCases` 로 확인)은 두 경우 모두 같습니다.

## 스레드 104537

- 작성자: 민진우(Thomas) · 위치: `/docs/specs/SRS.md:2606`

**원문**

> From Claude Code review,
> **💡 권장**
>
> "커넥터는 재시도하지 않는다"와 "재시도·서킷은 mesh(istio) 담당"(§7.5.4·§7.7.4)이 함께 적혀 있습니다. mesh 기본 재시도 정책(예: 503·connect-failure 시 재시도)이 core→커넥터 경로나 커넥터→업체 egress 에 적용되면, `createCase` 같은 비멱등 POST 가 커넥터 코드와 상관없이 두 번 나갈 수 있습니다. 이 두 경로에서 mesh 재시도를 끈다(`retries.attempts: 0`)는 내용을 요구사항이나 배포 runbook 에 적어 두길 권합니다.
>

**판단 — 위험 수용(시연)** · vendor 5xx 는 드물고, 시연은 시연 계정이라 중복 케이스가 생겨도 정리만 하면 된다. mesh 재시도 비활성은 1차 운영 요구사항으로 기록.

**답변**

> 좋은 지적입니다. 이번 시연에서는 업체 5xx 가 드물고 시연 계정으로만 호출해 중복 케이스가 생겨도 정리하면 되는 수준이라, 커넥터 경로의 mesh 재시도 비활성화는 1차 운영 요구사항으로 결정 기록 57번에 남겼습니다. 운영 연동 전에는 core→커넥터, 커넥터→업체 두 경로 모두 재시도를 끄도록 하겠습니다.

## 스레드 104538

- 작성자: 민진우(Thomas) · 위치: `/docs/specs/SRS.md:2624`

**원문**

> From Claude Code review,
> **💡 권장**
>
> 커넥터 전용 최소 권한 DB 계정을 1차로 미루면, 시연 동안 커넥터는 core 와 같은 계정으로 `device`·자격 관련 테이블에 쓰기 권한을 갖습니다. 이 앱은 외부 업체 응답을 파싱하고 인터넷으로 나가는 워크로드라 공격면이 core 와 다릅니다. 둘 중 하나를 권합니다.
> - `device`·`clinic` 읽기와 `alliedstar_*` 읽기·쓰기만 주는 GRANT 가 몇 줄로 끝나면 지금 적용합니다.
> - 미룬다면 Appendix B #57 에 "시연 동안 이 위험을 받아들인다"고 적습니다.
>
> 관련해서, 신규 테이블 두 개(`alliedstar_account_link`·`alliedstar_job`)의 마이그레이션을 어디서 소유하는지(core prisma 스키마인지, 커넥터 앱 쪽인지)도 적혀 있지 않습니다.
>

**판단 — 위험 수용 명시 + 수용** · 시연 동안 같은 DB 계정 사용 위험 수용을 결정 기록 57번에 명시. 마이그레이션 소유 = 기존 Prisma 스키마·migrate 이미지(core 와 같은 경로).

**답변**

> 시연 동안 커넥터가 기존 VTG 앱 DB 계정을 함께 쓰는 위험은 받아들이는 것으로 결정 기록 57번에 명시했습니다(외부 노출 없는 시연용 격리 스택이고 시연 계정만 씁니다). 최소 권한 계정은 1차입니다. 신규 테이블 두 개의 마이그레이션은 별도 소유 없이 기존 Prisma 스키마에 들어가 기존 migrate 이미지가 함께 만든다고 §7.5.8 에 적었습니다.

## 스레드 104539

- 작성자: 민진우(Thomas) · 위치: `/docs/specs/SRS.md:53`

**원문**

> From Claude Code review,
> **💡 권장**
>
> core 의 `apps/core/src/compat/header.middleware.ts` 는 `Vatech-Product`·`Vatech-Version`·`Vatech-Clinic-Id` 를 필수로 요구하고, 제품별 최소 버전 매트릭스(`server-configuration.ts`)를 적용합니다. 이 예외 문단에 VT Edge 의 제품 값(OnePager §8.3.3 에서는 `VT-Edge`)과, 매트릭스에 항목이 없을 때 통과하는지 거절하는지를 적어 주세요. 그러면 11/11 서울 dev 등록 시험에서 이 부분 때문에 막히는 일을 줄일 수 있습니다.
>

**판단 — 수용** · 확인 결과: 헤더 미들웨어는 Product·Version·Clinic-Id 존재를 요구하고, 호환성 매트릭스는 항목이 없는 제품을 건너뛴다(통과). 프록시는 버전 게이트가 없다. §1.2 예외에 `VT-Edge` 와 이 동작을 적음.

**답변**

> 확인했습니다. core 의 헤더 미들웨어는 `Vatech-Product`·`Vatech-Version`·`Vatech-Clinic-Id` 가 있어야 하고, 호환성 매트릭스는 항목이 없는 제품을 건너뛰므로 `VT-Edge` 는 통과합니다. 프록시 요청에는 버전 게이트가 걸리지 않습니다. §1.2 예외 문단에 제품 값 `VT-Edge` 와 이 동작을 적어 두었습니다.

## 스레드 104533

- 작성자: 민진우(Thomas) · 위치: `PR 전체`

**원문**

> From Nemesis(v0.9.5, 🆔mwa0b4d81ku, ⏱1m10s, 🔢231.4k in/6.7k out),
> ## Code Review (Other)
>
> VT Edge 를 v1.0 device 로 받는 예외(§1.2), Alliedstar 커넥터 FR-INT-08(§7.5.8), 결정 기록(Appendix B #57), UnitTCL BR.11, DBML 두 테이블이 한 PR 안에서 함께 추가돼 추적성은 대체로 잘 연결돼 있습니다. 특히 다음 결정들은 근거가 분명하게 서술돼 있습니다.
> - 개발사 자격과 원내 범위 판단을 VTG 쪽에 두는 것
> - 업체 규격 변환을 core 와 분리된 앱으로 두는 것
> - 예약 키를 버리고 빈 값을 서명·전송에서 함께 빼는 것
> - 비기록 대상과 재시도하지 않는 정책
>
> 다만 기존 §7.5.1 의 `internal_bypass` 서술("v1.0 확정 사용처 없음")을 갱신하지 않아 문서 안에서 모순이 생겼습니다. 이는 통제 문서로서 반드시 고쳐야 합니다.
> 그 밖에 보완을 권하는 사항은 다음과 같습니다.
> - ③b 신원 전달 방식(P0 미정)을 Alliedstar 에 한해 먼저 정하는 결정이라는 점을 명시하고, 커넥터에 GW 말고 다른 ingress 가 없도록 하는 요구사항을 추가
> - 원내 범위 보호 대상 API 를 `getCaseDetail` 하나에서 API 별 판단으로 넓히기
> - `result=unknown` 케이스를 나중에 맞추는 방법 정하기
> - 커넥터→업체 timeout 과 VTG target timeout 사이의 관계 정의
>
> 또 §1.2·Appendix B #57 에 적힌 유럽 시연 스택은 운영 Region Directory 에 등록하지 않는다고 했습니다. 그렇다면 그 스택에서 Edge 를 등록·인증하는 경로(§7.1.1·§7.2)와 토큰의 `region` 값을 어떻게 정할지도 runbook 이나 스펙 어딘가에서 다룰 필요가 있습니다.
>
> 6 line-specific finding(s) were posted as inline comments.
>

**판단 — 회신** · 요약. 유럽 스택 Edge 등록 경로는 Region Directory 대신 유럽 VTG 주소를 설정으로 직접 주고, 토큰 `region` 은 그 스택의 `GW_REGION`. 인프라 handoff·runbook 에서 다룸.

**답변**

> 검토 감사합니다. 인라인 지적은 각 스레드에 적은 대로 반영하거나 시연 범위에서의 판단을 남겼습니다. 유럽 시연 스택의 Edge 등록은 운영 Region Directory 를 거치지 않고 Edge 에 유럽 VTG 주소를 설정으로 직접 주는 방식으로 하고, 토큰의 `region` 은 그 스택의 `GW_REGION` 값이 됩니다. 이 내용은 인프라 handoff 문서(`docs/handoff/alliedstar-connector-infra.md`)와 커넥터 runbook 에서 다루고, §7.5.8 에도 한 줄로 남겼습니다.


## 처리 (2026-11-10)

- 반영 커밋: c73c40b(리뷰 반영) · 46bbc4b(§7.5.1 정규식 편집으로 지워진 CleverSpace 근거 문장 복원)
- 13개 스레드 모두 답변(comment 2) · resolve(fixed)
- 구현 확인 요청(GW 세션): 상위 요청이 취소돼도 대장 기록을 마치는지(104530) · 업체 2xx 아닌 응답 시 대장 unknown(104534) · TC-ASC-10 업체 500 케이스

# 2라운드 (2026-11-11) — Claude Code 재리뷰 1건

## 스레드 104682

- 작성자: 민진우(Thomas) · 위치: `/docs/specs/SRS.md:2588`

**원문**

> 🔧 수정 필요 — `#57` 재번호 교차참조 누락
>
> 이번 수정(c73c40b)이 `Appendix B #57` 을 재번호했습니다: ④ = "시연 동안 받아들이는 위험", ⑤ = "1차(2027-01)". 그런데 이 줄은 여전히 "사용자 승인 흐름·연결 해제는 **1차(Appendix B #57 ④)**" 로 ④를 가리킵니다. "사용자 승인 흐름"은 이제 ⑤(1차) 항목이므로 **④ → ⑤** 로 고쳐야 합니다. (통제 문서 추적성 · L2584·L2610·L2629·L2630 은 하위번호 없이 #57 만 가리켜 영향 없음.)
>
> — Claude Code 재리뷰

**판단 — 수용** · 결정 기록 57번 번호를 바꾸면서 생긴 교차참조 누락. ④ → ⑤ 한 글자.

**답변**

> 반영하겠습니다. 결정 기록 57번 번호를 바꾸면서 이 줄의 교차참조를 놓쳤습니다. 사용자 승인 흐름은 1차 항목이므로 ⑤로 고치고, 다른 하위 번호 참조가 남았는지 함께 확인했습니다.

- 2라운드 반영 커밋: ca6316b · 104682 답변·resolve(fixed)
