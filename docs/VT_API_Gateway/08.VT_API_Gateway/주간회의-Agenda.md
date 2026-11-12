# VT API Gateway — 11/19 주간회의 Agenda

> 순서: **1. Alliedstar 시연 준비(리허설 D-1)** → 2. R1 하행 NATS 전환 → 3. 지난 회의 후속
>
> 이전 주차 내용은 `주간회의-Agenda-Archive.md`. Target Policy 는 11/12 완료 보고로 끝났다(Archive 11/12).
>
> _11/12 회의 직후 기준으로 이월했다. 회의 전에 진행분을 갱신한다._

- 🔴 **이번 회의에서 결정·확인할 것**
  - 리허설(11/20) 진행 여부 — 1-1 표
  - EzServer 하행 방향(Thomas) — 2장

- **지난 회의(11/12) 결정 추적**

  | 결정                                                                 | 담당          | 상태 |
  | -------------------------------------------------------------------- | ------------- | ---- |
  | OnePager PR 15974 승인 보류 — 오늘 중 client 측 구조(EzDent-i 또는 별도 Agent 가 촬영 명령) 결정 → 바뀌면 Raymond 가 OnePager 수정 → 승인·머지 | Scott·Nick · Raymond | ✅ 11/12 — 장비 Agent 구조로 OnePager 수정 → Scott 승인 → 머지 · 스펙 머지·spec-v1.3.0 |
  | 실 업체 자격 Jack 에게 전달                                          | Raymond       | ✅ 11/12 |
  | Edge 를 서울 dev VAG 에 연결                                         | Scott         | ✅ 11/12(Scott 개인 PC) |
  | 업체 호출 IP 허용 목록 — 없음                                        | Scott         | ✅ 11/12 확인 · 문서 4곳 정리는 OnePager 수정 때 |
  | 유럽 스택 착수                                                       | Jack          | 11/12 착수 · 완료 알림 대기 |
  | test 환경은 서울에 있다                                              | Jack          | ✅ 확인 |
  | HA 부하테스트는 급한 일 끝나면 진행                                  | —             | 보류 |
  | NATS 관리형도 있다 — 어떤 형태인지(SaaS 또는 전용 클러스터)          | Jack          | 확인 필요 |
  | EzServer 하행을 JetStream 으로 바꿀 때 필요한 일정 확인              | Thomas        | 회신 대기 — 2장 |

---

## 1. Alliedstar IO 스캐너 연동 — ADF 시연 준비 (리허설 D-1)

- **목표** — EzDent-i 에서 환자를 고르면 원내 VT Edge 가 VAG 를 거쳐 Alliedstar 에 케이스를 만들고, 그 PC 에서 촬영 앱(AS Connect)을 띄운다
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
  | VAG · Alliedstar 커넥터   | Raymond |
  | 유럽 스택 인프라          | Jack    |

- **업체 환경**(11/12 확정) — 업체 시험 환경 `api-us-aws-a.allied-star.com`(업체 운영과 분리) · dev·유럽 스택 공용 · 시연 PC 는 업체 안내대로 hosts 설정(ELB 라 당일 IP 재확인)
- **문서**
  - OnePager = [alliedstar-io-scanner-onepager-2026-11-09.md](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/onepager/alliedstar-io-scanner-onepager-2026-11-09.md&version=GBmain)(PR 15974 · 11/12 머지)
  - VAG 스펙 = spec-v1.3.0([PR 15997](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/15997) · 11/12 머지)
  - 인프라 요청 = [alliedstar-connector-infra.md](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/handoff/alliedstar-connector-infra.md&version=GBmain)(Jack 이 결과 칸에 기입)
  - Scott·Nick 요청 = [alliedstar-edge-ezdenti-requests.md](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/handoff/alliedstar-edge-ezdenti-requests.md&version=GBmain)(회신 칸에 답)

### 1-1. 🔴 회의에서 결정·확인

