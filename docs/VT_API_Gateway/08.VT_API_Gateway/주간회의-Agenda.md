# VT API Gateway — 11/19 주간회의 Agenda

> 순서: **1. Alliedstar 시연 준비(리허설 D-1)** → 2. R1 하행 JetStream 채널 추가 → 3. 지난 회의 후속·공유
>
> 이전 주차 내용은 `주간회의-Agenda-Archive.md`. Target Policy 는 11/12 완료 보고로 끝났다(Archive 11/12).
>
> 11/19 오전 기준으로 갱신했다.

- 🔴 **이번 회의에서 결정·확인할 것**
  - **데모에 꼭 필요한 것**(1-1 표의 🔴)
    - AS Connect 앱 로그인·Launch 실패 → 원인 = 업체 IP 2개 응답 없음 → 촬영 PC hosts 를 정상 IP 로 고정(Nick)
    - createCase 실패·503 → 업체 조회는 빠름 → 케이스 생성만 느린지 VAG 쪽인지 로그로 확인(Jack) · 시간 제한은 별도로 늘림
    - **오늘 중 끝낼 순서**: 서울 dev Launch 확인 → 유럽 Edge enroll·승인·계정 연결 → 유럽 실측(최종은 유럽 리전 · Scott)
    - 시연 PC 준비(AS Connect 계정 · hosts)
    - 리허설(11/20) 진행 여부·범위
    - Raymond(11/20)·Jack(11/24~27) 부재 동안 Console 운영·인프라 대응 담당
  - 하행 JetStream OnePager — **오늘(11/19) PR · 11/23(월)까지 승인**(Jack 화~금 휴가 전) — 2장

- **지난 회의(11/12) 결정 추적**

  | 결정                                                                 | 담당          | 상태 |
  | -------------------------------------------------------------------- | ------------- | ---- |
  | OnePager PR 15974 승인 보류 — 오늘 중 client 측 구조(EzDent-i 또는 별도 Agent 가 촬영 명령) 결정 → 바뀌면 Raymond 가 OnePager 수정 → 승인·머지 | Scott·Nick · Raymond | ✅ 11/12 — 장비 Agent 구조로 OnePager 수정 → Scott 승인 → 머지 · 스펙 머지·spec-v1.3.0 |
  | 실 업체 자격 Jack 에게 전달                                          | Raymond       | ✅ 11/12 |
  | Edge 를 서울 dev VAG 에 연결                                         | Scott         | ✅ 11/12(Scott 개인 PC) |
  | 업체 호출 IP 허용 목록 — 없음                                        | Scott         | ✅ 11/12 확인 · OnePager·handoff 4곳 반영(11/12) |
  | 유럽 스택 착수                                                       | Jack          | ✅ 11/18 — VAG 앱 5개·커넥터·업체 자격 · 운영 Region Directory euc1 게시 · prod Console 배포 · target 등록(Raymond) · Edge enroll 만 남음 |
  | test 환경은 서울에 있다                                              | Jack          | ✅ 확인 |
  | HA 부하테스트는 급한 일 끝나면 진행                                  | —             | 보류 |
  | NATS 관리형도 있다 — 어떤 형태인지(SaaS 또는 전용 클러스터)          | Jack          | ⏭ JetStream OnePager 단계에서 확인 |
  | EzServer 하행을 JetStream 으로 바꿀 때 필요한 일정 확인              | Thomas        | ✅ **Thomas 결정 = B안** — "이번 릴리즈는 MQTT 를 유지하고, NATS 전환은 이후 일정으로 분리한다" · v6.6.0 은 MQTT · 전환 시점은 미정 — 2장 |

---

## 1. Alliedstar IO 스캐너 연동 — ADF 시연 준비 (리허설 D-1)

### 1-1. ⏳ 남은 일 · 오늘 확인할 것

> **굵게** = 미완료 · 🔴 = 오늘 회의에서 확인·결정 · 🚧 = 다음 단계를 막고 있음 · 완료된 일은 1-3 한 일

