# Thomas 문의

- ⭐ (GW 종합 검토 · 권고: B안 — GW 경유)
  - ⚠️ **전제 한계 — Dentbird API 문서 미확인 (중요)**: `docs.dentbird.com`은 현재 **랜딩/목차 페이지만 공개**되어 **인증 방식·webhook 스펙·업로드 방식을 확인하지 못했다.** 아래 분석과 B안 공수 추정은 **미확인 가정** 위에 있으며, **Dentbird 상세 API 문서(또는 이마고웍스 기술 확인) 확보 후 반드시 재확정**해야 한다.
  - 현 설계 = **A안(직접·GW 비경유)**: [Link]로 Dentbird 웹 직접 가입/구독(ES referral 정산) → 이마고웍스가 credential 발급 → 고객이 Clever One에 직접 입력 → Clever One이 Dentbird API 직접 호출.
  - 권고 = **B안(Clever One → EzServer → GW → Dentbird 경유)**. 근거 두 축:
    - 정책: Scott/ES 기본 정책 = **밖으로 나가는 모든 정보는 GW 경유** → A안은 위반.
    - 기술(결정적): Dentbird webhook은 온프렘 클라(공개 inbound 없음)가 못 받는다 → **GW 공개 수신 + MQTT 하향만 가능** → B안 사실상 강제.
  - 경계 조정: 가입/구독 [Link] 브라우저 흐름은 **계정 provisioning**이라 **직접 유지**(referral 보존), **케이스 데이터·credential만 GW로**.
  - 실현성: **AXS target 모델 재사용**이라 난이도 **중**. 신규 = per-clinic 자격 custody(인증 모델에 따라) · 대용량 케이스 파일 프록시 · Clever One 경유 전환.
  - A vs B 비교:

    | 항목 | A안 (직접·현 시나리오) | B안 (GW 경유) ← 권고 |
    | --- | --- | --- |
    | ES 정책(모든 outbound GW) | 위반 | 부합 |
    | webhook 수신 | 불가(온프렘 공개 inbound 없음 → polling만) | GW 공개 수신 → MQTT로 온프렘 push |
    | 보안 거버넌스(egress·감사·정책) | 없음(GW 밖) | 중앙 chokepoint |
    | credential 위치 | Clever One 클라(client-side secret) | GW(KMS custody) |
    | PHI 규제(IEC 62304/ISO 13485) | 거버넌스 밖(위험) | 거버넌스 안 |
    | 구현 공수 | ~0(product 기설계) | 중(Clever One 재작업 + per-clinic 자격 + 대용량 + EzServer) |
    | GW팀 운영 부담 | 없음 | 있음(크리티컬 패스) |
    | 대용량 케이스 파일 | 직접(성능 자유) | GW 프록시 부담 → presigned 검토(§4.1.4) |
    | referral 정산 | 자연 | signup 직접 유지 시 동일 |
    | 기존 자산 재사용 | — | AXS target 모델 대부분 재사용 |

  - 확정 필요(B안 공수·설계 확정용):
    - Dentbird 인증 모델 — 파트너/OAuth(Vatech=integrating entity·per-clinic link·AXS 동형 → 쉬움) vs per-customer API key(clinic마다 구독 → per-clinic 자격 custody 필요). ← B 난이도를 가름.
    - webhook 스펙 — 제공 이벤트·인증(HMAC secret 등)·payload의 org/clinic 식별 필드.
    - 업로드(케이스 파일) 방식·크기 — GW 프록시 vs presigned.
    - ⚠️ **위 3항목은 Dentbird API 문서를 확인하지 못해 전부 미확정이다** — `docs.dentbird.com`은 랜딩/목차만 공개. 상세 섹션 접근 또는 이마고웍스 기술 확인이 **선결**이며, 그 전엔 B안 공수·설계가 확정 불가.
  - 정본:
    - 신규 target 온보딩 runbook — https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/manual/target-onboarding.md
    - GW SRS — https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/specs/SRS.md

