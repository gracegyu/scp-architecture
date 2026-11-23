# VT API Gateway — 11/26 주간회의 Agenda

> 순서: **1. R1 하행 JetStream 채널 추가** → **2. AXS 조직 연결 스펙(PR 16269)** → **3. Enrollment 일회용 승인 링크(PR 16272)** → 4. Alliedstar ADF 시연 마무리 → 5. 공유
>
> 이전 주차 내용은 `주간회의-Agenda-Archive.md`(11/19 = Alliedstar 원인 분석·조치 경과 · 설계 요점 · 문서 목록 · JetStream 결정 경과).
>
> 11/19 오후까지의 진행을 반영해 시작했다. Jack 11/24~27 휴가.

- 🔴 **이번 회의에서 결정·확인할 것**
  - 하행 JetStream OnePager PR 16267 — 승인 여부(11/23 목표) · 다음 단계(SRS 스펙 PR) — 1장
  - AXS 조직 연결 스펙 PR 16269 — 리뷰 · Straumann 답 · EzServer 필요 시점 — 2장
  - Enrollment 일회용 승인 링크 OnePager PR 16272 — 받아들이는 위험 · 리뷰 — 3장
  - ADF 시연 결과 · 시연 뒤 할 일(유럽 스택 IP 제한 · 1차 범위) — 4장

- **지난 회의(11/19) 결정 추적**

  > 11/19 회의 결정은 Agenda 에 기록되지 않았다 — 아래는 11/19 오후까지 확인된 상태다. 회의에서 빠진 결정을 채운다.

  | 11/19 항목 | 담당 | 상태 |
  | --- | --- | --- |
  | AS Connect 앱 로그인 · Launch | Nick | ✅ 11/19 13:25 — hosts 두 줄로 케이스 생성 → AS Connect 실행 확인 |
  | createCase 실패 · 503 | Jack · Raymond | ✅ 서울 dev 케이스 생성 성공(11/19 13:25) |
  | 커넥터 수정(응답 없는 IP 건너뛰기) | 구현 세션 → Jack | ✅ PR 16264 머지 · 서울 dev·유럽 배포(Jack · 11/19) |
  | Console target 시간 제한 응답 40초·전체 45초 | Raymond | ✅ 서울 dev·유럽(11/19) |
  | 커넥터 `ALLIEDSTAR_VENDOR_TIMEOUT_MS`=38000 | Jack | ✅ 서울 dev·유럽(11/19 14:33) |
  | Edge 요청 시간 제한 50초 이상 | Scott | 확인 |
  | 업체에 장애 보고(로드밸런서 IP 2개) | Scott | 영문 보고문 준비됨 · 전달·답 확인 |
  | 유럽 Edge enroll → 승인 | Scott | ✅ 11/19 16:27 — 유럽용 Edge 패키지(VT-Edge-Europe-0.3.3-euc1-adf.1-r2)로 유럽 VAG 연결·승인 확인(Console 감사 로그) · 패키지 Nick·Owen 공유 |
  | 유럽 계정 연결 | Jack | ✅ 들어가 있음(11/19 16:39 확인 · Scott 계정 openid 맞음) |
  | 유럽 케이스 생성 → AS Connect 실행 실측 | Nick | 11/19 시험 요청 — Scott 유럽 Edge 패키지(enroll 된 기기 정보 주입 · 새 enroll·승인 불필요) · 결과 확인 |
  | 리허설(11/20) · ADF 기간 유럽 인프라 담당 | Scott | 확인 |
  | Raymond 부재 중 Console 승인 | Scott · Jack | ✅ 둘 다 Admin — 유럽 Console 기기 승인 가능 |
  | 하행 JetStream OnePager PR — 11/19 올림 · 11/23 승인 | Scott · Jack · Thomas | 1장 |

---

## 1. 📌 R1. 하행(GW → 원내)에 NATS JetStream 채널을 추가한다 — MQTT 와 함께 지원

- **OnePager PR 16267**(11/19) — https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/16267
  - 필수 승인 = Scott · Jack · Thomas = EzServer 확인(선택 리뷰어)
  - 11/23(월) 승인 목표(Jack 휴가 전) — 결과 확인
