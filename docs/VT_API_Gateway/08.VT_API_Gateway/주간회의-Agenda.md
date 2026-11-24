# VT API Gateway — 11/26 주간회의 Agenda

> 순서: **1. R1 하행 JetStream 채널 추가** → **2. AXS 조직 연결 스펙(PR 16269)** → **3. Enrollment 일회용 승인 링크(PR 16272)** → 4. Alliedstar ADF 시연 마무리 → 5. 공유
>
> 이전 주차 내용은 `주간회의-Agenda-Archive.md`(11/19 = Alliedstar 원인 분석·조치 경과 · 설계 요점 · 문서 목록 · JetStream 결정 경과).
>
> 11/24 오전까지의 진행을 반영했다. Jack 11/24~27 휴가.

- 🔴 **이번 회의에서 결정·확인할 것**
  - 하행 JetStream OnePager PR 16267 — Jack 승인 ✅ · **Scott 승인** · 바뀐 순서(조회 API 먼저 → PoC → go/no-go → SRS) 확인 — 1장
  - AXS 조직 연결 스펙 PR 16269 — 재설계(승인 webhook) 방향 · 잔여 위험(소유권 미검증) 수용 · Samuel 후속 답 · EzServer 필요 시점 — 2장
  - Enrollment 일회용 승인 링크 OnePager PR 16272 — 받아들이는 위험 · **Scott·Thomas 승인** — 3장
  - 자동 리뷰(Nemesis) 운영 — push 마다 재리뷰가 돈다 · 수렴 기준 — 5장
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
  | 하행 JetStream OnePager PR — 11/19 올림 · 11/23 승인 | Scott · Jack · Thomas | Jack ✅ Approve(11/23) · Scott 대기 — 1장 |

---

## 1. 📌 R1. 하행(GW → 원내)에 NATS JetStream 채널을 추가한다 — MQTT 와 함께 지원

- **OnePager PR 16267**(11/19) — https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/16267
  - **Jack ✅ Approve(11/23)** · Scott 승인 대기(필수) · Thomas 선택
  - 리뷰 스레드 모두 처리(자동 리뷰 4라운드 · Jack 1건)
- **Jack 우려와 대응(11/23 Teams·PR)**
  - Jack: 「NATS Jetstream 현재 도입은 시기상조」 — 고가용성에서도 유실 사례 · Operator 부재로 운영 중 수동 개입 · 운영 레퍼런스 부족
  - Scott: 도입 결정이 아니라 아이디어 단계 · 운영 장벽이 높으면 폐기해도 되는 단계 · "되는 것 찾고, 안되는 것이 되는 것에 비해서 얼마나 리스크가 큰지를 검토"
  - 근거(Jack PR 코멘트) — Jepsen(NATS 2.12.1): 정전 시 확인된 93만 건 중 13만 건 유실(기본값이 ack 후 2분마다 디스크 동기화) · nats-server 이슈 7564·7567 · 7545(노드 제거 중 크래시 → 에러 없이 유실)
  - 대응 — 쓰기마다 디스크 동기화(우리 부하 평균 초당 3건이라 여유) · 놓친 알림 조회 API · DB 원본 재발행 · 노드 교체는 StatefulSet 고정 이름·볼륨으로(멤버 제거가 아니게) · 2.12.3 이상
  - AZ 2곳(2+1) — dev·prod EKS 가 AZ 2곳만 씀 · AZ 전체 장애는 비용과 바꾼 한계로 수용(Jack 커밋)
  - AWS IoT 유지 + pull 은 운영 주체를 확보하지 못할 때의 예비안
- **바뀐 순서(11/23 · 통제 문서 승인은 go 뒤)**
  1. OnePager 승인 → **놓친 알림 조회 API** 스펙·구현(채널 무관 · 지금 MQTT EzServer 의 유실도 줄인다)
  2. 이번 주 — **로컬 유실 재현 시험**(NATS 3 노드 · LazyFS 로 정전 재현 · 기본 설정과 유실 방지 설정 비교) → 결과 PR 첨부 · Raymond
  3. Jack 복귀 뒤 — **서울 dev PoC**(NATS 만 · EKS 1.36 → 1.37 업그레이드로 노드 교체 확인 · 수동 작업 runbook 초안 · 조회 API 로 메움 확인)
  4. **go/no-go — Scott** · go 면 JetStream SRS 스펙 PR(초안 있음)
- 설계 요지
  - 기기마다 채널 하나 · VT Edge 는 JetStream · EzServer 는 버전에 따라 MQTT 또는 JetStream
  - 알림은 병원마다 그 병원 기기가 쓰는 채널에만 채널당 한 번 · 본문은 두 채널이 같다(원본 그대로)
  - 스트림 리전당 1개(인프라 IaC) · consumer 는 기기마다 VAG 자동 생성·삭제 · 보관 14일
  - MQTT → JetStream 전환은 겹침(유예 잠정 24시간 뒤 옛 자격 폐기)

---

## 2. AXS 조직 연결 — VAG 가 `link` 를 대행하고 승인 webhook 으로 매핑 (Thomas 안건 11/19)

- 계기
  - Thomas 안건 — 카탈로그 AXS 입력란에 Straumann 고객번호(`customerNumber`) 추가
  - 검토 중 결함 발견 — 기존 설계대로면 `link` 가 Org-ID 등록 전이라 VAG 에서 403 으로 막힌다
