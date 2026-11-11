# PR 15974 리뷰 대응 — Alliedstar IO 스캐너 연동 OnePager

- PR: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/15974
- 투표: Jack 승인(10) · Scott·Nick 0
- 판단 기준: 시연 1회용 — 문서 정합만 맞춘다

# 1라운드 (2026-11-11) — Jack 1건 · Thomas(Claude Code 재리뷰) 2건

## 스레드 104637

- 작성자: 임건혁(Jack) · 위치: `PR 전체`

**원문**

> @<B62326D5-BE2F-6C22-BDD5-19CE8D112C90> cc. @<E616BABA-1CD7-6573-A367-AFAF4633BD3C> 인프라 요청 문서 업데이트 확인했고 이견 없습니다. 유럽 지역 리전 (독일) 코드는 euc1 (eu-central-1) 사용 예정입니다.
> 또한 이번에 환경변수 관련하여 Parameter Store에 들어가던 설정값을 별도의 시크릿 매니저로 (dev/vt-api-gateway-core/config) 제가 이관해두었고 이 PR이 머지되면 제가 문서 수정 PR 올려두겠습니다.
>

**판단 — 수용(회신)** · 유럽 리전 코드 euc1 확정 · 설정 저장 위치가 Secrets Manager 로 이관. handoff B7·B8 과 OnePager 의 `<eu-region>` 을 euc1 로, handoff A5 설정 위치를 Secrets Manager `…/config` 로 고친다. 커넥터 설정 경로(`dev/vt-api-gateway-alliedstar-connector/config`)는 Jack 확인 요청.

**답변**

> 확인과 승인 감사합니다. 유럽 리전 코드 euc1 을 인프라 요청 문서(B7·B8)와 OnePager 에 반영했습니다. 설정값을 Secrets Manager 로 옮기신 것에 맞춰 A5 의 위치 표기도 Parameter Store 에서 Secrets Manager 로 고쳤습니다. 커넥터 설정도 같은 방식으로 dev/vt-api-gateway-alliedstar-connector/config 에 두면 되는지만 확인 부탁드립니다. env-reference 쪽 정리는 말씀대로 머지 후 올려 주시는 PR 로 맞추겠습니다.

## 스레드 104683

- 작성자: 민진우(Thomas) · 위치: `/docs/onepager/alliedstar-io-scanner-onepager-2026-11-09.md:241`

**원문**

> 💡 수정 권장 — SRS 업무 API 표와 동기화
>
> 스펙 PR 15997(c73c40b)이 이 표에 대응하는 SRS §7.5.8 표를 개정했습니다: ① **원내 범위** 열 추가, ② `getCaseDetail`(openid 없이 caseCode) 를 별도 "케이스 조회" 행으로 분리, ③ 업체 경로 표기를 앞 `/` 없는 `open/...` 로 통일. OnePager 는 #57 의 *근거 문서* 라 두 통제 문서가 어긋나면 정합이 깨집니다. 이 표를 개정된 SRS 표 구조에 맞춰 주세요. (경로 표기·openid 범위 세부는 PR 15997 에서 이미 확정 — 여기선 동기화만.)
>
> — Claude Code 재리뷰

**판단 — 수용** · 스펙 PR 15997 개정(원내 범위 열·getCaseDetail 분리·open/... 표기)과 OnePager §8.3.2 표를 맞춘다. 같은 김에 §8.3.3·§8.5 의 egress 서술도 스펙과 맞춘다(현재 클러스터 egress 미제한 → 시연은 host 설정 고정).

**답변**

> 반영했습니다. §8.3.2 표를 스펙 §7.5.8 표 구조에 맞춰 원내 범위 열을 넣고, getCaseDetail 을 케이스 조회 행으로 분리했으며, 업체 경로 표기를 앞 / 없는 open/... 로 통일했습니다. 같은 이유로 §8.3.3 과 §8.5 의 egress 서술도 스펙과 맞췄습니다(현재 클러스터는 egress 를 제한하지 않아 시연은 호출 host 를 설정으로 고정).

## 스레드 104684

- 작성자: 민진우(Thomas) · 위치: `/docs/onepager/alliedstar-io-scanner-onepager-2026-11-09.md:50`

**원문**

> 🔧 수정 필요 — "1차/2차" 가 문서 안에서 두 뜻
>
> 이 줄은 9/28 킥오프 기준 "**1차** = 촬영 실행 · **2차** = EzServer 저장" 입니다. 그런데 문서 전반(§4 L43 · §7 L85~86 · §8)은 **시연 = 촬영 실행**, **1차(2027-01) = 결과 수집**, **2차(2027-Q2) = EzServer 저장** 으로 씁니다. 같은 "1차"가 L50 에선 촬영 실행, L85 에선 결과 수집을 가리켜 승인자가 단계 약속을 오독할 수 있습니다. 킥오프의 1차(촬영)가 이 문서에서 **시연 + 1차(결과 수집)로 쪼개졌다**는 단서를 붙이거나 번호를 문서 전반과 맞춰 주세요.
>
> — Claude Code 재리뷰

**판단 — 수용** · 킥오프의 1차(촬영 실행)가 이 문서에서 시연 + 1차(결과 수집)로 나뉘었다는 단서를 L50 에 붙이고, §7 일정표 2027-01 행("1차 — 실제 촬영 Case 요청")도 "1차 — 촬영 결과 수집"으로 고친다.

**답변**

> 반영했습니다. 킥오프의 1차(촬영 실행)가 이 문서에서는 이번 시연과 1차(촬영 결과 수집)로 나뉘었다는 단서를 해당 줄에 붙였고, 일정표의 2027-01 행도 "1차 — 촬영 결과 수집"으로 고쳐 문서 전반의 번호와 맞췄습니다. 2차(EzServer 저장)는 그대로입니다.

## 처리 (2026-11-11)

- 반영 커밋: 93fcd76(OnePager·인프라 handoff)
- 104683·104684 답변·resolve(fixed) · 104637 답변(커넥터 설정 경로 질문 남아 열어 둠)