| #   | 항목                                                         | 누가        | 결정·확인되면                         | 회의 결정 |
| --- | ------------------------------------------------------------ | ----------- | ------------------------------------- | --- |
| 1   | client 측 구조 — 촬영 명령을 EzDent-i 가 내는가, 별도 Agent 가 내는가 · OnePager 반영·승인 상태 | Scott·Nick  | OnePager 머지 → 스펙 머지             |  |
| 2   | 서울 dev 전 구간 실측 결과 — Edge → VAG → 커넥터 → 업체(케이스 생성·촬영 명령) | Raymond·Scott | 유럽 스택으로 전환                  |  |
| 3   | 유럽 스택 완료 여부 · 유럽 전 구간 실측                       | Jack·Raymond | 리허설 진행                          |  |
| 4   | 시연 PC 준비 — 촬영 앱 · hosts 설정 · 시연장 네트워크에서 업체 host 접속 | Scott·Nick | 리허설 진행                          |  |
| 5   | EzDent-i ↔ Edge 계약                                         | Nick·Scott  | 요청 문서 회신 칸에 기록              |  |
| 6   | 리허설(11/20) 진행 여부 · 시연 범위 축소 필요 여부            | 전원        | 리허설 진행 또는 범위 확정            |  |

### 1-2. ✅ 한 일

- **이번 주(11/13~19)** — _회의 전 갱신_
- **지난주까지**
  - 스펙·문서
    - ✅ OnePager(PR 15974) 작성·리뷰 반영 — Jack 승인 · Scott 승인 보류(client 구조 결정 대기)
    - ✅ OnePager 에 업체 환경 확정 반영(11/12) — 시험 환경 · `openid` 받는 방법 · 시연 PC hosts · 리전 원칙의 시연 예외
    - ✅ VAG 스펙 개정(PR 15997) — 리뷰 2라운드 14건 반영 · Thomas 승인(11/11) · 업체 환경 반영(11/12) · 머지만 남음
      - VT Edge 를 v1.0 device 로 받는다
      - Alliedstar 커넥터 요구사항(FR-INT-08)
      - 업체 계정 연결·업무 대장 테이블
      - 테스트 케이스 14개
    - ✅ 유럽 스택 방침 — Scott 결정(11/10) · 유럽 prod 클러스터 · 운영 도메인 `api.euc1.gw.ezcld.com` · 실 환자 정보 없음 · 시연 뒤 사내 IP 제한
    - ✅ 실 업체 자격 수령·전달(11/12)
  - 구현(브랜치 완료 · PR 은 스펙 머지 뒤)
    - ✅ 커넥터 골격 · 업체 서명(RSA2) · 신원 확인 · 원내 범위 보호
    - ✅ 테스트 unit 166건 · e2e 27건 통과
    - ✅ 배포 단위(Dockerfile · 파이프라인 정의) · 운영 runbook
  - 인프라 — 서울 dev(Jack)
    - ✅ ECR · gitops 배포 정의(es-gitops PR 16034) · 설정 · DB 접속 정보 · 공개 주소
  - VT Edge
    - ✅ 서울 dev VAG 연동(11/12 · Scott 개인 PC)

### 1-3. ⏳ 남은 일 (11/12 기준 순서)

| #   | 할 일                                                 | 담당          | 선행                 | 목표   | 상태 |
| --- | ----------------------------------------------------- | ------------- | -------------------- | ------ | ---- |
| 1   | client 측 구조 결정 → OnePager 수정 → 승인·머지        | Scott·Nick · Raymond | —            | 11/13  |  |
| 2   | 스펙 머지 · 태그 spec-v1.3.0                          | Raymond       | 1                    | 11/13  |  |
| 3   | 커넥터 구현 PR 생성·CI·머지                           | Raymond       | 2                    | 11/13  |  |
| 4   | 커넥터 파이프라인 등록 → 이미지 빌드                  | Jack          | 3                    | 11/14  |  |
| 5   | 업체 자격 2개 주입 · 업체 host `api-us-aws-a` 로 변경  | Jack          | ✅ 자격 전달          | 11/13  |  |
| 6   | 시연 계정으로 업체 승인 페이지 로그인 → `openid` 받기 · Edge 의 clinicId 받기(Scott) → 계정 연결 1행 | Raymond | — | 11/14 |  |
| 7   | 서울 dev 커넥터 기동 · target 등록                    | Raymond       | 4 · 5                | 11/14  |  |
| 8   | 서울 dev 전 구간 실측 — Edge → VAG → 커넥터 → 업체    | Raymond·Scott | 6 · 7                | 11/17  |  |
| 9   | 유럽 스택 구축                                        | Jack          | —                    | 11/18  |  |
| 10  | 유럽 스택 배포·실측                                   | Raymond·Jack  | 9                    | 11/19  |  |
| 11  | 리허설(유럽 VAG)                                      | 전원          | 10                   | 11/20  |  |
| 12  | 시연 뒤 유럽 스택 사내 IP 제한                        | Jack          | 시연 종료            | 11/28  |  |

