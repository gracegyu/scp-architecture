# VT API Gateway — 11/12 주간회의 Agenda

> 순서: **1. Alliedstar 시연 준비(진행 중 · 승인 필요)** → 2. Target Policy(완료 보고) → 3. R1 하행 NATS 전환 → 4. 공유
>
> 이전 주차 내용은 `주간회의-Agenda-Archive.md`.

- 🔴 **이번 회의에서 결정·승인할 것** — 모두 1장 Alliedstar
  - OnePager [PR 15974](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/15974) 승인(Scott — 필수 리뷰어)
  - 실제 업체 자격 전달 일정(Scott) — 11/13 마감

---

## 1. Alliedstar IO 스캐너 연동 — ADF 시연 준비 (진행 중)

- **목표** — EzDent-i 에서 환자를 고르면 원내 VT Edge 가 VTG 를 거쳐 Alliedstar 에 케이스를 만들고, 그 PC 에서 촬영 앱(AS Connect)을 띄운다
- **일정** — 리허설 11/20(금) · ADF 전시 11/24~
- **시연 범위** — 케이스 생성과 촬영 실행까지(11/10 Nick 확인)
  - 촬영 결과 가져오기는 1차
  - webhook(업체 콜백 수신·원내 전달)은 없다
  - EzServer 는 무관하다
- **개발 분장**(11/09 Scott·Raymond 합의)

  | 지점                      | 담당    |
  | ------------------------- | ------- |
  | EzDent-i · IO 스캐너 연동 | Nick    |
  | VT Edge                   | Scott   |
  | VTG · Alliedstar 커넥터   | Raymond |
  | 유럽 스택 인프라          | Jack    |

- **문서**
  - OnePager = [PR 15974](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/15974)
  - VTG 스펙 = [PR 15997](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/15997)
  - 인프라 요청 = [alliedstar-connector-infra.md](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/handoff/alliedstar-connector-infra.md&version=GBspec/alliedstar-onepager)(Jack 이 결과 칸에 기입)
  - Scott·Nick 요청 = [alliedstar-edge-ezdenti-requests.md](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/handoff/alliedstar-edge-ezdenti-requests.md&version=GBspec/alliedstar-onepager)(회신 칸에 답)
  - 두 문서는 OnePager PR 브랜치에 있다 — 머지 뒤에는 main 경로로 바꾼다

### 1-1. 🔴 회의에서 승인·확인

| #   | 항목                                                      | 누가       | 승인·확인되면                                        |
| --- | --------------------------------------------------------- | ---------- | ---------------------------------------------------- |
| 1   | OnePager PR 15974 승인 — Jack 승인 완료 · 리뷰 지적 전부 해소 | Scott(필수) · Nick(선택) | 바로 머지                                            |
| 2   | 스펙 PR 15997 — 승인 완료(Thomas) · OnePager 머지 뒤 머지 진행 공유 | —          | 머지 · 태그 spec-v1.3.0                              |
| 3   | 실제 업체 자격(appid · 서명 키 · 시연 계정) 전달 일정      | Scott      | 11/13 까지 못 받으면 시연을 조회로 줄인다            |
| 4   | Edge 를 서울 dev VTG 에 처음 연결 — 11/11 예정, 진행 여부 | Scott      | 안 됐으면 새 날짜                                    |
| 5   | EzDent-i ↔ Edge 계약                                      | Nick·Scott | 정해지면 요청 문서 회신 칸에 기록                    |
| 6   | 업체가 호출 IP 허용 목록을 요구하는지                     | Scott → 업체 | 요구하면 Jack 이 유럽 스택 egress IP 전달           |
| 7   | 유럽 스택 착수일                                          | Jack       | 11/13 기동 목표 유지 여부                            |

### 1-2. ✅ 한 일

- **스펙·문서**
  - ✅ 관련 PR 5건 리뷰·처리(11/09) — 4건 머지 · 1건은 중복이라 닫음
  - ✅ OnePager(PR 15974) 작성·리뷰 반영 — Jack 승인
  - ✅ VTG 스펙 개정([PR 15997](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/15997)) — 리뷰 2라운드 14건 반영 · Thomas 승인(11/11) · 머지만 남음
    - VT Edge 를 v1.0 device 로 받는다
    - Alliedstar 커넥터 요구사항(FR-INT-08)
    - 업체 계정 연결·업무 대장 테이블
    - 테스트 케이스 14개
    - 시연 동안 받아들이는 위험 명시 — 커넥터 접근 제한 장치 · mesh 재시도 끄기 · 전용 DB 계정 · egress 제한은 1차로 미룸
  - ✅ 유럽 스택 방침 — Scott 결정(11/10)
    - 유럽 prod 클러스터에 그대로 올린다(네임스페이스·DB 분리 없음)
    - 운영 도메인 `api.euc1.gw.ezcld.com` · 리전 코드 `euc1`
    - 실제 환자 정보는 넣지 않는다 · 시연 뒤 사내 IP 로만 접속 제한
    - 운영 Region Directory 에는 유럽 항목을 올리지 않는다(Jack 11/11)
  - ✅ 커넥터는 VTG 저장소의 별도 프로세스(5번째 배포 단위 · 11/10 확정)
