# PR 15934 리뷰 — Alliedstar API 대응과 검증 범위 정리

| 항목 | 내용 |
| --- | --- |
| PR | [15934](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/15934) · `tasks/ESIP-38-alliedstar-api-handoff` → main (분기 `6ccff84`) |
| 작성 | Scott |
| 변경 | `docs/handoff/alliedstar-edge-integration.md` r1 → r2 (+21 −10) — 업무 API 15개 대응표 · 공개 테스트 조회 결과 |
| 검토일 | 2026-11-09 |
| **판단** | **승인(제안 포함)** — Draft handoff 정리로는 충분하다. 단 1·2번은 **커넥터 구현 전에 문서에서 바로잡아야** 한다 |

## 확인한 것 (업체 공식 문서 대조 — API List·Security, 2026-11-09 내려받음)

- 대응표 15개 경로가 업체 API 목록과 일치한다. 공식 호출 16개 중 `createUser` 를 원내 제공에서 뺀 것은 맞다 — 이 API 는 사용자 승인(`openid`) 없이 개발사(`appid`) 자격만으로 계정을 만든다.
- 콜백 2개(스캔 결과·주문 정보)를 원내가 아닌 GW 가 받는다 — 방화벽 뒤 원내에 공개 포트를 만들지 않는 GW 원칙과 같다.
- 공개 테스트 자격으로 `listCases` 정상 서명 200·변조 서명 40002 를 확인했고, 그 범위(배포 GW 아님·listCases 전용)를 정직하게 적었다.

## 짚을 것

1. **문서 본문은 GW 주소 `/v1/alliedstar/…` 를 계약처럼 읽히게 적었다 — 의도(모의 GW)와 표현이 어긋난다.**
   - **Scott 의 의도는 우리와 같다.** PR 설명은 "Edge `/v1/scanners/alliedstar` 및 **모의 GW** `/v1/alliedstar`"라고 적고, "동일한 URL 을 강요한다는 의미가 아니라 업무별 1:1 대응을 명확히 하는 목적"이라고 밝혔다.
   - 그런데 문서 본문 첫 문단은 "Edge `/v1/scanners/alliedstar` 와 **GW `/v1/alliedstar`** 뒤에 업무 경로를 붙인다"를 최초 v1 계약으로 적는다.
   - GW 는 **GW 고유 API**와 **target 프록시**를 나눈다(ADR-11). target 프록시는 **호스트(서브도메인)로 연동 대상을 고르고**(예 `axs.<region>.gw.<도메인>`) 경로는 그대로 전달한다. 연동 대상을 붙일 때 GW 에 업체 이름의 경로를 새로 만들지 않는다.
   - 같은 문서도 "자사 커넥터를 internal target 으로 등록 · common proxy 에 vendor 분기를 추가하지 않는다"를 추천한다. 그러면 Edge → GW 계약은 `<커넥터 target>.<region>.gw.<도메인>` + 업무 경로이고, `/v1/alliedstar` 는 **모의 GW 주소**로만 남아야 한다.
   - 제안: 본문 첫 문단도 PR 설명처럼 "모의 GW"로 적고, 실제 GW 계약은 커넥터 target 호스트로의 프록시라고 한 줄 덧붙인다. 한 단어 수정 수준이다.
2. **Alliedstar 에도 "연동사 단위 API"가 있다 — Target Policy 와 같은 문제다.**
   - 업체 인증은 개발사 자격(`appid` + RSA2 키) 하나이고, 어느 사용자(원내) 범위인지는 요청의 `openid` 로 정한다. 그런데 다음 API 는 `openid` 로 범위가 갇히지 않는다.

     | API | 범위 | 원내가 호출하면 |
     | --- | --- | --- |
     | `getCaseDetail` | `caseCode` 만 받는다(`openid` 없음) | **다른 원내의 케이스 상세(환자 정보)** 를 caseCode 로 조회 |
     | `listOrders` | `openid` 선택 · `unionid`(조직)만으로도 조회 | `openid` 를 빼고 다른 조직을 지정하면 그 조직 주문 조회 |
     | `toothsplit` | `openid` 없음 · 임의 클라우드 주소 입력 | 개발사 자격으로 업체 서비스 사용(과금·남용) |
     | `createUser` | `openid` 없음 | 이미 원내 제공에서 제외 |

   - `openid` 를 쓰는 API 도 **`openid` 를 Edge 입력으로 받으면** 다른 원내의 `openid` 를 넣어 범위를 넘을 수 있다.
   - 문서에 "외부 계정·key·host 를 Edge 입력으로 받지 않음"이 있으나 `openid`·`unionid` 는 명시돼 있지 않다.
   - 제안: 커넥터 원칙에 세 줄을 넣는다 — (가) `openid`·`unionid` 는 **검증된 device → clinic 의 계정 연결에서 커넥터가 넣고 Edge 입력값은 버린다** (나) `openid` 없이 `caseCode` 로 조회하는 API(`getCaseDetail`)는 **그 원내가 만든 케이스인지 job 대장으로 확인한 뒤**에만 호출한다 (다) `toothsplit` 은 필요가 확인되기 전까지 원내 제공에서 뺀다.