| #  | 할 일 | 담당 | 목표 | 상태 | 오늘 회의 | 🚧 막는 것 | 회의 결정 |
| -- | --- | --- | --- | --- | --- | --- | --- |
| 1  | **AS Connect 앱 로그인 · Launch** — 11/19 오전 Nick 시험: 앱 로그인 실패("현재 네트워크를 사용할 수 없습니다") → Launch 오류. 원인 = 업체 시험 환경 로드밸런서의 IP 5개 중 2개(`100.58.144.120` · `3.219.109.235`)가 TCP 연결 자체에 응답 없음(Raymond 측정 11/19 09:50 · 오후 재확인) · 계정 연결은 Scott 계정으로 변경 완료(11/18) | **Nick**: 촬영 PC hosts 를 응답하는 IP 로 고정(`52.6.223.226 api-us.allied-star.com`) — 가이드·IP 점검 스크립트 https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/handoff/alliedstar-capture-pc-hosts.md&version=GBmain (PR 16263) · IP 가 바뀌면 스크립트로 다시 고름 | 11/19 | 가이드 전달 · 조치 대기 | 🔴 확인 | 🚧 유럽 실측 · 리허설 |  |
| 2  | **createCase 실패 · 503** — 업체에선 케이스가 생기는데(AS Connect 웹 8건) VAG 가 15초 안에 결과를 못 받음 → Edge 가 중복 방지로 멈춤(`reconciliation_required`). 원인 = 커넥터가 응답 없는 IP 에 연결되면 15초 제한까지 멈춤(로컬 측정은 빠름 · Pod 에서만 막힘 — sidecar 추정) → 2-2 커넥터 수정으로 해결 | **Jack**: 서울 dev 08:30~09:30 커넥터 로그로 원인 확인(응답 없는 IP 연결 여부) · core 503 확인 · 시간 제한도 늘림: ✅ Console 응답 40초·전체 45초(Raymond · 서울 dev·유럽 11/19) · **Jack** 커넥터 `ALLIEDSTAR_VENDOR_TIMEOUT_MS`=38000·재시작 · **Scott** Edge 요청 50초 이상(서울 dev·유럽) | 11/19 | 2-2 배포 뒤 서울 dev 재시험 | 🔴 확인 | 🚧 시연 안정성 |  |
| 2-1 | 업체에 장애 보고 — 로드밸런서 IP 2개 연결 불가 · 서브넷 인터넷 경로·NACL 확인 요청(영문 보고문 Raymond 작성 11/19) · 기존 소통 창구로 전달(인도 법인 경로 안 씀 · Owen 11/19) — 업체가 고치면 hosts 없이도 풀리지만 기다리지 않고 함께 진행 | Scott | 11/19 | 보고문 준비됨 · 업체 전달·답 대기 | | |  |
| 2-2 | **VAG 커넥터가 응답 없는 IP 를 건너뛰게 수정** — 보통은 Host 이름으로 접속하고 IP 선택은 DNS·LB·HTTP 클라이언트에 맡기지만, 업체 LB IP 일부가 죽어 있어 커넥터가 **매 호출 DNS 로 IP 목록을 직접 받아 살아 있는 IP 로 접속**하도록 바꿈(인증서 검증·Host 헤더는 원래 Host 이름 그대로 · 업체 입장에선 평소와 같은 요청) · 요청을 보내기 전 연결 실패(연결 3초 안에 안 됨·거부)만 새 연결로 다시 시도(최대 3번 · 그 뒤 502) · 요청을 보낸 뒤 실패는 재시도 안 함(케이스 중복 방지) · 업체 IP 가 바뀌어도 VAG 는 설정 변경 불필요 | Raymond(스펙 ✅ spec-v1.3.2 · PR 16262) → 구현 PR 16264(DNS 매 호출 조회 · 응답 없는 IP 3초에 끊고 다음 IP · 실측 40초+ → 약 7초) → ✅ 머지(main e5c7652 · 11/19 10:36) → **Jack** 서울 dev·유럽 배포(커넥터 파이프라인 이미지 빌드 중) | 11/19 | 배포 대기 | 🔴 확인 | 🚧 시연 안정성 |  |
| 3  | **Edge 유럽 enroll** — Edge 의 VAG 주소를 `api.euc1.gw.ezcld.com` 으로 바꿔 새로 enroll | Scott | 11/19 오전 | ⏳ | 🔴 확인 | 🚧 4·5·6 |  |
| 4  | **유럽 Console 에서 Edge 승인 · clinicId 확인** | Raymond | 11/19 오전 | 3 뒤 | | |  |
| 5  | **유럽 DB 계정 연결 1행** — Scott 계정 openid · SQL 전달함 | Jack | 11/19 오전 | 3 뒤 | | |  |
| 6  | **유럽 실측** — Edge → VAG → 커넥터 → 업체 | Scott(Raymond 대기) | 11/19 15:00~ | ⏳ | | 🚧 리허설을 유럽으로 |  |
| 7  | **시연 PC 준비** — AS Connect 를 VAG 계정 연결과 같은 계정(es-scott)으로 로그인 · hosts(당일 IP 재확인) · 시연장 네트워크에서 업체 host 접속 | Scott·Nick | 11/20 | ⏳ | 🔴 확인 | |  |
| 8  | **리허설 진행 여부 · 범위** — Scott: 서울 dev 로 먼저 해 보고 **최종은 유럽 리전**에서 · 범위 축소 필요 여부 | 전원 | 11/20 | ⏳ | 🔴 결정 | |  |
| 9  | **11/20 리허설 담당** — Raymond 부재 · Console 운영(기기 승인·target 확인)과 장애 대응 | Scott | 11/19 | ⏳ | 🔴 결정 | |  |
| 10 | **ADF 기간 유럽 인프라 담당** — Jack 11/24~27 휴가 | Scott | 11/23 | ⏳ | | |  |
| 11 | **시연 뒤 유럽 스택 사내 IP 제한** | Jack | 11/28 | ⏳ | | |  |
| 12 | Edge ↔ 장비 Agent 연동 방식 문서(요청 문서 S8) — Raymond 초안 → Scott 확인 | Raymond·Scott | 12/4 | ADF 뒤 | | |  |
| 13 | EzDent-i ↔ Edge 계약 문서(요청 문서 N1) — 동작 중 | Nick·Scott | ADF 뒤 | ADF 뒤 | | |  |