- Dentbird 연동시 고려사항
  - 연동 시나리오 (TBD): https://vatechcorp-my.sharepoint.com/shared?listurl=%2Fpersonal%2Fjoy%5Fshin%5Fewoosoft%5Fcom%2FDocuments&viewid=ebc8906e%2Db3a2%2D4150%2D84e5%2Df8bbdebbc451&ga=1&id=%2Fpersonal%2Fjoy%5Fshin%5Fewoosoft%5Fcom%2FDocuments%2FJoy%5FOneDrive%2F14%2E%20%ED%95%B4%EC%9E%90%2F7%2E%20%EC%9D%B4%EB%A7%88%EA%B3%A0%EC%9B%8D%EC%8A%A4%2F%5BES%2D%EC%9D%B4%EB%A7%88%EA%B3%A0%EC%9B%8D%EC%8A%A4%5D%5F20260416%5FClever%20One%5FDentbird%20%EC%97%B0%EB%8F%99%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4%2Epdf&parent=%2Fpersonal%2Fjoy%5Fshin%5Fewoosoft%5Fcom%2FDocuments%2FJoy%5FOneDrive%2F14%2E%20%ED%95%B4%EC%9E%90%2F7%2E%20%EC%9D%B4%EB%A7%88%EA%B3%A0%EC%9B%8D%EC%8A%A4
  - 연동 관련 문서 (Dentbird): https://docs.dentbird.com/dentbird-partner-integration-guide.html
  - 1. Account의 credential을 넣게 되어 있는데, Dentbird에 전달 방안?
    - API 대한 정보가 정확하지 않아 어떻게 전달하는지는 모르나 header를 통해 전달하지 않을까 추측
    - EzServer enrollment 과정에서 credential을 설정할 수도 있지 않을까?
    - EzServer에서 넣어야 한다면 EzServer 수정 필요
      - ➡️ (B안 기준) credential은 **GW target 자격**으로 두고 **KMS custody + GW가 아웃바운드 주입**(§7.5.1). 고객이 이마고웍스에서 받은 자격을 **Clever One 클라이언트가 아니라 GW에 등록**한다(운영자 Console 또는 self-plane). EzServer는 `Vatech-Target`만 붙이고 자격은 GW가 얹는다(EzServer에 credential 안 넣음 — 경계 혼선 회피).
        - 확정 필요: 인증 방식(OAuth2 vs 정적 API key — 후자면 Connector 정적 주입 지원 확인) · 스코프(target 단위 vs per-clinic → per-clinic이면 org_binding 수준 secret custody 신규).
  - 2. Dentbird가 Webhook을 제공하는 데, 이를 CleverOne에서 받을 방법은?
    - EzServer가 VAG MQTT에서 받은 메시지를 그대로 MQTT로 C1에 전달하면 될까?
      - ➡️ (B안 기준) **Dentbird → GW 공개 webhook 수신·검증·payload 저장 → dispatcher → MQTT(IoT Core)로 해당 clinic의 EzServer → Clever One**(§7.6). 그린 대로 "EzServer가 MQTT로 받아 C1 전달"이 이 경로의 마지막 홉이다. **A안(직접)으로는 온프렘 클라에 공개 inbound가 없어 webhook 수신 불가**(polling 우회만) → 이 요구가 B안을 사실상 강제한다.
        - 확정 필요: webhook payload의 org/clinic 식별 필드(org_mapping 키) · webhook 인증(HMAC secret 등).