3. **콜백 수신은 GW 신규 기능이다.** 현재 GW 수신부는 HMAC 계열 서명만 검증한다. Alliedstar 콜백은 JSON 본문 안의 `sign` 을 업체 공개키로 검증하는 RSA2 방식이고, `site` 헤더(cn·eu·uk·us·jp·global)로 지역을 알려 준다. 수신자 결정은 `userOpenid` → 원내 연결로 해야 한다. 또 응답은 HTTP 202 가 아니라 업무 `code=200` JSON 이어야 하고, 콜백에 독립 이벤트 ID 가 없어 중복·재스캔을 가를 규칙이 필요하다(COMM-1841 기술 검토와 같은 결론). GW 쪽 과제로 가져간다.
4. **환자 정보의 리전 경계.** `createPatient`·`createCase` 는 환자 이름·생년월일을, 콜백은 환자 이름·사용자 이메일·전화를 싣는다. 유럽 원내 요청은 **eu site 엔드포인트로만** 나가야 한다(GW PHI 리전 경계). "site 별 outbound host·region binding" 항목에 이 이유를 적어 두면 좋겠다.
5. (경미) "최신 Target Policy 문서는 구현 계획을 포함한다. 실제 코드의 집행 완료를 가정하지 않는다" — Target Policy 스펙은 11/05 승인·머지됐고 구현은 이번 주 마무리 예정이다. 위 2번의 `toothsplit`·`createUser` 차단은 Target Policy 규칙으로도 걸 수 있다.

## 리뷰 코멘트 초안 (PR 전체 코멘트·복사용)

```
대응표 15개 경로가 업체 공식 API 목록과 맞고, createUser 를 원내 제공에서 뺀 판단과 콜백을 GW 가 받는 구조도 맞습니다. 공개 테스트 결과의 범위도 정확히 적어 주셨습니다. Draft 정리로 승인하고, 커넥터 구현 전에 문서에서 바로잡았으면 하는 점 두 가지와 GW 쪽으로 가져갈 점을 적습니다.

첫째, PR 설명에는 /v1/alliedstar 가 모의 GW 주소이고 같은 URL 을 강요하는 뜻이 아니라고 적어 주셨는데, 문서 본문 첫 문단은 "GW /v1/alliedstar"라고만 되어 있어 실제 GW 계약으로 읽힙니다. GW 는 GW 고유 API 와 target 프록시를 나누고, target 프록시는 호스트(서브도메인)로 연동 대상을 고른 뒤 경로를 그대로 전달합니다. 연동 대상마다 GW 에 업체 이름의 경로를 만들지 않습니다. 문서 자체도 커넥터를 internal target 으로 두고 공통 프록시에 업체 분기를 넣지 않는 안을 추천하고 있으니, 본문도 PR 설명처럼 모의 GW 로 적고 실제 계약은 커넥터 target 호스트로의 프록시라고 한 줄 덧붙여 주시면 좋겠습니다.

둘째, 업체 공식 문서를 대조해 보니 AXS 의 webhook 구독과 같은 연동사 단위 API 가 Alliedstar 에도 있습니다. getCaseDetail 은 openid 없이 caseCode 만 받아서 개발사 자격이면 다른 원내의 케이스 상세를 조회할 수 있고, listOrders 는 openid 없이 unionid 만으로도 조회되며, toothsplit 도 openid 없이 개발사 자격으로 호출됩니다. 또 openid 를 받는 API 도 openid 를 Edge 입력으로 받으면 다른 원내의 값을 넣을 수 있습니다. 커넥터 원칙에 openid 와 unionid 는 검증된 device 의 원내 계정 연결에서 커넥터가 넣고 Edge 입력값은 버린다, caseCode 로 조회하는 API 는 그 원내가 만든 케이스인지 job 대장으로 확인한 뒤에만 호출한다, toothsplit 은 필요가 확인되기 전까지 원내 제공에서 뺀다는 세 줄을 넣어 주시면 좋겠습니다. 막아야 할 경로는 GW 의 Target Policy 규칙으로도 걸 수 있습니다.

GW 쪽으로 가져갈 것도 적어 둡니다. Alliedstar 콜백은 본문 안의 sign 을 업체 공개키로 검증하는 RSA2 방식이라 HMAC 만 지원하는 현재 GW 수신부에 새 검증 방식이 필요하고, 수신자는 userOpenid 로 원내를 찾아야 합니다. 응답 형식(업무 code 200)과 독립 이벤트 ID 가 없는 콜백의 중복 판정 규칙도 함께 설계하겠습니다. 또 환자 정보가 오가므로 유럽 원내 요청은 eu site 엔드포인트로만 나가도록 리전 경계를 GW 에서 지키겠습니다.
```