### 1-2. 리스크

- ⚠ **오늘(11/19) 하루에 서울 dev Launch 확인 · 유럽 enroll·승인·연결·실측을 모두 끝내야 한다** — 서울 dev 는 계정 변경 뒤 아직 시도 전(Scott 11/19). 오후에는 13:30~15:00 설명회가 겹친다
- ⚠ **Raymond 11/20 부재 — VAG 쪽 준비는 11/19 까지 끝낸다.** 리허설 당일 Console 운영(기기 승인·target 확인)은 Jack(유럽 최초 운영자) · 장애 확인은 GW 구현 세션
- ⚠ 유럽이 11/19 까지 안 되면 리허설은 서울 dev 로 한다(같은 업체 시험 환경 · 계정 연결 완료 · 사내망에서 접속)
- ⚠ 유럽 스택은 운영 클러스터·운영 도메인이다 — 실제 환자 정보를 넣지 않고, 시연 뒤 사내 IP 로 제한한다
- ⚠ **업체 시험 환경 로드밸런서의 IP 2개가 연결되지 않는다**(Raymond 측정 11/19 · 가벼운 요청 10번 중 5번이 46~49초) — 앱 로그인 실패·createCase 시간 초과의 원인. 업체 서버 처리는 빠르다(정상 IP 로 1초 안). 업체에 보고함(2-1)
  - 촬영 PC 는 정상 IP 로 hosts 고정 · ELB 라 IP 가 바뀔 수 있어 **리허설·시연 당일 아침 재측정**(예비 정상 IP `54.211.228.114` · `34.192.45.185`)
  - VAG 커넥터는 응답 없는 IP 를 3초에 끊고 다음 IP 로 붙도록 고쳤다(2-2) — IP 를 고정하지 않고 매번 DNS 를 새로 받으므로 IP 가 바뀌어도 설정 변경 불필요
  - 시연 대안: 미리 만들어 둔 케이스로 Launch 만 보여 주기(Scott 결정)
- ⚠ **Jack 11/24(화)~27(금) 휴가 — ADF 시연 기간과 겹친다.** 시연 중 유럽 인프라 문제(파드·DB·인증서) 대응자를 정해 둔다
- ⚠ 촬영 PC 의 AS Connect 는 **VAG 계정 연결과 같은 Alliedstar 사용자(es-scott)로 로그인**해야 케이스가 열린다 — 리허설·시연 체크 항목


### 1-3. ✅ 한 일 (참고)