- 리뷰에서 답할 것(OnePager 8.8)
  - Scott — 기기별 채널 · MQTT·JetStream 함께 지원 · 리전 설정으로 세 경우 지원 확정 · 첫 리전 순서
  - Jack — NATS 운영 방식 = EKS 자체 운영 · 운영 주체·on-call·서명 키 보관 · 규모 가정과 노드 규격·대략 비용
  - Thomas — EzServer v6.6.0 이 운영에서 하행을 켜는지 · EzServer JetStream 전환 시점(OnePager 6.1 리스크와 연결)
- 설계 요지
  - 기기마다 채널 하나 — 기기가 지원 채널을 알리고 VAG 가 정한다 · 알리지 않으면 MQTT
  - VT Edge 는 항상 JetStream · EzServer 는 버전에 따라 MQTT 또는 JetStream
  - 알림은 병원마다 그 병원 기기가 쓰는 채널에만 채널당 한 번 보낸다 · 본문은 두 채널이 같다
  - 스트림은 리전당 하나 · 병원 구분은 subject 의 clinicId · consumer 는 기기마다 VAG 가 자동 생성·삭제 · 보관 14일
  - NATS 는 회사 정책(인프라는 모두 AWS)에 따라 EKS 자체 운영
- 다음
  - 승인되면 미리 써 둔 SRS 초안(11/17)을 OnePager 기준으로 고쳐 스펙 PR — 버전 spec-v1.5.0(1.4.0 은 AXS 조직 연결)
  - 인프라 — NATS 클러스터 구성 요청(handoff) · Jack 복귀 뒤

---

## 2. AXS 조직 연결 — VAG 가 Org-ID 등록 중에 `link` 호출 (Thomas 안건 11/19)

- 계기
  - Thomas 안건 — 카탈로그 AXS 입력란에 Straumann 고객번호(`customerNumber`) 추가
  - 검토 중 결함 발견 — 기존 설계대로면 `link` 가 Org-ID 등록 전이라 VAG 에서 403 으로 막힌다
- **스펙 PR 16269**(spec-v1.4.0) — https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/16269
  - 필수 승인 = Scott · Thomas
  - 클리닉은 고객번호만 입력한다 · 사용자는 Organization ID 를 몰라도 된다
  - VAG 가 Org-ID 등록 처리 중에 `link` 를 불러 매핑을 만든다 · 프록시로 부르는 `link` 는 막는다
  - `PENDING` 이어도 매핑을 만든다 · 동의 확인은 EWC [Refresh] 에서 `check`(자동 폴링 없음)
  - 카탈로그가 등록된 Org-ID 를 돌려준다 — `check` 본문용 · EzServer 가 따로 저장하지 않는다
- **열린 것**
  - 이미 연결된 조직에 `link` 를 다시 부르면 같은 Org-ID 를 돌려주는지, 409 인지 — Straumann 문의(Thomas)
  - EzServer 쪽 필요 시점 — Thomas 답
- 다음 — 스펙 승인 → 구현 세션 구현

---

## 3. Enrollment 일회용 승인 링크 — 대리점 설치자도 Entra 없이 승인 (Owen 제기 11/19)

- 계기 — enroll 뒤 C/S 의 Console 승인이 번거롭고 실수할 수 있다 · 나라에 따라 대리점 직원이 설치하는데 Entra 계정이 없다(Owen)
- 제안 — Thomas 의 승인 링크 + Scott 의 OTP 아이디어를 합쳤다
  - VAG 가 enroll 응답에 일회용 승인 링크를 주고, EzServer 화면이 링크와 QR 을 보여 준다
  - 설치 PC 에서 링크 클릭 또는 휴대폰 QR 로 승인 · 한 번만 · 30분 · 그 기기 하나만
  - 새 병원의 첫 기기에만 · 이미 기기가 있는 병원은 지금처럼 Console 승인
  - 링크 승인마다 Admin 에게 메일 · 리전 시간당 상한 · 선점 경고 · 리전 설정으로 켬(기본 꺼짐)
