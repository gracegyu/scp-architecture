# VT API Gateway — 8/13 주간회의 Agenda

> **과거 주차(6/25~8/6)는 [`주간회의-Agenda-Archive.md`](주간회의-Agenda-Archive.md)로 이관·보존**(가끔 조회용). 본 문서는 **8/13 현행 주차만** 유지한다. 틀(논의/공유/이월)은 이전 주와 동일하며 **Gantt(S1)·스펙 작성 테이블(S2)은 매주 상시 포함**한다. _※ `(프레임)` 표시 항목은 8/13 회의 시 확정한다._

- 이번 주 진행 _(프레임 · 8/13 회의 시 확정 · 상세·수치는 아래 논의 R#/공유 S# 한 곳에만)_
  - **(8/6~8/13 완료) GW 자율 구현 범위 완결** — **P11 Admin CRUD 전 Task 완료**(11-1~11-6 머지: targets·policies·config/org-mappings·operators RBAC 생애주기·webhook-events break-glass·audit 전면·데이터분류 스캐폴드) + **P9-4 app-side graceful drain**(무유실·offline-hang 강제종료) → ④/인프라 무관 자율 가능 범위 소진 · 구현현황 = S3
  - **(8/13 완료) T-AUTH-2-6 — GW JWKS 공개 엔드포인트(v1.0.11 승격) + ③b device 토큰 계약 정합** — `GET /.well-known/jwks.json`(무인증·개인키 미노출·CleverSpace GW Guard=외부 검증자) + 토큰 `iss`https형식/TTL≤15분/`aud`=GW수준. 머지 #12478(외부 검증 시뮬 실 jwt.verify·전체 e2e 430 회귀0) → S3 ②-f
  - **(v1.0.11 반영) 스펙 정합화** — prod 리전 **시드니 `apse2`** 교정(멜버른 apse4=IoT Core 미지원)·JWKS v1.0 승격·Console 전역 단일 확정 → 코드 영향은 T-AUTH-2-6뿐(리전=배포 config·grep 반전 확인·재작업 0) → 공유 S5
  - **(진행 중 실무) AWS 환경 분리** — 계정/네트워크·ESO/Parameter Store 경로·`.env.template`(Jack·Raymond·③-I) · GW_REGION dev 프로비저닝
  - **(잔여) EzServer OnePager 수령 확인** · 보류·선결(IO Scanner=`이월-R1`)은 이월 표 참조
  - _(이번 주 결정사항 = 회의 시 추가)_

- 논의 사항 (이번 주 · 신규 논의/결정 안건)
  - _R1(GW Console 멀티리전 운영자 authz)은 이번 주 결정 완료 → 스펙 세션이 §7.9.2·DBML(`operator_role`)·③-C Console SRS로 정리·반영. 아젠다 상시 논의에서 종료._
  - _(이번 주 결정사항 = 스펙 세션 정리 후 반영 · 회의 중 신규 안건 발생 시 여기 추가 · 보류·선결은 아래 「이월 논의 사항」 표 참조.)_

- 공유 사항 (결정 아님 · 정보 공유 · 매주 상시)
  - **S1. 프로젝트 일정(Gantt) — 8/13 스냅샷** — 스펙 생애주기(작성→PR→baseline) + GW 구현 타임라인.
    - **정본** = [개발 Roadmap 결정 §3.9](<VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>) (수정은 그쪽 먼저 · 7/23→7/30 변경은 정본 §3.9 동기화 완료).
    - **8/6→8/13 변경**:
      - **GW 자율 구현 범위 완결**: P8·P9 골격(app-side) + **P11 Admin CRUD 전부(11-1~11-6 머지)** + **P9-4 app-side drain**(무유실)
      - **v1.0.11 정합화**: JWKS 엔드포인트 v1.0 승격 → **T-AUTH-2-6 완료(#12478)** · prod 리전 시드니 `apse2` 교정(멜버른=IoT Core 미지원) · Console 전역 확정
    - **직전 7/30→8/6 변경 유지**:
      - region-silo(R2) 구현 재작업 완료(PR #12241·8/3·단일 datasource) · P6 프록시 완결 · R2-1 확정(서울=dev·호주 먼저 오픈)
    - **직전 7/23→7/30 변경 유지**:
      - 0단계 IO Scanner·④ AXS = 보류(Straumann 협상)
      - ③-P-CS CleverSpace·③-P-CO CleverOne OnePager 2개 = Raymond·7/27 병행 착수(각 1·2·3단계 통합 · ①호환성·②Presigned One Pager 폐지→두 제품 OnePager에 흡수 · CleverOne Nick→Raymond)
      - 1·2·3단계 우선
    - **막대 색**: 작성=기본 · PR=강조 · ◆=baseline/마일스톤 · 빨강=외부/미정 선결
    - **선결(빨강)**: IO Scanner↔EzServer 연동방식(**보류·R1**) · AXS sandbox 자격(Straumann)
    - **목표 = 10월 출시**(역산·잠정 — ④ AXS/IO Scanner 보류로 **2단계 일정·출시일 재검토 대상**)
    - **병행 별도 프로젝트**: `SectionView Module 구현`(7/13~2주·Raymond·**GW 아님**·완료)은 `▷ 병행` 섹션에 표기
    - **GW 구현 = 2단계 병행(유지)** — 1단계 GW 독립 코어(P0~P6·P10)는 ③ baseline 고정으로 **정상 진행**(IO Scanner 보류 영향 없음). 2단계 AXS 연동(P7~P12)만 ④ AXS 보류에 연동되어 **후행**.
    - (결정)
      - GW Console v1.0 최소기능으로 앞으로 당겨서 진행한다. 전규현/ Raymond
        - **③-C Console Sub-SRS 작성 착수(8/5)** — v1.0(필수)·v2.0(방향) 한 문서로 baseline 동결 가능 수준까지 초안 완료·리뷰 중. **차주초 PR 예정**.
      - GW Console
        - MS Entra로 연동
        - infra
          - istio로 admin api 접근권한 제어
          - 페이지접근도 ZeroTrust 에서만 접근 가능하게한다.

    ```mermaid
    gantt
        title v1.0 = Straumann IO Scanner 연동 — 10월 출시 목표(역산·잠정) · 7/23 결정(IO Scanner 보류·1·2·3단계 우선) 반영
        dateFormat YYYY-MM-DD
        axisFormat %m/%d
        todayMarker stroke-width:3px,stroke:#d33,opacity:0.6

        section ③ GW SRS + API/DBML (계약 SSOT · baseline v1.0 동결)
        작성 (본문+OpenAPI·DBML)       :done, srsw, 2026-06-15, 28d
        PR 리뷰·수정                  :done, srspr, 2026-07-13, 2026-07-20
        baseline v1.0 (7/20 확정·spec-v1.0.1 정합화 7/22) :milestone, done, srsbl, 2026-07-20, 0d

        section GW 구현 → E2E → 출시 (③ SRS 완료 직후 착수 · 2단계 병행 · Raymond 부분투입)
        1단계 GW 독립 코어 (③ 고정·④무관·P0~P6·P10·진행중) :active, implindep, 2026-07-21, 45d
        2단계 AXS 연동 (P7~P12·④ AXS 보류 해제 후)   :implaxs, after implindep, 40d
        AXS E2E (sandbox)              :e2e, after implaxs, 14d
        개발환경 연동 완료(9월·R2)       :milestone, dev9, 2026-09-30, 0d
        v1.0 production 연동 완료(10월·R2·재검토) :milestone, rel, 2026-10-31, 0d

        section ③-I 인프라 IaC (① 초안+PR=Raymond → ② Jack 상세·리뷰·수정(PR #11973 병합 7/27) → 계획서 병합=완료·baseline tag 불요 · AWS dev·qa·stag·prod)
        ① 초안+PR (Raymond·diagram+요구추출) :done, infw, 2026-07-20, 2d
        ② Jack 상세작성·리뷰·수정 (PR #11973 병합 7/27) :done, infpr, 2026-07-21, 6d
        ③ 계획서 PR 병합 완료 (baseline tag 불요·living doc) :milestone, infbl, 2026-07-27, 0d
        Infra 구축·자동배포 완료(8월·R2) :milestone, infra8, 2026-08-31, 0d

        section ③-P-EZ EzServer 연동 스펙 (① 초안+PR=Raymond → ② Teddy 상세·리뷰·수정 → ③ baseline · IO Scanner부=보류)
        ① 초안+PR (Raymond·기본 GW연동) :done, ezw, 2026-07-20, 5d
        ② Teddy 상세작성·리뷰·수정 :active, ezpr, after ezw, 14d
        ③ baseline :milestone, ezbl, after ezpr, 0d

        section ③-P-CS CleverSpace OnePager (① 초안+PR=Raymond → ② CleverSpace팀(Larry) 상세·리뷰·수정 → ③ baseline)
        ① 초안+PR (Raymond·PR #12239·EzCloud) :done, cssub, 2026-07-27, 5d
        ② CleverSpace팀(Larry) 상세작성·리뷰·수정 :active, cspr, after cssub, 14d
        ③ baseline :milestone, csbl, after cspr, 0d

        section ③-P-CO CleverOne OnePager (① 초안+인계=Raymond·SharePoint → ② CleverOne팀(Nick) 상세·리뷰·수정 → ③ baseline)
        ① 초안+인계 (Raymond·SharePoint gw_adaptation) :done, cosub, 2026-07-27, 5d
        ② CleverOne팀(Nick) 상세작성·리뷰·수정 :active, copr, after cosub, 14d
        ③ baseline :milestone, cobl, after copr, 0d

        section ④ AXS Sub-SRS · IO Scanner (보류 — 7/23 결정: 0단계 IO Scanner 보류·Straumann 협상)
        IO Scanner↔EzServer 연동방식 확정(보류·선결·R1) :crit, ezm, after cosub, 21d
        작성 (IO Scanner scope · Straumann 협상 후) :axsw, after ezm, 21d
        PR 리뷰·수정                  :axspr, after axsw, 14d
        baseline                      :milestone, axsbl, after axspr, 0d
        AXS sandbox 자격(Straumann·선결) :crit, cred, 2026-08-18, 21d

        section ③-C GW Console v1.0 (Flow 최소기능·MS Entra·Istio admin·ZTNA · SRS 8/5 착수·전규현/Raymond)
        SRS 작성 (8/5 착수)            :active, consrsw, 2026-08-05, 6d
        SRS PR 리뷰·수정 (차주초)       :consrspr, 2026-08-11, 14d
        v1.0 최소 구현 (Flow 동작 최소) :conv1, after consrspr, 28d
        v1.0 최소기능 완료             :milestone, conv1m, after conv1, 0d
        section ③-C GW Console v2 (온보딩·Org 관리 화면 등 확장 — 후속)
        v2 확장 스펙+구현 (10월 중순 착수) :conv2, 2026-9-25, 28d
        baseline/확장 완료             :milestone, conv2m, after conv2, 0d

        section v1.0 이후 (deferred · post-v1.0)
        CleverOne 연동 *구현* (스펙은 지금·구현 post-v1.0) :codef, after rel, 14d

        section ▷ 병행 · 별도 프로젝트 (GW 아님)
        SectionView Module 구현 (Raymond·완료) :done, sv, 2026-07-13, 2026-07-30
    ```

  - **S2. 스펙 작성 테이블 — 제품별 개발 항목 종합 (제품 × 단계) · 매주 스냅샷** · 정본=[Roadmap §4](<VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>) (수정은 그쪽 먼저)
    - **각 셀 앞 이모지 = 그 항목을 다루는 스펙의 작성 진행**: ✅ baseline · 🟢 PR · 🟡 작성중 · ⬜ 미작성 (— = 해당 없음)

      | 제품 | 0단계(IO Scanner 수집·**보류**·R1) | 1단계(호환성) | 2단계(presigned) | 3단계(GW 일원화) | 4단계(멀티리전) | 5단계(Straumann) | 후속 | 스펙 산출물(단위·유형) |
      | --- | --- | --- | --- | --- | --- | --- | --- | --- |
      | **CleverSpace** | — | 🟡 서버 버전 체크·well-known·오류코드 | 🟡 presigned 발급 API 신규 | 🟡 GW 경유 수신 정합 | ⬜ 멀티 Region 구축 | — | — | **🟢 ③-P-CS CleverSpace OnePager 인계(PR #12239·EzCloud `docs/onepager/gw_adaptation`)** — CleverSpace 팀(Larry) 검토 |
      | **CleverOne**(OnePager 지금·연동 구현 post-v1.0) | — | 🟡 Vatech-\* 헤더·well-known·fallback | 🟡 presigned 업로드 이용 | 🟡 Direct→GW 경유 | ⬜ Region 선택 UI(대안)·ClinicID | — | — | **🟢 ③-P-CO CleverOne OnePager 인계(SharePoint gw_adaptation)** — CleverOne 팀(Nick) 검토 · 담당=Nick·작성=Raymond |
      | **EzServer(EZ)** | ⬜ IO Scanner 데이터 수신(방식 R1·**보류**·TBD) | 🟡 헤더 대리 전달 | 🟡 전송 로직(presigned 직접) | 🟡 GW 경유 전환 | 🟡 ClinicID·Region·클리닉 등록(잠정) | 🟡 AXS(갈래A)·presigned 직접(IO Scanner 세부=TBD) | ⬜ Rust 재개발 | **🟡 ③-P-EZ One Pager 초안 작성됨**(Raymond→EzServer 팀) — `specs/03p-ez-ezserver/EzServer-GW적응-OnePager.md` · ④(갈래A) |
      | **IO Scanner(Straumann 장비·수집 제품 미정)** | ⬜ 스캔 데이터→EzServer 유입(**보류**·수집 제품·방식 이월-R1·미정·Straumann 협상) | — | — | — | — | (AXS 워크플로 대상) | — | 이월-R1 확정 후 ③-P-EZ(수신)·④(AXS scope) |
      | **CleverLab** | — | — | — | — | — | ⬜ AXS 오더·상태·확정(갈래B)·presigned | — | ④ Sub-SRS(갈래B) |
      | **VatechAPIGateway** | — | 🟢 ↳3단계 흡수(호환 게이트·§7.7) | 🟢 ↳3단계 흡수(presigned 중계·§4.1.4) | 🟢 본체·라우팅·인증·호환·presigned 중계·경로B 흡수 | 🟢 리전 라벨 호스트·Region Directory·HA(K8s)·Route53·RDS(리전 단일) | ⬜ AXS OAuth 중계·Org-ID·온보딩·인바운드·고정IP | — | **③ SRS ✅ baseline(spec-v1.0.4)** · region-silo `spec-v1.0.5` PR 리뷰중 · ④ connector ⬜(보류) |
      | **GW Console** | — | — | — | — | 🟡 Admin Web Console v1.0 최소(MS Entra·Istio admin 제어·ZTNA 페이지 접근) | ⬜ 온보딩·Org-ID 관리 화면(v2) | — | ⬜ ③-C Sub-SRS v1.0 최소기능 **9월 착수 예정**(R5 당김 결정·전규현/Raymond) |
      | **인프라** | — | — | — | 🟢 dev·qa·stag(단일 Region)·prod(Region별) | 🟢 Route53·K8s·비-AWS minio | 🟢 AXS 고정IP·샌드박스 | — | **🟢 ③-I IaC 구축 계획서 — PR #11973 병합(7/27)·Jack 상세 반영**(Raymond diagram+SRS추출→Jack) — 정본 `vt-api-gateway-infra` · **baseline tag 불요**(living doc) · **AWS 4계층** · **+ 8/4 KMS 키 토폴로지 provisioning ask**(spec-v1.0.7·handoff-infra 항목5 — 리전별 CMK `gw-payload`/`gw-target-cred`·pod별 grant·dev payload CMK 선생성) |
      | **외부(Straumann AXS)** | — | — | — | — | — | ⬜ API·OAuth·샌드박스·자격증명(선결·**협상중**) | — | ④ 입력(외부 제공) |
      | **LMP(License Portal, 바텍)** | — | — | — | — | — | — | ⬜ (조건부) 제3자 서명 attestation | **enroll B안 시만**·ES 라이선스팀(R9·B-42) |

    - **스펙 문서 등록처·경로·baseline (SSOT)** — 각 제품 스펙 정본의 Repo·경로·태그. _(미정 = R3에서 등록처 확정 · OnePager는 담당팀 baseline 시 tag 부여)_

      | 단위 | 스펙 문서 | Repo (Azure DevOps) | 경로 | baseline tag |
      | --- | --- | --- | --- | --- |
      | **③ GW** | SRS(+OpenAPI·DBML·UnitTCL) | `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway` | `docs/specs/SRS.md` · `docs/specs/design/`(openapi·dbml) · `docs/specs/UnitTCL.md` | **`spec-v1.0.4`**(최신 baseline) · region-silo `spec-v1.0.5`(PR 리뷰중) |
      | **③-C GW Console** | Sub-SRS | `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console` (별도 repo·GW 소유→이관) | **작성 중(초안·경로=R3 확정 대기)** | **작성 중(8/5 착수)·차주초 PR 예정** |
      | **④ AXS** | Sub-SRS | 〃 vt-api-gateway (GW 소유) | `docs/specs/04-subsrs-straumann-axs/` | 미작성(보류) |
      | **③-I 인프라** | IaC 구축계획서 | `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-infra` | `docs/IaC-구축계획서.md` | **PR #11973 병합(7/27)** · baseline tag 불요(living doc) |
      | **③-P-EZ EzServer** | GW적응 OnePager | `https://dev.azure.com/ewoosoft/ezserver/_git/ezserver_suite` (branch `v6.5.x`) | `doc/onepager/gw_adaptation/Confidential_gw_adaptation_onepager.md` | 미부여(EzServer 팀 baseline 예정·R3 확인) |
      | **③-P-CS CleverSpace**(=EzCloud) | GW적응 OnePager | `ezicloud/ezcloud`(https://dev.azure.com/ewoosoft/ezicloud/_git/ezcloud) | `docs/onepager/gw_adaptation/CleverSpace-GW적응-OnePager.md` | **PR #12239**([링크](https://dev.azure.com/ewoosoft/ezicloud/_git/ezcloud/pullrequest/12239))·팀 baseline 예정 |
      | **③-P-CO CleverOne** | GW적응 OnePager | SharePoint `ProjectDoc/Clever One/srs/OnePager/gw_adaptation`([문서](https://vatechcorp.sharepoint.com/:t:/s/es/IQC500caygYpS78euV2xO5WyAfzZF2kbz_09J20UbackH2k?e=tQLWOJ) · [폴더](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Forms/AllItems.aspx?id=%2Fsites%2Fes%2FProjectDoc%2FClever%20One%2Fsrs%2FOnePager%2Fgw%5Fadaptation&viewid=5a018594%2D6322%2D4139%2Db7ee%2De9dd4aa4d23a&p=true&ga=1)) | 〃(SVN 제품·git 아님) | — (SharePoint·team baseline) |
      | **③-P-LMP LMP** | OnePager(조건부) | **미정 (ES 라이선스팀?)** | — | — |
      | **CleverLab** | ④ Sub-SRS(갈래B) | 미정 (보류) | — | — |

      > **진행 배경 (누적·상시)**
      >
      > - **0단계 IO Scanner·④ AXS = 보류**(Straumann↔ES 데이터 흐름 협상) → **1·2·3단계 우선**.
      > - **③-P-CS CleverSpace·③-P-CO CleverOne OnePager 2개**(각 1·2·3단계=호환성+presigned+GW일원화 통합) **= Raymond·7/27 병행 착수**(deferred→active · CleverOne Nick→Raymond → 담당팀 전달).
      > - **①호환성·②Presigned One Pager 별도 미작성 → 두 제품 OnePager에 흡수**(딱 2개 문서 · presigned=CleverSpace 발급 API+CleverOne 이용, 둘 다 GW 경유라 양쪽 변경).
      > - ③ GW SRS = **baseline v1.0 동결(7/20)·spec-v1.0.1 정합화(7/22)**.
      > - ③-I Infra = **PR #11973 병합 완료(7/27)**(Jack 상세·baseline tag 불요·living doc) · ③-P-EZ EzServer 초안 = Raymond→Teddy 상세.
      > - **AWS 환경 4계층(dev·qa·stag·prod)** 결정 반영.
      > - CleverOne OnePager는 지금 작성(연동 *구현*만 post-v1.0).
      > - 순서·의존 = [Roadmap §3.9].

  - **S3. GW 구현 현황 — Phase·Task 스냅샷 (8/13·매주 갱신)** — 1단계 코어 완료 · 2단계 P8·P9·P11 완결 · 인증 v1.0.11 보강 중.
    - **어디까지 왔나 (8/13)**: 1단계 코어(P0~P6·P10) 완료. 2단계는 **P8 골격(8-1·8-2·8-3) + P9 골격 app-side(9-1·9-2·9-3) + P9-4 drain + P11 Admin CRUD 전부(11-1~11-6 머지) 완결** — 로컬 더블 기준, 실연동은 ④ AXS 후. **인증 보강**: v1.0.11로 JWKS 엔드포인트 v1.0 승격 → **T-AUTH-2-6 완료(#12478)**(공개키 게시+토큰 claim 정합·개인키 미노출·외부 검증 시뮬). **④/인프라 무관 자율 가능 범위 소진**(9-4·12-2 후보 처리: 9-4 app-side 완료·12-2 compat E2E는 게이트 미배선(① One Pager 매트릭스)으로 블록). **남은 것 = P7(External Connector·AXS)·9-5(IoT)·P12-1(sandbox E2E)=④ AXS 실자격 선결 · 9-4 실 KEDA·0-5 잔여(자동배포)·P12-4=③-I 인프라(Jack) · P12-2(compat E2E)=① One Pager 매트릭스 확정 · P12-3(부하)=부하환경 · P7 골격(7-1/2/4/5)=로컬 더블 선행 가능(보류).** 구현 다음 통합·검증·QA 단계가 이어진다.
    - 매 Task 완료 시 갱신.
    - **진행 단계** — 스펙(분석/설계)과 구현을 분리해 진행한다. 스펙은 HLD로 baseline 동결됐고 현재 구현(LLD 병행) 중이다. 구현이 끝이 아니라, QA 인계 전 개발팀이 통합·시스템 테스트로 동작을 확증하는 단계가 남고, 이어 QA·운영이 있다.
      - **스펙 — 분석/설계(HLD)**: SRS·DBML·OpenAPI·TCL baseline v1.0 동결 · 정합화(v1.0.1~v1.0.4) 지속 · LLD는 구현과 병행
      - **구현(LLD 병행)** — _구현 단계 내 진척(코딩 Task) · region-silo 재작업(8/3·PR #12241) 완료로 **P4 대부분 삭제·단일화** → Task 집합 축소·재산정 예정_: 1단계 코어 **P0~P6·P10 완료 + region-silo 재작업 완료** · 2단계 **P8 골격 완료(8-1·8-2·8-3)·P9 착수(9-1)** / P7·P11·P12는 ④ 연동 Spec 후 · Task별 검증 4종(unit·e2e·curl·DB)
      - **✅ region-silo(R2·spec-v1.0.5/1.0.6) 재작업 완료(8/3·PR #12241 머지 `9146ae3`)**: 아래 ✅완료 중 **P1 T-DATA-1-1(전역/리전 2-DB)·1-6(region_catalog 시드) · P3 T-ENR-3-2(GeoDNS default region 배정) · P4 전체(Region Resolver·GET /v1/regions·PUT /me/region·region 카탈로그 CRUD) · P6 T-PXY-6-2의 region 해석 단계**가 리전 완전 분리로 **삭제·단일화됨**(단일 datasource·region=배포 상수·Region Directory·리전 변경=마이그레이션·ClinicResolution=리전 echo·하드 FK). **완료 이력은 아래 표에 보존**(당시 PR 기준)하되 현행 코드는 단일 datasource. 검증: unit 534·e2e 157·CI green(build 20260803.1)·`verify-spec`/`verify-ci` 게이트 신설.
      - **개발 통합·검증(QA 인계 전)**: 통합 테스트 · 시스템 E2E(실 계약: AXS·CleverSpace·EzServer) · 성능·부하 · HA·복원력 · 보안 검토 → 동작 확증 후 QA 인계
      - **QA**: 릴리스 회귀 · QA TCL · V&V 산출물(IEC 62304 / ISO 13485)
      - **운영·릴리스**: staging/prod 배포(인프라) · AXS pilot
    - **상태 범례**: ✅ 완료(main merge) · 🟢 리뷰중(PR) · 🟠 구현중 · ⬜ 대기 · 🔴 외부 선결 대기. **표기 규칙**: **7/30 이전 완료분 = Phase 단위 묶음 · 7/30 이후 구현(region-silo 재작업) = Task 단위 전개 · 미착수 = Phase 단위.**

      **① 7/30 이전 완료 — Phase 단위 (묶음)**

      | Phase | Task 범위 | 상태 | 대표 PR |
      | --- | --- | --- | --- |
      | **P0 플랫폼 스캐폴드** | 0-1~0-6 (4-way 스캐폴드·로컬환경·포트어댑터·더블·Prisma·관측·에러·Config·헬스·README·**CI·Dockerfile**) | ✅ 완료 | #11971~11995 · **CI=`azure-pipelines.yml`(우리)** · **CD=`.azure-pipelines/`(Jack·devsecops 4앱+promote)** |
      | **P1 데이터 모델·마이그레이션** | 1-1~1-7 (스키마·raw-SQL 제약·KMS envelope·Redis 키스페이스·audit append-only·시드 하네스) | ✅ 완료 → **8/3 단일 datasource 재작업(②)** | #12006~12040 |
      | **P2 인증 토대** | 2-1~2-5 (device private_key_jwt→RS256 + operator Entra OIDC·RBAC) | ✅ 완료 | #12094~12143 |
      | **P3 enrollment·생애주기** | 3-1~3-5 (개시/완료·상태머신·재-enroll 회전·C/S 승인·kill·pending 자동만료) | ✅ 완료 → **region 배정 삭제(②)** | #12158~12171 |
      | **P4 레지스트리·region resolution** | 4-1~4-5 (Resolver·ClinicResolution·PATCH/PUT me·PHI PDP·카탈로그 CRUD) | ✅ 완료 → **region-silo로 대부분 삭제·단일화(②)** | #12173~12191 |
      | **P5 호환성 게이트** | 5-1~5-3 (Vatech-\* 파싱→400·well-known 서빙·semver 게이팅) | ✅ 완료 | #12194~12200 |
      | **P6 target-routed 프록시** | 6-1~6-3 (라우터·SSRF·PEP 체인·verbatim bypass·복원력) | ✅ 완료 → **region 해석 단계 삭제(②)** | #12203~12213 |

      > **T-PLAT-0-5 확정(8/3)**: 우리 CI(`azure-pipelines.yml`·lint/build/unit/e2e/scan)+Dockerfile **완료** · 배포(CD)는 Jack `.azure-pipelines/`(devsecops 4앱+promote-qa/prod) **별도 소관·운영 중**(dev 배포됨). 옛 "🔴 배포 Jack 템플릿 수령 후" blocker 해소 → **P0 전체 ✅**.

      **② 7/30~8/3 구현 — Task 단위 (풀기) · region-silo 재작업(R2·PR #12241 머지 `9146ae3`)**

      | Task | 내용 | 상태 | 검증 |
      | --- | --- | --- | --- |
      | 스키마·마이그레이션 | 전역/리전 2-DB → **단일 datasource** · baseline squash · 하드 FK · NULLS NOT DISTINCT · audit append-only 트리거 | ✅ 완료(8/3) | migrate deploy·정적/실DB e2e |
      | config·리전 상수 | `GW_REGION` 배포 상수 · `DATABASE_URL` 단일 · `GW_PUBLIC_HOST` · 앱별 단일 PrismaService | ✅ 완료 | config unit |
      | API·런타임 | **Region Resolver·GET/PUT `/v1/regions`·region_catalog CRUD·GeoDNS 배정 삭제** · ClinicResolution=리전 echo · proxy PEP region 해석 제거 | ✅ 완료 | e2e·curl |
      | 테스트·감사 | e2e/unit 재정합(**534/157**) · 9-파티션 전수 정독 감사 · 폐기개념 grep 0 · **CI e2e 401 회귀 수정**(token aud=config 동기화) | ✅ 완료 | 검증 4종·CI green |
      | 게이트·문서 | `make verify-spec`·`verify-ci` 신설 · README 드리프트 정정(#12348) | ✅ 완료 | — |

      **②-b P10 fleet·config·inventory — Task 단위 (8/3 완결 · 1단계 마무리)**

      | Task | 내용 | 상태 | PR |
      | --- | --- | --- | --- |
      | 10-1 heartbeat | POST /v1/fleet/heartbeat·fleet_state upsert·nextIntervalSeconds·device_id=토큰 subject·metrics 미저장 | ✅ 완료 | #12363 |
      | 10-2 ConfigService | 중앙 config(gw.*) 실효 resolve(device>clinic>region>global)·pull 엔드포인트·configVersion는 gw/1.1 이월 | ✅ 완료 | #12364 |
      | 10-3 inventory | 클라 SW 인벤토리 튜플 presence·os sentinel·Redis SET NX throttle·fire-and-forget | ✅ 완료 | #12366 |
      | 10-4 admin 조회 | GET /v1/admin/fleet·/clients·/clinics/{id}/clients·online 파생·cursor 엔벨로프·RBAC | ✅ 완료 | #12368 |

      **②-c P8 webhook 수신(Receiver) — Task 단위 (8/3~ · 골격 3종 완료 · 2단계 head-start · 로컬 더블)**

      | Task | 내용 | 상태 | PR |
      | --- | --- | --- | --- |
      | 8-1 HMAC 검증·골격 | Host/inbound_host 식별(→404)·HMAC+timestamp 검증(replay 방지·timestamp-binding)·Receiver 골격·즉시 202 ACK | ✅ 완료 | #12369 |
      | 8-2 멱등·payload 암호화 | eventId 멱등(PK·P2002 dedup·중복 0)·store-then-ack·**payload 전용 CMK envelope 암호화·평문 미저장**(키 §7.1.3.1 분리·Jack 승인·spec-v1.0.7) | ✅ 완료 | #12411 |
      | 8-3 SQS enqueue | 저장 후 eventId claim-check 적재(body=eventId만·재시도·store→ACK→enqueue·isNew만) | ✅ 완료 | #12414 |

      > **P8 비고**: 2단계 head-start(④ AXS 실연동 전 로컬 더블로 선행) · **dev 실검증 = Jack payload CMK provisioning 후**(배포-시점 의존) · 8-3 후 실연동은 ④ 후.

      **②-d P9 webhook 분배(Dispatcher) — Task 단위 (8/4~ · 골격 app-side 3종 완료 · 2단계 head-start · 로컬 더블)**

      | Task | 내용 | 상태 | PR |
      | --- | --- | --- | --- |
      | 9-1 SQS 소비·대상해석·DLQ | SQS(eventId) 소비→**(target_id,external_org_id) 복합키** org_mapping→clinic→payload 복호→MQTT publish(gw/clinic/{clinicId}/webhook·qos1)→dispatched · 미해석=**발행 전 fail-closed dead_letter**(교차클리닉 오분배 차단) · 멱등 | ✅ 완료 | #12420 |
      | 9-2 MQTT QoS1·verbatim | 하행 발행 정형화: 토픽 화이트리스트 검증(위험문자 거부·fail-closed·리전 미포함)·QoS1·원 payload verbatim | ✅ 완료 | #12434 |
      | 9-3 DLQ·재전달·멱등 | attempt-cap 백오프→dead_letter·eventId 멱등(중복발행0)·브로커 장애 SQS 잔류 무유실(오프라인 publish 무한 hang 수정=timeout) | ✅ 완료 | #12437 |
      | 9-4 KEDA 오토스케일 + drain | app-side graceful scale-in drain(무유실·offline-hang 강제종료·drain 순서 보장) 완료 · KEDA config 참조 매니페스트 | 🟢 app-side 완료(#12471) | 실 KEDA 스케일 검증=③-I(Jack) |
      | 9-5 device IoT 프로비저닝 | Thing/cert·enroll 확장 | ⬜ 대기 | ④ AXS/IoT Core |

      > **P9 비고**: full-loop(수신→저장→분배→Mosquitto 구독자 더블)을 로컬로 그린(9-1) · 동반 = **런타임 dep 분류 가드 신설**(소스 devDep import 시 CI 실패·GATE 1b) · dev 실검증·실연동은 ④ AXS 후.

      **②-e P11 Admin API·레지스트리·audit — Task 단위 (8/5~8/6 · ④ 무관·자율 · 구현 완료: 11-1~11-6 전부 머지 · 코어 P0~P6 인증/DB 위에 관리면 축조)**

      | Task | 내용 | 상태 | PR |
      | --- | --- | --- | --- |
      | 11-1 targets CRUD | 연동 대상(라우팅+아웃바운드 자격+인바운드 webhook) 통합 1레코드 CRUD · write-only 자격/시크릿→**KMS wrap**(target-cred 전용 CMK)·응답은 KMS 참조 포인터만(**원문·암호문 미노출**) · 종속(매핑·정책·이벤트) 삭제 **409** · 부재보존 병합(운영 필드 조용한 소실 차단) | ✅ 완료 | #12441 |
      | 11-2a policies CRUD | 인가 정책(deny-by-default 허용 SSOT) 등록/조회/삭제·**자연키 upsert**(동시경합 1행 원자성)·부재보존 병합·targetId FK 400·scopeId 형식검증·감사 | ✅ 완료 | #12443 |
      | 11-2b config·org-mappings | 중앙 config(PUT 멱등·version 값변경시만++·updated_by 서버강제·NULLS NOT DISTINCT)·Org-ID↔ClinicID 매핑(복합PK·mapping_version++·이중 FK 400·복합키 커서)·감사 | ✅ 완료 | #12444 |
      | 11-3 operators·RBAC 생애주기 | 운영자 목록/상태·역할 생애주기 상태머신(직접부여·승인/거부/회수·행 보존)·self access-request·승인 큐·**마지막 admin 회수 409**(advisory lock 원자화·동시 회수→하나만·v1.0.10)·회수후 재부여(partial unique) | ✅ 완료 | #12456 |
      | 11-4 webhook-events + break-glass | 이벤트 메타 조회(PHI-free·필터·커서)·단건·**본문 열람(break-glass·KMS 복호·PHI masking·전량 감사)** · RBAC 티어(메타=read·payload=admin) · 복호 평문 유출 차단 | ✅ 완료 | #12459 |
      | 11-5 audit 전면 커버리지 | GET /v1/admin/audit(actor/action/result/시각범위 필터·id DESC 커서·조회전용·RBAC admin)·**전 write 경로 감사 전수(14 엔드포인트·누락 0)** — device 전이·kill 감사 누락 보완(성공 시만·actor 위조차단·PHI 없음) | ✅ 완료 | #12469 |
      | 11-6 데이터 분류·크로스보더 동의 | 경량 스캐폴드(v1.0 단일리전 no-op·gw/1.2 활성)·크로스보더 재동의 판정·자동이관 없음·consent 이력 audit·엔드포인트 없음 | ✅ 완료 | #12470 |

      > **P11 비고**: ④ AXS 실연동과 무관한 **관리·레지스트리·감사면**이라 자율 진행 중(코어 P0~P6 인증/RBAC/DB 완료가 선결이라 지금 가능). 11-1 이 target-cred CMK(§7.1.3.1 키 #3·payload 키와 별개)·secret-ref 코덱(libs/common 승격·admin write·receiver read 계약 단일화)을 도입 — Jack `alias/gw-target-cred-<region>` prod provisioning 후속.

      **②-f P2 인증 보강 — v1.0.11 정합화 (8/13~ · JWKS v1.0 승격)**

      | Task | 내용 | 상태 | PR |
      | --- | --- | --- | --- |
      | 2-6 JWKS 공개 + 토큰 claim 정합 | `GET /.well-known/jwks.json`(무인증·RS256 공개키·kid·Cache-Control·회전 구·신 동시게시·개인키 미노출)·외부 검증자(CleverSpace GW Guard)용 · 토큰 `iss=https://api.<region>.gw.<도메인>`·TTL≤15분 상한·`aud`=GW수준 정합 | ✅ 완료 | #12478 |

      > **②-f 비고**: v1.0.11(#12440)이 JWKS 엔드포인트를 **gw/1.2 백로그→v1.0 승격**(외부 검증자 실재). 비대칭 RS256·kid·공개키 JWK 파생은 이미 T-AUTH-2-1에 있어 **공개키 게시 + claim 3건 정합만 추가**(기존 토큰·개인키·검증 재작업 0). 리전 apse4→apse2·Console 전역은 config/타 소유(코드 무영향).

      **③ 2단계 — Phase 단위 (대기)**

      | Phase | 범위 | 상태 | 비고 |
      | --- | --- | --- | --- |
      | **P7 External Connector·AXS** | OAuth2 cc·egress 고정IP·앱 PDP egress·org-binding·presigned 중계 | ⬜ 대기 | 🔴 2단계·④ AXS 실연동 후(보류) |
      | **P11 Admin API·audit·컴플라이언스** | 전 CRUD·RBAC 생애주기·break-glass·audit 전면 | 🟢 완료(11-1~11-6 전부 머지·②-e) | ④ 무관·자율 완결 |
      | **P12 E2E·하드닝** | AXS sandbox E2E·compat E2E·부하·HA/KEDA 검증 | ⬜ 대기 | 🔴 2단계·④ AXS sandbox 실자격 |

      > **직전 주(7/30) 구현 요약 · P2~P6 완결** — 1단계 GW 독립 코어에서 **P2~P6 다섯 Phase를 완결**했다. **P2 인증**: device 면(2-1 private_key_jwt→RS256 토큰, 2-2 jti 1회 소비·검증후 정본 clientId rate-limit·revocation denylist, 2-3 deviceAuth Guard)에 operator 면(2-4 Entra OIDC+confused-deputy 방어+JIT, 2-5 RBAC deny-by-default+`/v1/admin/me`)을 더해 양 인증면을 완비. **P3 enrollment**: 개시/완료(3-1·3-2)에 이어 device 생애주기 상태머신·재-enroll 회전 옛 credential 폐기(3-3)·C/S 승인 slice+kill 즉시 denylist 전파(3-4)·미승인 pending 자동만료(3-5)로 종료. **P4 레지스트리·region resolution**: Region Resolver(mapping_version CAS·버전 조건부 캐시·4-1)·ClinicResolution+GET /v1/regions(4-2)·PATCH /me+PUT /me/region(4-3)·PHI region-boundary 앱 내부 PDP(4-4)·admin region 카탈로그 CRUD(4-5)로 완결. **P5 호환성 게이트**: Vatech-\* 파싱→400(5-1)·well-known 매트릭스 서빙(5-2)·semver 3단계 게이팅 guard(5-3). **P6 target-routed 프록시**: 서브도메인 라우터+SSRF fail-closed(6-1)·PEP 체인(auth 401→PDP 403→region)+verbatim bypass(6-2)·아웃바운드 복원력(6-3 D1~D3 타임아웃·취소 전파·에러 정규화·Idempotency-Key)로 완결. 모든 엔드포인트 Task에 **검증 4종(unit·e2e[실 DB·Valkey]·curl 왕복·DB/Valkey 조회)** 과 **E2E 반복성 하네스**(clean-slate·seed·FLUSHDB)를 적용했고, 보안 민감 Task(프록시·인증)는 **독립 적대적 pre-PR 리뷰**로 검증했다. (region-silo 재작업 상세는 위 ② Task 테이블 참조.)

  - **S3-1. 커버리지 현황 (구현과 분리 · merged=unit+e2e 합산 · 8/13 측정·post-T-AUTH-2-6 · 매 Task 완료 시 갱신)** — 커버리지 스윕(1·2·3순위 101 케이스·PR #12372) 후 실측, 이후 Task마다 재측정. 정본 기준 = **merged**(단위+통합 합산).

    | 스코프 | Statements | Branches | Functions | Lines |
    | --- | --- | --- | --- | --- |
    | **① 전역 (merged)** | **96.63%** | **92.41%** | **93.36%** | **96.42%** |
    | **② 보안 도메인 (merged)** | **98.60%** | **96.00%** | **100%** | **98.50%** |
    | **③ 핵심 보안 파일 16개 (merged·개별)** | — | **각 100%** | — | — |
    | _참고: 전역 (unit-only)_ | 77.73% | 83.02% | 72.15% | 78.73% |
    | **CI 게이트 floor — ① 전역** | 92 | 87 | 88 | 92 |
    | **CI 게이트 floor — ② 보안** | 95 | 89 | 95 | 95 |
    | **CI 게이트 floor — ③ 핵심파일(개별·branch)** | — | **90** | — | — |

    - **추천 기준값 (= 위 표의 'CI 게이트 floor' 행 · 회귀 방지 하한)**:
      - _① 전역 · ② 보안(합산)_: 재앙적 회귀 catch용 하한(달성치 대비 여유 有). 달성치 상승 시 floor 도 올려 개선을 잠금(**ratchet**).
      - _③ 핵심 파일(개별·branch ≥90)_: **규범적(실질 요구수준)** — 합산이 못 잡는 단일 파일의 보안 분기 공백을 차단. 현재 16개 전부 100%. 미커버는 (A)도달가능→테스트 / (B)도달불가→`istanbul ignore`+실증근거로만 처리(숫자 치팅 금지·적대 감사로 부당 ignore 색출·수정).
      - _수준_: 업계 통상(라인 ~80% · 분기 70~80%가 "양호")보다 높음 · 가장 엄격한 **Branch 를 전역 92.4 / 보안 96.0% 달성**.
      - _한계_: %는 필요조건일 뿐 — 본 스윕은 **적대적 mutation testing**(방어 로직 역전 → 테스트 red 확인)으로 회귀 포착력까지 검증.

    - **CI 게이트·조회**:
      - **게이트(차단)**: CI `GATE: merged coverage floor (unit+e2e)` 스텝이 전역/보안 8개 값 중 하나라도 floor 미달이면 **비-0 종료 → PR 머지 차단**(required check). _실증: 빌드 49327이 이 게이트에서 실패해 막혔다가 수정 후 통과._
      - **조회 — 로그**: PR → **CI verify** → **`Verify gates`** 잡 → **`GATE: merged coverage floor (unit+e2e)`** 스텝 로그에 Coverage summary + floor 대조표 출력.
      - **조회 — UI**: 빌드 **Coverage 탭**(`PublishCodeCoverageResults`·cobertura) — %·파일별·추세 시각화.
      - **로컬 재현**: `make coverage-merged`.

    - **범례**:
      - **지표(4열)** — "해당 요소 중 테스트가 1회 이상 실행한 비율(%)":
        - **Statements(구문)**: 실행 가능한 개별 구문의 실행 비율(기본 지표·코드 대부분에 대응).
        - **Branches(분기)**: `if`/`switch`/삼항/`&&`·`||`·`??` 조건 분기의 **각 방향(true·false)** 실행 비율 — **가장 엄격**, "정상만 타고 오류·fail-closed 경로 미검증" 공백을 드러냄(보안 척도).
        - **Functions(함수)**: 정의된 함수·메서드 중 1회 이상 호출된 비율.
        - **Lines(라인)**: 실행 가능한 소스 라인의 실행 비율(Statements 와 유사·물리 라인 기준).
      - **스코프 — 점점 좁고 엄격한 3단계(포함관계·중복 아님: 전역 ⊃ 보안 도메인 ⊃ 핵심 파일)**:
        - **① 전역**: 앱 전체(`apps/**` + `libs/**`) **합산** — "레포 전반이 안 무너졌나". 가장 넓고 느슨.
        - **② 보안 도메인**: 6개 보안 폴더(`auth`·`authz`·`enroll`·`proxy`·`webhooks`·`crypto`) **합산** — ①의 부분집합. PHI·자격증명·게이팅 민감 경로라 **전역보다 높은 floor**.
        - **③ 핵심 보안 파일**: ② 안의 **보안 결정 파일을 파일별(개별)로** 검사(합산 아님·branch floor **≥90**). **왜 별도인가**: 합산(①②)은 자잘한 covered 코드가 많으면 **한 파일의 보안 분기 공백을 가릴 수 있다** — 파일별 게이트라야 "auth.service 하나가 무너져도" 잡는다. 미커버 중 **도달불가 방어 분기는 `istanbul ignore`+근거로 제외**해 reachable 기준으로 관리. **대상 목록**: `auth.service`·`device-token.verifier`·`signing-key.provider`(토큰 발급·검증), `hmac.guard`·`json-path`(webhook 인증·파싱), `kms-envelope`(PHI 암호화), `egress-allowlist`·`pdp.service`·`policy-resolution`(인가·SSRF), `enroll.service`·`enroll-complete.service`·`enroll-ip`·`pending-expiry.job`(enrollment·nonce), `proxy.service`·`router`·`proxy-timeout`(프록시 라우팅·타임아웃).
        - **참고: 전역(unit-only)**: 단위 테스트만의 수치. 컨트롤러·가드·미들웨어·local 어댑터가 0%로 잡혀(그 계층은 e2e로 커버) 낮음 — merged 가 정본임을 보이는 대조치.
      - **merged**: unit + e2e(실 DB/Valkey) 합산(nyc) — 두 실행을 합쳐야 "실제 실행·검증된" 라인이 정직하게 집계됨. 현재 테스트 규모 = **unit 841**(receiver store/sqs·dispatcher consumer 신규 포함) · e2e 는 webhook 저장·enqueue·**분배 full-loop(SQS→Mosquitto 구독자)** 포함. _표의 % 는 8/4 스윕 실측 기준값(이후 소규모 Task 델타는 자잘하며, 보안 per-file floor 유지)._

  - **S4. 리전 자동 결정(country→region) 스펙 반영 (정보 공유)**
    - 온보딩 시 EzServer가 **리전을 직접 고르지 않고**, Region Directory의 리전별 담당 국가(`countries`) 매핑으로 **자기 클리닉의 나라(LMP 라이선스/Clinic-ID)에 맞는 리전을 자동 결정**(R6).
    - 지연(GeoDNS) 추천이 아니라 **주권상 결정적 매핑** + C/S 승인 검증.
    - **v1.0은 production 단일(호주)이라 자명 → 실효는 gw/1.2 멀티리전**(당장 blocker 아님).
    - 반영: SRS §2.3.1(온보딩·다이어그램)·§7.3.6(Region Directory `countries` 필드·규칙·JSON 샘플)·§7.3.1 + EzServer handoff · spec-v1.0.6(미커밋·누적).

  - **S5. 이번 주 완료·확정 상세 (참고 · 논의 대상 아님 · 진행 요약의 근거)**
    - **(8/3 완료) R2. GW 저장소 = 리전 완전 분리 — 스펙 + 구현 코드 모두 완료** _(결정 상세는 7/30 스냅샷 R2)_
      - **스펙**: SRS·DBML·OpenAPI·env-reference·well-known·크로스팀 handoff 전면 개정 + 자동 코드리뷰 11라운드·Jack 인프라 리뷰 전건 반영(미해결 0) → PR #12207 머지(`a0d1600`·`spec-v1.0.5`) + #12231 머지(`9cc08fa`·`spec-v1.0.6`)(7/30). **변경 규모 = 12 files · +477 / −676 라인(순 −199)** — SRS +281/−253 · OpenAPI +57/−254 · DBML +32/−53 · UnitTCL +28/−62 · 기타(env-reference·well-known·handoff 등) +79/−54.
      - **구현 코드**: PR #12241 머지(`9146ae3`·8/3) — 전역/리전 2-DB→단일 datasource·region=배포 상수·Region Resolver/리전 API(GET·PUT `/v1/regions`)/region_catalog CRUD 삭제·하드 FK·ClinicResolution=리전 echo. **변경 규모 = 139 files · +1,685 / −5,538 라인(순 −3,853)** — 앱 소스 65f · 테스트 46f · 설정·문서 23f · 마이그레이션/생성물 5f. 대량 삭제 = 2-DB·resolver·리전 API 복잡도 제거.
      - **검증**: unit 534 · e2e 157 · CI green(build 20260803.1) · `verify-spec`/`verify-ci` 게이트 신설 · README 드리프트 정정(PR #12348). 후속 = IP Spec Index·체크박스 갱신.
      - **PR**: [구현 #12241](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/12241) · [스펙 #12207](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/12207)
    - **R2-1. 호주 first-open 리전 전략 — ✔ 확정**
      - v1.0 production 리전 = **호주 멜버른(ap-southeast-4·`apse4`)** · **서울(apne2) = 비-prod 전용**(dev·test·staging). 호주 클리닉을 서울에 임시로 두지 않음. _(8/4 ③-I 확정: 비용 우위로 시드니 ap-southeast-2 대신 멜버른 ap-southeast-4 — spec-v1.0.8 교정)_
      - region silo라 production은 리전별 독립 스택 1개씩(서울 production은 추후 추가 가능).
      - '서울 임시 홈 → 호주 이전'(리전 통째·대량 이전) 시나리오 없음 — 호주 클리닉은 처음부터 호주 리전 온보딩(PHI residency).
      - 스펙 영향: SRS §2.3.9 호주 임시-홈 예시 v1.0 제외(gw/1.2 재홈 역량만 존치)·기준 리전=호주 멜버른(dev=서울) — spec-v1.0.6 + 리전 라벨 apse4 교정 spec-v1.0.8.
      - 유지: AXS webhook 콜백 org(클리닉)별 세분화 요청 계속.
    - **R3. 제품 OnePager(③-P) 인계 — ✔ 방식 확정**
      - CleverSpace(=EzCloud·git): PR 인계 완료 — `ezicloud/ezcloud`·`docs/onepager/gw_adaptation/CleverSpace-GW적응-OnePager.md`(정정본)·**PR #12239**(`d3f676a0`)·통지 Larry(고형용).
      - CleverOne(svn): SharePoint 폴더 인계 완료 — `ProjectDoc/Clever One/srs/OnePager/gw_adaptation`(작성 Raymond)·통지 Nick(탁수용).
      - EzServer: Teddy 수령·PR 착수 확인(`ezserver_suite/doc/onepager/gw_adaptation`).
    - **R4. GW 도메인 별도(vatech.com 미사용) — ✔ 확정**
      - vatech.com은 이메일 도메인이라 GW 관리 어렵고 혼란 소지 → GW는 별도 도메인(구체 도메인 지정 예정·③-I).
      - 스펙 반영(완료·미커밋): GW 호스트 예시 `…gw.vatech.com` 34곳 → `gw.<도메인>` 플레이스홀더. `vks.vatech.com`·이메일 `@vatech.com`은 유지.
    - **R5. GW Console v1/v2 분리 · v1.0 최소기능 선행 — ✔ 확정(전규현/Raymond)**
      - Console이 있어야 온보딩·디바이스 승인 Flow가 돎 → v1.0 = Flow 동작 최소 스펙으로 착수 앞당김(v2 후속).
      - v1.0 범위: 인증=MS Entra · Istio admin API 접근제어 · 페이지 접근 ZTNA.
      - 소유=전규현/Raymond · 일정 v1.0 9월 착수(~28d)·v2 10월 중순(~10/15).

- 이월 논의 사항 (6/25·7/2·7/9 미결 — 계속)

  | # | 항목 | 타입 | 상태 |
  | --- | --- | --- | --- |
  | 4 | Webhook 클라우드 분배(CleverLab 갈래B) | [논의] | v1.0 제외 — Open 후 결정 |
  | 6 | AXS sandbox 자격증명(Straumann 제공) | [정보] | pilot·E2E 블로커 — 확보 시점?(협상중) |
  | 7 | 경로 B EOS 시점 | [논의] | 리뷰서 workaround·지속성 확정(§2.8) — EOS *시점*만 PM·CS/CO OnePager 미정(①흡수) |
  | 8 | v1.0 목표 RPS·동시 세션 | [정보] | 인프라/규모 PL 입력 대기 |
  | 9 | RTO/RPO·유지보수 윈도우 | [정보] | 인프라 설계 단계 — failover 요건은 R2(저장소 전역일관 vs 리전분리·Q3) 결정과 연계 |
  | 10 | 감사·consent 보존 기간 | [정보] | 법무 확인 대기 |
  | 11 | 호환성 매트릭스 확정본 | [정보] | CleverSpace/CleverOne OnePager 의존(①폐지·흡수) — 초안 7/27 작성·확정값은 담당팀 baseline 후 |
  | 14 | 관측성 앱↔인프라 계약 확정 — ①로그 필드 스키마(현행 pino 기본 필드 ↔ §6.3.2 최소셋 매핑·Appendix B #14) ②메트릭 export 배선(OTLP reader→Grafana Alloy 엔드포인트) | [논의·설계] | **추후 확정** — 트리거=③-I 관측 스택 구축 or P6 프록시 착수(먼저). Raymond 초안(필드 매핑표+엔드포인트 요구)→Jack(인프라) 비동기 합의. **앱 계약(stdout JSON+OTel·redaction) 이미 구현·무블로킹** |
  | 이월-R1 | IO Scanner↔EzServer 연동 방식 | [논의·선결] | **보류(7/23 결정)** — 이번 주 논의 「Straumann↔ES 데이터 흐름 협상」 결과에 종속(결정 시 이월-R1·④ AXS scope 착수 조건 확정) |
  - **차주 이월 후보**: 이월-R1(IO Scanner↔EzServer 연동 방식·**보류**)·이월-R2(목표일정·출시일 재검토) 미확정 시 다음 주 이월.