- **이번 주(11/12~18)**
  - 스펙·문서
    - ✅ OnePager 머지(11/12 · Scott 승인) — 장비 Agent 구조 반영 · 업체 IP 허용 목록 불필요 반영
    - ✅ VAG 스펙 머지 · 태그 spec-v1.3.0(11/12)
    - ✅ Scott 에 Edge ↔ 장비 Agent 연동 방식 확인 요청(요청 문서 S8 · 11/12)
  - 구현
    - ✅ 커넥터 구현 PR 16064 머지(11/12) — 사전 리뷰 지적 6건 반영 · unit 182 · e2e 27
    - ✅ 커넥터 파이프라인 등록·첫 이미지 빌드 성공(11/12 · Jack)
  - 서울 dev 준비(11/16)
    - ✅ 업체 자격 주입·커넥터 Ready(Jack)
    - ✅ target `alliedstar` 등록 · 차단 규칙 2건 · timeout 3/15/20초(Raymond)
    - ✅ 업체 승인 페이지로 `openid` 받기 · 계정 연결 1행 insert(ES 서울치과 · Jack 실행)
    - ✅ VAG 쪽 실측 — 차단 2건 403 · core → 커넥터 라우팅·토큰 검증·계정 연결 확인 동작
    - ✅ 시연 끝날 때까지 dev:showcase 금지(ES 서울치과 데이터 보호) — 구현 세션에 공지
  - 유럽 스택
    - ✅ VAG 앱 5개 배포 · 커넥터 Ready · 업체 자격 주입(11/16 · Jack)
    - ✅ 운영 Region Directory euc1 PR 16068 승인(11/18 · Raymond)
    - ✅ 11/19 진행 순서 공유(11/18 · Scott·Jack)
    - ✅ 운영 Region Directory euc1 게시 · prod Console 배포(11/18 · Jack)
    - ✅ 유럽 target `alliedstar` 등록 — 404 → 401 확인(11/18 · Raymond)
  - 서울 dev 실측(11/18 · Scott·Nick)
    - ✅ createCase 성공 · Edge listPatients 조회 성공
    - ✅ Launch 오류 원인 파악 — AS Connect 로그인 계정과 VAG 계정 연결이 다름 → 시연을 Scott 계정(es-scott)으로 하기로 함
    - ✅ 서울 dev 계정 연결을 Scott 계정 openid 로 변경(Jack)
  - 11/19 원인 분석·조치(Raymond)
    - ✅ 업체 시험 환경 측정 — 가벼운 요청 10번 중 5번 46~49초 · IP 5개 중 2개 응답 없음 · 정상 IP 3개 확인
    - ✅ VAG 커넥터 방식(Node)으로 측정 — 10번 모두 0.2~2.6초(응답 없는 IP 를 빠르게 건너뜀)
    - ✅ 업체 실제 처리 측정 — 커넥터와 같은 코드·서명·Scott 계정으로 케이스 목록 조회 10번 모두 0.2~1.5초 · code=200
    - ✅ 원인 특정 — 업체 로드밸런서 IP 2개가 TCP 연결 자체에 응답 없음(서버 처리 문제 아님) · DNS 는 AWS 가 관리 → 업체 로드밸런서 네트워크 설정 문제로 추정
    - ✅ VAG 스펙 개정 spec-v1.3.2(PR 16262) — 요청 전 연결 실패만 다음 IP 로 재시도
    - ✅ 커넥터 수정 PR 16264 머지(구현 세션) — 업체 시험 환경 실측 40초+ → 약 7초
    - ✅ 촬영 PC hosts 가이드·IP 점검 스크립트(PR 16263) — Nick 에 전달
    - ✅ Console target 시간 제한 응답 40초·전체 45초 — 서울 dev·유럽
    - ✅ 업체 장애 보고문(영문) 작성 — 업체 전달은 1-1 의 2-1
- **지난주까지**
  - 스펙·문서
    - ✅ OnePager(PR 15974) 작성·리뷰 반영 — Jack 승인
    - ✅ OnePager 에 업체 환경 확정 반영(11/12) — 시험 환경 · `openid` 받는 방법 · 시연 PC hosts · 리전 원칙의 시연 예외
    - ✅ VAG 스펙 개정(PR 15997) — 리뷰 2라운드 14건 반영 · Thomas 승인(11/11)
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


### 1-4. 목표 · 범위 · 분장 · 문서 (참고)

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

### 1-5. 설계 요점(참고)

- 커넥터는 업무 요청을 업체 규격(개발사 자격 · RSA2 서명 · 사용자 `openid`)으로 바꿔 대신 호출한다
- ⭐ Alliedstar 에도 연동사 단위 API 가 있다 — Target Policy 를 만든 이유와 같은 빈틈
  - `getCaseDetail` 은 케이스 코드만으로 조회된다 — 다른 원내 환자 정보가 보일 수 있다
  - 커넥터가 원내 계정 연결로 `openid` 를 넣고, 그 원내가 만든 케이스인지 확인한 뒤에만 조회한다
  - `createUser`·`toothsplit` 은 Target Policy 로 막는다 — Target Policy 의 두 번째 적용
- 1차 결과 수집은 기존 EzScan Air 처럼 push(저장 완료 → 원내 알림 → 제품 갱신)가 자연스럽다(Nick 의견)