- 1차안(11/19)은 틀렸다 — Thomas 실측(ppr EU): `link` 의 PENDING 응답에 `organizationId` 가 없다 · `link` 재호출은 PENDING·APPROVED 모두 409
  - 원인 — 문서의 응답 스키마만 보고 실측 없이 전제로 삼았다
- **Straumann 회신(11/23 Samuel)** — 승인되면 AXS 가 webhook `organization.link` 로 `organizationId` 를 보낸다(공개 문서에 없는 이벤트) · 고객번호는 AXS 웹 사이트 프로필 메뉴에 표시
- **승인 화면(Thomas 11/23 화면 녹화)** — AXS 프로필 메뉴 → My company → Connections → VATECH `PENDING` → Approve(약관 동의) → `APPROVED` · Reject·Revoke 버튼도 있다 · 요청이 오면 빨간 점
- **스펙 PR 16269 재설계(spec-v1.4.0)** — https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/16269
  - 고객번호 입력 → VAG 가 `link` 호출 · 동의 대기 기록(202 · 카탈로그 `pending_consent`)
  - 병원 관리자가 AXS 에서 승인 → 승인 webhook → VAG 가 매핑 생성 · 그 이벤트를 병원 하행으로 전달(연동 완료 신호)
  - EzServer 는 `link`·`check`·Refresh 가 필요 없다 — 카탈로그 상태와 하행 이벤트로 완료를 안다
  - 철회(Revoke)면 매핑 삭제 · 거절이면 진행 기록 삭제 · 둘 다 다시 등록 가능
  - 등록 진행 기록(`org_link_request`) 신설 — 예약(동시성) · 동의 대기 · 결과 불명(복구) · 자동 삭제 없음(취소는 운영자가 업체 `unlink` 뒤)
  - `org_mapping (clinic_id, target_id)` 유일 제약 — 배포 전 기존 중복 점검 필요
  - 기기의 AXS Org-ID 직접 등록은 없앤다 — 이미 연결된 병원·복구는 운영자 교정
  - ⚠ 잔여 위험 — 고객번호 소유권은 검증하지 않는다(출처 없음) · 그 조직 관리자의 승인 · Org-ID 충돌 시 Admin 알림 · 감사로 완화
  - 리뷰 지적 모두 반영(1차 10건 · 재리뷰 11건) · 필수 승인 = Scott · Thomas
- **열린 것** — Samuel 후속 답(11/23 문의)
  - 승인 이벤트가 기존 구독으로 오는지 · 거절·철회 이벤트 형식 · 이벤트에 고객번호를 실을 수 있는지(응답 유실 시 자동 짝짓기) · 이미 승인된 조직의 Org-ID 확보 · Org-ID 고정 여부 · 재전송 정책
  - 답이 오면 한 번에 고쳐 push(그 전에는 push 보류 · 자동 재리뷰 때문)
  - EzServer 쪽 필요 시점 — Thomas 답
- 다음 — 승인·머지 → 구현 세션 구현 · **EzServer handoff**(Thomas · 바뀌는 계약과 EWC 흐름 한 장)

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
  - 필수 승인 = Scott · Thomas · Levi·Daniel 선택 · Owen 은 저장소 권한이 없어 리뷰어로 넣지 못함
  - 리뷰 반영(11/23 · 3라운드) — Thomas 의 핵심 지적: 첫 기기 판정이 발급 때 한 번뿐이라 「미리 enroll → 진짜 병원 가동 → 보관한 토큰으로 승인」 공격이 열려 있었다
    - 판정 = 「그 병원에 승인된 적이 있는 기기가 없음」 · 발급·승인·재발급 세 번 확인 · 승인은 병원 단위 직렬화 · `device` 에 첫 승인 시각 컬럼
    - 승인 화면 거부 버튼 제거 · 같은 링크 재호출은 「이미 승인됨」 · 상한은 새 승인만 세고 재호출은 막지 않음 · 메일 실패해도 승인은 진행(재시도·경보)
  - 두 번째 기기는 나중에 「기존 기기 보증」으로 넓힐 수 있다(이번 범위 아님)
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

- **자동 리뷰(Nemesis) 운영 — push 마다 전체 재리뷰가 돈다**(11/23 하루 세 PR 에서 10번 넘게 · 16269 한 번 ≈ 8분)
  - 스펙 PR(16269)은 실제 결함이 나와 가치가 있다 · OnePager(16267·16272)는 지적이 8 → 5 → 2 처럼 줄지만 고친 곳에서 새로 생긴다
  - 우리 쪽 — 수정을 모아 push 1회 · 외부 답 대기 중인 PR 은 push 보류 · 새 코멘트는 등급·성격을 보고 판단
  - 논의 — OnePager 의 「권장」은 후속 스펙 PR 로 미루는 기준 · 재리뷰를 요청할 때만(또는 하루 1회) 돌리는 방법(Thomas)

- **VAG 설명회 — 기획·QA 팀**
  - ✅ 11/19 13:30~15:00(Daniel 주관) · 1부 VAG 제품 설명(Raymond) · 2부 EzServer 와 VAG 연동 흐름(Thomas)
  - 발표 자료 = Wiki `vt-api-gateway/overview/vag-introduction`

- **EzServer 리전 목록(RGD) 서명 검증 공개키**(Levi)
  - prod 공개키 2개(k1·k2) — 운영 Directory euc1 게시 뒤 Jack 이 EzServer 에 전달 · 전달 여부 확인