- **구현**(브랜치 완료 · PR 은 스펙 머지 뒤)
  - ✅ 커넥터 골격 · 업체 서명(RSA2) · 신원 확인 · 원내 범위 보호
  - ✅ Edge → VTG → 커넥터 → 가짜 업체 전체 경로 테스트 통과
  - ✅ 테스트 unit 166건 · e2e 27건 통과
  - ✅ 업체 테스트 서버에서 정상 서명 통과 · 변조 서명 거부 확인
  - ✅ 배포 단위(Dockerfile · 파이프라인 정의) · 운영 runbook
- **인프라 — 서울 dev**(Jack 11/10~11)
  - ✅ 이미지 저장소(ECR) 생성
  - ✅ gitops 배포 정의 머지(es-gitops PR 16034) — 클러스터 내부 전용 Service · DB 마이그레이션 Job
  - ✅ 커넥터 설정 등록(Secrets Manager `dev/vt-api-gateway-alliedstar-connector/config`)
  - ✅ DB 접속 정보 주입
  - ✅ 공개 주소 `alliedstar.apne2.gw.dev.ezcld.net` → VTG 도달 확인 — target 등록 전이라 404 는 정상
  - ✅ 커넥터 → 업체 테스트 서버 egress 제한 없음

### 1-3. ⏳ 남은 일 (순서대로)

| #   | 할 일                                                 | 담당          | 선행                 | 목표   |
| --- | ----------------------------------------------------- | ------------- | -------------------- | ------ |
| 1   | OnePager 머지 → 스펙 머지 · 태그 spec-v1.3.0          | Raymond       | 1-1 의 1 승인        | 11/12  |
| 2   | 커넥터 구현 PR 생성·CI·머지                           | Raymond       | 스펙 머지            | 11/13  |
| 3   | 커넥터 파이프라인 등록 → 이미지 빌드                  | Jack          | 구현 PR 머지         | 11/13  |
| 4   | 업체 자격 값 2개(appid · 서명 키) 주입                | Jack          | Scott 이 자격 전달   | 11/13  |
| 5   | 서울 dev 커넥터 기동 · target 등록 · 시연 계정 연결   | Raymond       | 3 · 4                | 11/14  |
| 6   | 서울 dev 실측 — Edge → VTG → 커넥터 → 업체            | Raymond·Scott | 5 · Edge 연결        | 11/17  |
| 7   | 유럽 스택 구축(배포 단위 · DB · IoT · KMS · 비밀값 · 도메인 · Console 접근 · 관측) | Jack | — | 11/18 |
| 8   | 유럽 스택 배포·실측                                   | Raymond·Jack  | 7                    | 11/19  |
| 9   | 리허설(유럽 VTG)                                      | 전원          | 8                    | 11/20  |
| 10  | 시연 뒤 유럽 스택 사내 IP 제한                        | Jack          | 시연 종료            | 11/28  |

### 1-4. 🚧 Blocker

| Blocker                                         | 막는 것                        | 풀 사람 | 기한  |
| ----------------------------------------------- | ------------------------------ | ------- | ----- |
| OnePager 승인 대기                              | 구현 PR · 파이프라인 · 배포    | Scott   | 11/12 회의 |
| 실제 업체 자격 미수령                           | 커넥터 기동 · 케이스 생성 시연 | Scott   | 11/13 |
| Edge 가 실제 VTG 에 연결해 본 적 없음            | 전 구간 실측                   | Scott   | 1-1 의 4 |
| 유럽 스택 미착수(인프라 요청 B2~B9 결과 칸 비어 있음) | 유럽 배포·리허설          | Jack    | 1-1 의 7 |

- 참고 — 업체 공개 테스트 자격으로 커넥터를 먼저 띄울 수는 있다. 단 케이스 조회만 되고 케이스 생성은 안 된다

### 1-5. 리스크

- ⚠ 유럽 스택이 0 에서 시작 — 남은 실질 영업일 6일
- ⚠ 유럽 스택은 운영 클러스터·운영 도메인이다 — 실제 환자 정보를 넣지 않고, 시연 뒤 사내 IP 로 제한한다

### 1-6. 설계 요점(참고)

- 커넥터는 업무 요청을 업체 규격(개발사 자격 · RSA2 서명 · 사용자 `openid`)으로 바꿔 대신 호출한다
- ⭐ Alliedstar 에도 연동사 단위 API 가 있다 — Target Policy 를 만든 이유와 같은 빈틈
  - `getCaseDetail` 은 케이스 코드만으로 조회된다 — 다른 원내 환자 정보가 보일 수 있다
  - 커넥터가 원내 계정 연결로 `openid` 를 넣고, 그 원내가 만든 케이스인지 확인한 뒤에만 조회한다
  - `createUser`·`toothsplit` 은 Target Policy 로 막는다 — Target Policy 의 두 번째 적용