- ⚠ 리스크 — 지금 VAG 는 라이선스를 실제로 검증하지 않아 누구나 새 병원을 만들어 자가 승인할 수 있다 · 남는 위험 = DoS·비용 · Clinic-ID 선점(탐지) · 근본 해결 = LMP 라이선스 검증
- **OnePager PR 16272** — https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/16272
  - 필수 승인 = Scott · Thomas · Owen 은 저장소 권한이 없어 리뷰어로 넣지 못함
- 전제 — 운영자 메일 알림(SRS §7.10 · gw/1.1) 구현 · EzServer 적용은 나중

---

## 4. Alliedstar IO 스캐너 연동 — ADF 시연 마무리

- **ADF 시연(11/24~) 결과 · 현장 이슈** — Scott · Nick
- 시연 PC 설치 파일 — 우선 개발용을 주고, 유럽에 붙는 것으로 다시 패키징해 전달(Scott 11/19 14:32) · 법인 설치 작업과 hosts 갱신은 법인 CS(Owen 11/19)
  - 유럽 Edge 패키지(VT-Edge-Europe-0.3.3-euc1-adf.1-r2)는 enroll 된 기기 정보를 넣어 둔 것이라 설치하면 바로 유럽 VAG 에 붙는다(Scott) · 서울 dev 는 기존 Edge
  - ⚠ 이 패키지를 여러 PC 에 깔면 모두 같은 기기 하나로 붙는다 — 두 PC 를 동시에 켜면 하행 연결이 서로 끊을 수 있다(시연은 webhook 없음 · 끊김이 보이면 의심)
- 시연 뒤 할 일

  | # | 할 일 | 담당 | 목표 | 상태 |
  | -- | --- | --- | --- | --- |
  | 1 | **유럽 스택 사내 IP 제한** | Jack | 11/28 | Jack 복귀 뒤 |
  | 2 | **업체 답** — 로드밸런서 IP 2개(`100.58.144.120` · `3.219.109.235`) 수정 여부 | Scott | — | 답 대기 |
  | 3 | 시연 결과 정리 · 1차 범위(촬영 결과 가져오기 · webhook) 착수 여부 | Scott | ADF 뒤 | |
  | 4 | Edge ↔ 장비 Agent 연동 방식 문서(요청 문서 S8) — Raymond 초안 → Scott 확인 | Raymond · Scott | 12/4 | |
  | 5 | EzDent-i ↔ Edge 계약 문서(요청 문서 N1) | Nick · Scott | ADF 뒤 | |
  | 6 | 커넥터 운영 runbook 의 `VTG` 표기를 `VAG` 로 | 구현 세션 | 다음 구현 PR | |

- 11/19 오후 진행(참고)
  - ✅ Nick 촬영 PC — hosts 두 줄(`api-us.allied-star.com` · `asconnect-us-aws-a.allied-star.com` → `52.6.223.226`)로 케이스 생성 → AS Connect 실행(13:25)
  - ✅ 사내 hosts 가이드·점검 스크립트를 두 줄 기준으로 수정(PR 16270) · 프랑스 법인 CS 용 영어 가이드 Owen 에 전달
  - ✅ 커넥터 수정 PR 16264 머지 · spec-v1.3.2 · Console 시간 제한 40초/45초 · 커넥터 업체 호출 제한 38초(Jack · 서울 dev·유럽)
  - ✅ 유럽 — Edge 연결·승인(Scott 16:27) · 계정 연결 확인(Jack 16:39) · Nick 에 유럽 시험 요청
  - ✅ 업체 장애 보고문(영문) 작성 · 기존 소통 창구로 전달(Owen 11/19)
- 문서 — 촬영 PC hosts 가이드 = https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/handoff/alliedstar-capture-pc-hosts.md&version=GBmain

---

## 5. 공유

- **VAG 설명회 — 기획·QA 팀**
  - ✅ 11/19 13:30~15:00(Daniel 주관) · 1부 VAG 제품 설명(Raymond) · 2부 EzServer 와 VAG 연동 흐름(Thomas)
  - 발표 자료 = Wiki `vt-api-gateway/overview/vag-introduction`

- **EzServer 리전 목록(RGD) 서명 검증 공개키**(Levi)
  - prod 공개키 2개(k1·k2) — 운영 Directory euc1 게시 뒤 Jack 이 EzServer 에 전달 · 전달 여부 확인