---

## 2. 📌 R1. 하행(GW → 원내)에 NATS JetStream 채널을 추가한다 — MQTT 와 함께 지원

- 왜 — 같은 원내에 EzServer 와 VT Edge 가 함께 붙으면 기기마다 자기 몫을 따로 받아야 한다(MQTT 는 전원 수신 또는 한 대 수신 · 오프라인 ~100건 무통보 폐기)
- 결정 경과
  - 11/09 — JetStream 으로 전환(제안 Scott · 검토 Raymond · 백로그 B-35)
  - 11/12 — Scott: VT Edge 만 JetStream 을 적용해도 된다
  - ✅ **11/13 Thomas 결정 = B안** — "이번 릴리즈는 MQTT 를 유지하고, NATS 전환은 이후 일정으로 분리한다"(원문) · v6.6.0(12/24)은 MQTT · 전환은 하되 시점은 미정
  - 11/16 — 그래서 VAG 는 MQTT 를 대체하지 않고 **JetStream 을 추가해 두 채널을 함께 지원**한다(Raymond)
- VAG 방식(스펙 초안)
  - 기기가 enroll 때 지원 하행 채널을 알리면 VAG 가 정한다 · 알리지 않으면 MQTT — EzServer 변경 없음
  - 정한 채널은 device 에 기록 · 하행 발신부는 그 채널로 보낸다
  - JetStream 은 기기마다 durable consumer — 같은 원내 기기들이 각자 이어 받는다 · 보관 14일(치과 장기 휴무 커버)
  - 이미 활성인 기기는 지원 채널을 다시 알려 채널을 바꾼다(C/S 재승인 없음) — EzServer 가 업그레이드 뒤 옮겨 가는 길
  - VT Edge 부터 JetStream · EzServer 전환 시점은 Thomas 가 정한다(B안에서 미정)
- NATS 운영 방식 — 자체 운영 또는 관리형은 인프라가 정한다(Jack)
  - 기준: 메시지가 그 리전 안에만 머무는가 · 원내 방화벽 때문에 443(WebSocket) 접속을 지원하는가
  - Jack(11/18): 서드파티 관리형도 있고 Kubernetes Pod 로 설치해도 어렵지 않다 · **회사 정책상 인프라는 모두 AWS** → OnePager 제안 = EKS 자체 운영
- 진행
  - 순서: **OnePager → PR 승인 → SRS → 구현**
  - ✅ OnePager 초안(11/18) — 사전 리뷰 2종(Nemesis 리허설 · 스펙 리뷰 스킬) 반영 · 세 경우(EzServer MQTT 전부 · JetStream 전부 · 혼재) · 병원별 채널 발행 · EKS 자체 운영 · API·DB 변경점
  - **11/19(오늘) OnePager PR · 11/23(월)까지 승인**(Jack 화~금 휴가) · 승인 = Scott · Jack · Thomas
  - SRS 초안은 미리 써 두었다(11/17) — OnePager 승인 뒤 OnePager 기준으로 고쳐 스펙 PR(spec-v1.4.0)

---

## 3. 지난 회의 후속 · 이번 주 공유

- **VAG 설명회 — 기획·QA 팀(11/19 13:30~15:00 · Daniel 주관)**
  - 1부 VAG 제품 설명(Raymond) · 2부 EzServer 와 VAG 연동 흐름(Thomas)
  - 발표 자료 = Wiki `vt-api-gateway/overview/vag-introduction`(PR 16194·16203)

- **EzServer RPS 의 VAG 인증서 검증(Levi · 11/17)**
  - ✅ VAG edge 인증서 = ACM 공인 인증서 — Jack 이 Amazon 루트 5개 번들(gw-ca.pem) 제공 · RPS 정상 동작 확인
  - ✅ 번들을 내려주는 API 는 만들지 않는다 — 설정 자동 변경 구조가 생기면 그 길로 교체
  - ✅ SRS §4.5 에 반영(spec-v1.3.1 · PR 16183)
  - ✅ 2037~2040 루트 만료 추적 = 백로그 B-36(2032 점검 · 매 릴리즈 번들 갱신)

- **EzServer 리전 목록(RGD) 서명 검증 공개키**(Levi · 11/11 문의)
  - Jack — dev/test 키는 EzServer 채널에 공유함
  - prod — 운영 Directory 첫 행(euc1) PR 16068 승인(11/18) · 머지·게시 뒤 Jack 이 prod 공개키 2개(k1·k2)를 EzServer 에 전달