- 1차 결과 수집은 기존 EzScan Air 처럼 push(저장 완료 → 원내 알림 → 제품 갱신)가 자연스럽다(Nick 의견)

---

## 2. Target Policy — ✅ 완료 (11/10)

- **무엇** — target 마다 클리닉이 호출하면 안 되는 API(메서드·경로)를 GW 에 등록해 두고, 클리닉이 호출하면 GW 가 거부한다
  - 첫 적용 = AXS webhook 구독 관리 API(`/v1/webhook/**`)
  - 막을 API 가 더 생기면 운영자가 Console 에서 규칙 한 줄을 추가한다 — 배포 불필요
- **왜** — AXS 의 webhook 구독 관리 API 는 연동사(Vatech) 단위라 AXS 가 클리닉을 구분하지 못한다
  - 클리닉 하나가 잘못 호출하면 같은 리전의 Vatech 연동 클리닉 전부가 영향을 받는다
  - 자격을 빌려주는 GW 만 막을 수 있다
- **결과**
  - ✅ 스펙 승인·머지(11/05 · Scott·Thomas) — [GW PR 15814](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/15814) · [Console PR 15815](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/15815)
  - ✅ 구현 머지(11/09~10) — GW 3건 · Console 3건
  - ✅ dev 실측(11/10) — 차단 403 · 비정규 경로 400 · Console 감사 기록 · Console 화면 시나리오 통과
  - ⭐ 사전 리뷰가 실제 우회 두 건(`#` 붙인 경로 · NUL 문자로 감사 누락)을 찾아 스펙에 반영했다
- **남은 것**
  - Clinic Policy(누가 이 target 을 써도 되나) 재설계 — gw/1.1
  - AXS 조직 연동 API 의 고객번호 검증 · 쿼리로 하는 메서드 재정의(`_method`) — backlog
- 테스트는 dev 에서 했다 — test 환경은 아직 없다
- 상세 = [Target Policy OnePager](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/onepager/target-policy-onepager-2026-10-27.md&version=GBmain)

---

## 3. 📌 R1. 하행(GW → 원내) 전달을 MQTT(AWS IoT Core)에서 NATS JetStream 으로 바꾼다 — Alliedstar 시연 끝나면 착수

- 제안 = Scott · 검토 = Raymond · 결정(11/09) = 전환
- 왜 — 같은 원내에 EzServer 와 VT Edge 가 함께 붙으면 기기마다 자기 몫을 따로 받아야 한다
  - 지금 MQTT 는 같은 clinic 토픽을 두 기기가 다 받거나(일반 구독), 그중 하나만 받는다(shared subscription)
  - 오프라인 기기 버퍼가 약 100건이고 넘치면 통보 없이 버린다
  - JetStream 은 기기·기능별 durable consumer 로 각자 이어 받고, 보존 기간을 우리가 정한다
- 왜 지금 — 하행은 정식 배포 전이고 EzServer 는 스펙 단계다. VT Edge 도 NATS 를 쓸 계획이다
- 대가
  - 관리형이 아니다 — 리전마다 클러스터를 우리가 운영한다(인프라 합의 필요 · Jack)
  - enroll 의 IoT 인증서 발급을 NATS 자격 발급으로 바꾼다
  - 원내 방화벽 때문에 443(WebSocket) 접속을 기본으로 한다
- 진행 — 1주 dev 검증(자격 발급·폐기 · 기기별 수신 · 443 접속 · 오프라인 재접속 유실 없음) → 스펙 개정(결정 기록 4번 재결정 · SRS §7.6.6) → 구현
- EzServer 하행 스펙도 함께 바뀐다(Thomas)
- 백로그 = vt-api-gateway B-35

---

## 4. 📌 공유 — EzServer 의 리전 목록(RGD) 서명 검증 문의(Levi · 11/11)

- EzServer 가 SRS §7.3.6 대로 `regions.json` 의 detached JWS 서명 검증을 적용 중이다
- ⚠ **공개키를 받기 전에는 EzServer 가 리전 목록을 쓸 수 없다** — dev 공개 JWKS 경로가 403 이라 별도 전달이 필요하다
- 서명키 생성·보관·회전·게시는 인프라 몫(Jack) — 공개키 전달 · 회전·긴급 폐기 절차 · prod RGD 공개 일정 · 게시 순서
  - Jack — dev/test 키는 EzServer 채널에 공유함 · prod RGD·키는 준비 예정
- 스펙 몫은 답변 완료 — prod 도 무인증 GET 유지 · 키 회전 중첩 기간은 EzServer 가 값을 제시(SRS §7.3.6 규칙)