### 1-4. 🚧 Blocker

| Blocker                                                         | 막는 것                     | 풀 사람    |
| --------------------------------------------------------------- | --------------------------- | ---------- |
| client 측 구조(EzDent-i 또는 별도 Agent) 미결정 → OnePager 승인 보류 | 스펙 머지 · 구현 PR · 배포 | Scott·Nick |
| 유럽 스택 구축 중(11/12 착수)                                   | 유럽 배포·리허설            | Jack       |

### 1-5. 리스크

- ⚠ 리허설까지 남은 시간이 짧다 — 서울 dev 실측과 유럽 스택 실측이 연달아 있다
- ⚠ 유럽 스택은 운영 클러스터·운영 도메인이다 — 실제 환자 정보를 넣지 않고, 시연 뒤 사내 IP 로 제한한다
- ⚠ 업체 시험 환경은 ELB 라 IP 가 바뀐다 — 시연 PC hosts 는 리허설·시연 당일 아침 다시 확인한다

### 1-6. 설계 요점(참고)

- 커넥터는 업무 요청을 업체 규격(개발사 자격 · RSA2 서명 · 사용자 `openid`)으로 바꿔 대신 호출한다
- ⭐ Alliedstar 에도 연동사 단위 API 가 있다 — Target Policy 를 만든 이유와 같은 빈틈
  - `getCaseDetail` 은 케이스 코드만으로 조회된다 — 다른 원내 환자 정보가 보일 수 있다
  - 커넥터가 원내 계정 연결로 `openid` 를 넣고, 그 원내가 만든 케이스인지 확인한 뒤에만 조회한다
  - `createUser`·`toothsplit` 은 Target Policy 로 막는다 — Target Policy 의 두 번째 적용
- 1차 결과 수집은 기존 EzScan Air 처럼 push(저장 완료 → 원내 알림 → 제품 갱신)가 자연스럽다(Nick 의견)

---

## 2. 📌 R1. 하행(GW → 원내) 전달을 MQTT(AWS IoT Core)에서 NATS JetStream 으로 — Alliedstar 시연 끝나면 착수

- 결정(11/09) = 전환 · 제안 = Scott · 검토 = Raymond · 백로그 = vt-api-gateway B-35
- 왜 — 같은 원내에 EzServer 와 VT Edge 가 함께 붙으면 기기마다 자기 몫을 따로 받아야 한다
- 운영 방식 — 리전마다 우리가 운영하거나 관리형을 쓴다
  - Jack(11/12): 관리형도 있다 — SaaS 형태인지 리전 전용 클러스터인지 확인 필요
  - 기준: 하행 메시지가 그 리전 안에만 머무는가 · 원내 방화벽 때문에 443(WebSocket) 접속을 지원하는가
- **EzServer 하행 방향 — Thomas 결정 대기**
  - 배경: EzServer 는 MQTT 로 하행 스펙을 썼고(미구현) 일정이 촉박하다
  - Scott(11/12): VT Edge 만 JetStream 을 적용해도 된다
  - 선택지
    - 1안. 이번에 JetStream 으로 적용한다
    - 2안. 이번에 VAG 연동은 하되 하행은 빼고, 나중에 JetStream 으로 적용한다 — 지금 붙는 target 에는 하행이 필요 없어, 필요한 target 이 붙기 전에만 하면 된다
    - 3안. EzServer 는 MQTT(IoT Core)를 그대로 쓴다 — VAG 가 하행 경로 두 개를 계속 유지한다
  - 🔴 Thomas 결정 →  _회의에서 기록_
- 진행 — 1주 dev 검증(자격 발급·폐기 · 기기별 수신 · 443 접속 · 오프라인 재접속 유실 없음) → 스펙 개정(결정 기록 4번 재결정 · SRS §7.6.6) → 구현

---

## 3. 지난 회의 후속

- **EzServer 리전 목록(RGD) 서명 검증 공개키**(Levi · 11/11 문의)
  - Jack — dev/test 키는 EzServer 채널에 공유함 · prod RGD·키는 준비 예정
  - 확인: prod 공개키·RGD 공개 일정