- 다중 target (AXS, CleverSpace, Dentbird, Pearl 등) 연동 방안
  - 하나의 clinic에 대해서 EzServer와 VAG가 연동되면 해당 region의 모든 target 에 대해서 연동이 가능한 상태가 되는가?
    - ➡️ 아니오. enrollment(device active)는 GW **연결만** 여는 것이고, 실제 target 연동은 **target별 org_binding + 자격**이 있어야 한다(target별 opt-in · §7.5 · org_mapping 생애주기). "모든 target 자동 연동"이 아니다.
  - clinic 별로 target 연동을 달리한다면 켜고 끄는 것을 어디서 하는가? VAG GW console, EzServer Web Console?
    - EzServer WebConsole에서 한다면 target 목록을 받을 수 있는 API를 VAG가 제공해야 한다.
    - on/off 외에 추가 정보(credential 등)이 있다면 이것도 API 에 포함되어야 한다.
      - ➡️ 정책 결정 — **운영자(GW Console org-mapping 화면)** vs **고객(EzServer self)**. 고객 self로 하려면 "clinic이 붙을 수 있는 target 목록 조회" **self-plane discovery API가 신규로 필요**(현재 없음 · 8/4 유보 항목). credential까지 self로 받으면 self 평면 secret 제출 경로도 설계 대상. **on/off 주체를 먼저 정해야** 신규 API 필요 여부가 갈린다.
- 신규 target 추가시 VAG에 등록 절차
  - 어떤 VTS 이슈로 생성? ESIP?
  - target 등록용 이슈 생성 template 이 있음 좋겠음.
    - target 명
    - dev endpoint
    - production endpoint
    - webhook url
    - api 문서 url
  - ➡️ GW는 신규 target = **레지스트리 1행 추가**(코드·경로 변경 없음). template 채택 권장 + GW 필수 필드 추가: **아웃바운드 인증 방식 · 인바운드 webhook 인증 · org 식별 방식**. 절차는 **신규 target 온보딩 runbook**([docs/manual/target-onboarding.md](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/manual/target-onboarding.md) · Azure DevOps Wiki publish)에 정리해 두었다.

- ℹ️ (참고) org_mapping 은 언제 생기나 — 헷갈리는 지점 정리
  - 한 줄 요약: 클리닉이 그 연동을 **"켤 때" 딱 1건** 생긴다. **최초 데이터(프록시) 요청 때 자동으로 생기는 게 아니다.**
  - 생기는 지점: EzServer가 GW로 보내는 `POST /v1/clinics/me/org-bindings`(= "이 연동 켜기" 등록 요청) 1건 → GW DB에 (외부 Org-ID ↔ clinic) **한 행** 기록. 이때 외부 target(AXS·Dentbird)은 **호출하지 않는다**(순수 GW 로컬 기록).
  - "그럼 target으로 첫 요청 올 때 생기나?" → 아니다. 실제 프록시/webhook 요청은 이 매핑이 **이미 있다고 전제**한다.
    - 왜 미리 있어야 하나: org_mapping은 **양방향 키**다. ① 인바운드 webhook은 대상이 "외부 Org-ID"로 보내오므로 "이게 어느 clinic이냐"를 이 매핑으로 되짚어야 분배되고, ② 아웃바운드는 그 clinic의 Organization-ID 주입에 쓴다. 요청만으로 "어느 조직 = 어느 clinic"을 안전하게 확정할 수 없어(신뢰·동의) 미리 등록한다.
  - 헷갈리는 **세 행위**를 분리하면 명확해진다:
    - ① device enrollment(승인·active): GW와의 **연결만** 연다. target 연동과 무관.
    - ② org_mapping 등록(로컬): `POST /v1/clinics/me/org-bindings` → GW DB 1행. **← org_mapping이 생기는 유일한 지점.** target 미호출.
    - ③ 외부 연동 링크(원격): 대상 쪽에 실제로 연결(예: AXS `link` API 호출·별도 프록시 호출). ②와 **별개 행위.** (Dentbird는 이런 원격 "연결" 호출이 있는지 확정 필요 — 없으면 ②만으로 끝.)
  - 순서 예 (AXS 기준·클리닉 케이스, A안/B안과 무관): (i) 이미 연동(organizationId 보유) = ②만 · (ii) Straumann 고객·미연동 = ③(`link`)로 organizationId 획득 → ② · (iii) 비-Straumann = Straumann 고객가입(수동) 선행 → (ii)로 수렴.
