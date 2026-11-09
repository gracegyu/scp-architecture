# PR 15931 리뷰 — EzServer·Edge 직접 연결 공존과 전환 원칙

| 항목 | 내용 |
| --- | --- |
| PR | [15931](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/15931) · `tasks/ESIP-37-direct-client-handoff` → main (분기 `6ccff84`) |
| 작성 | Scott |
| 변경 | `docs/handoff/ezserver-edge-direct-clients.md` 신설(55줄) · `scripts/dev-enroll.sh` 주석 정정 |
| 검토일 | 2026-11-09 |
| **판단** | **승인(제안 포함)** — 방향은 GW 설계와 맞는다. 제안 3건은 머지를 막지 않는다 |

## 확인한 것

- **1:N 모델과 맞다.** GW SRS 는 `clinic ↔ device` 를 1:N 으로 정의하고(§1.2·용어·Appendix B 47번), 현재 `/v1/enroll/complete` 는 같은 clinic 이어도 매번 새 pending device 를 만든다. 문서의 "Edge 등록만으로 기존 EzServer 의 키·토큰·인증서를 교체하지 않는다"는 main 동작과 같다.
- **`dev-enroll.sh` 주석 정정이 맞다.** 예전 주석은 "같은 CLINIC_ID 면 기존 device 를 회전시켜 빼앗는다"였는데, 회전 경로는 이미 없어졌다(main `enroll-complete.service.ts` — 옛 인증서를 폐기하지 않는다). 런타임 변경 없음.
- **권한 근거가 옳다.** "인증된 device 로 clinic 을 확인하고 제품명 헤더·본문 clinicId 를 권한 근거로 삼지 않는다"는 GW 원칙(device 기준 해석·§6.4.1) 그대로다.
- **MQTT 중복 수신을 정확히 짚었다.** Dispatcher 는 clinic 토픽(`gw/clinic/{clinicId}/webhook`)으로 발행하므로 두 기기가 모두 구독하면 같은 이벤트를 받는다.

## 짚을 것

1. **GW 스펙 범위가 바뀌는 결정이다.** GW SRS 는 지금 "v1.0 의 device = EzServer 뿐"이고 비-EzServer device 는 Will Not Do 다(§1.2). Edge 를 GW device 로 받는 것은 이 범위를 여는 결정이라 GW 스펙(결정 기록)에 올려야 한다. 이 문서는 Draft handoff 로 두고, 스펙 반영은 GW 쪽에서 가져간다.
2. **운영자가 같은 원내의 두 기기를 구분할 수 없다.** `device` 테이블에는 제품 정보가 없다(`Vatech-Product` 는 `client_inventory` 에만 남는다). 같은 clinic 에 EzServer 와 Edge 가 있으면 Console 기기 목록에서 둘이 구분되지 않아, 검증 조건 3("한 기기만 폐기")을 운영자가 실제로 수행할 때 **엉뚱한 기기를 폐기할 위험**이 있다. GW 과제(등록 시 제품을 device 에 남기고 Console 에 표시)로 가져간다.
3. **SRS 의 다중 기기 해법이 Edge 에는 맞지 않는다.** SRS §7.6.6 은 한 clinic 에 EzServer 가 여러 대일 때 shared subscription(`$share/ezserver/…`, 한 대만 수신)을 해법으로 적고 있다. 이 해법은 "같은 일을 하는 기기 중 아무나 하나"를 전제로 한다. EzServer 와 Edge 는 맡는 기능이 다르므로 같은 그룹에 넣으면 엉뚱한 쪽이 받고, 다른 그룹이면 둘 다 받는다. 문서의 "별도 설계 게이트"에 이 점을 적어 두면 좋겠다 — 기능(이벤트 종류)별 수신자를 GW 가 정해야 한다.
4. (경미) "ESIP-30" 은 GW 저장소 독자가 찾을 수 없다. 링크나 한 줄 요약을 붙이면 좋겠다.

## 리뷰 코멘트 초안 (PR 전체 코멘트·복사용)

```
방향에 동의하며 승인합니다. 1:N 등록과 dev-enroll.sh 주석 정정은 현재 main 동작과 맞고, 권한 근거를 인증된 device 로만 두는 원칙도 GW 설계와 같습니다.

몇 가지는 GW 쪽에서 이어받겠습니다. 첫째, GW SRS 는 지금 v1.0 device 를 EzServer 로 한정하고 있어서 Edge 를 GW device 로 받는 것은 스펙 범위를 여는 결정입니다. 이 문서는 Draft 로 두고 GW 스펙 결정 기록에 따로 올리겠습니다. 둘째, device 테이블에 제품 정보가 없어 같은 원내의 EzServer 와 Edge 를 Console 에서 구분할 수 없습니다. 한 기기만 폐기하는 운영을 하려면 등록 시 제품을 device 에 남기고 화면에 보여야 해서 GW 과제로 가져가겠습니다.

문서에 하나만 더 적어 주시면 좋겠습니다. SRS 는 한 원내에 EzServer 가 여러 대일 때 shared subscription 으로 한 대만 받게 하는 것을 해법으로 적고 있는데, 이는 같은 일을 하는 기기 중 아무나 하나를 고르는 방식이라 맡는 기능이 다른 EzServer 와 Edge 에는 맞지 않습니다. 결과 수신 이전의 설계 게이트에 "기능별 수신자를 GW 가 정해야 한다"는 점을 함께 적어 두면 후속 설계가 같은 함정에 빠지지 않을 것 같습니다. 그리고 ESIP-30 은 이 저장소에서 찾을 수 없어 링크나 한 줄 요약을 붙여 주시면 좋겠습니다.
```

## GW 후속 (OnePager 반영)

- Edge 를 GW device 로 받는 범위 결정 → GW SRS 결정 기록
- device 에 제품 기록 + Console 표시
- 기능별 수신자(이벤트 → 기기) 설계 — 1차 이후
