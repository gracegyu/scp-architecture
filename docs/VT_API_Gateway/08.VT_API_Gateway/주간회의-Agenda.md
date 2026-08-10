# VT API Gateway — 8/13 주간회의 Agenda

> **과거 주차(6/25~8/6)는 [`주간회의-Agenda-Archive.md`](주간회의-Agenda-Archive.md)로 이관·보존**(가끔 조회용). 본 문서는 **8/13 현행 주차만** 유지한다. 틀(논의/공유/이월)은 이전 주와 동일하며 **Gantt(S1)·스펙 작성 테이블(S2)은 매주 상시 포함**한다. _※ `(프레임)` 표시 항목은 8/13 회의 시 확정한다._

- 이번 주 진행 _(프레임 · 8/13 회의 시 확정 · 상세·수치는 아래 논의 R#/공유 S# 한 곳에만)_
  - **(8/6~8/13 완료) GW 자율 구현 범위 완결** — **P11 Admin CRUD 전 Task 완료**(11-1~11-6 머지: targets·policies·config/org-mappings·operators RBAC 생애주기·webhook-events break-glass·audit 전면·데이터분류 스캐폴드) + **P9-4 app-side graceful drain**(무유실·offline-hang 강제종료) → ④/인프라 무관 자율 가능 범위 소진 · 구현현황 = S3
  - **(8/13 완료) T-AUTH-2-6 — GW JWKS 공개 엔드포인트(v1.0.11 승격) + ③b device 토큰 계약 정합** — `GET /.well-known/jwks.json`(무인증·개인키 미노출·CleverSpace GW Guard=외부 검증자) + 토큰 `iss`https형식/TTL≤15분/`aud`=GW수준. 머지 #12478(외부 검증 시뮬 실 jwt.verify·전체 e2e 430 회귀0) → S3 ②-f
  - **(v1.0.11 반영) 스펙 정합화** — prod 리전 **시드니 `apse2`** 교정(멜버른 apse4=IoT Core 미지원)·JWKS v1.0 승격·Console 전역 단일 확정 → 코드 영향은 T-AUTH-2-6뿐(리전=배포 config·grep 반전 확인·재작업 0)
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
    - **어디까지 왔나 (8/13)**: 1단계 코어(P0~P6·P10) 완료. 2단계는 **P8 골격(8-1·8-2·8-3) + P9 골격 app-side(9-1·9-2·9-3) + P9-4 drain + P11 Admin CRUD 전부(11-1~11-6 머지) 완결** — 로컬 더블 기준, 실연동은 ④ AXS 후. **인증 보강**: v1.0.11로 JWKS 엔드포인트 v1.0 승격 → **T-AUTH-2-6 완료(#12478)**(공개키 게시+토큰 claim 정합·개인키 미노출·외부 검증 시뮬). **v1.0.12 정합화**: (A) **enroll CSR→IoT Core mTLS cert 발급·폐기 완료(#12557)**(app-side·`IotCertPort`·발급 INACTIVE 게이팅·승인 활성·revoke/kill/재-enroll 폐기=REVOKED+detach·독립리뷰 Critical 수정) + (B) Admin API Entra-gated CORS(#12497). **④/인프라 무관 자율 가능 범위 소진**(9-4·12-2 후보 처리: 9-4 app-side 완료·12-2 compat E2E는 게이트 미배선(① One Pager 매트릭스)으로 블록). **남은 것 = P7(External Connector·AXS)·9-5(IoT)·P12-1(sandbox E2E)=④ AXS 실자격 선결 · 9-4 실 KEDA·0-5 잔여(자동배포)·P12-4=③-I 인프라(Jack) · P12-2(compat E2E)=① One Pager 매트릭스 확정 · P12-3(부하)=부하환경 · P7 골격(7-1/2/4/5)=로컬 더블 선행 가능(보류).** 구현 다음 통합·검증·QA 단계가 이어진다.
    - 매 Task 완료 시 갱신.
    - **진행 단계** — 스펙(분석/설계)과 구현을 분리해 진행한다. 스펙은 HLD로 baseline 동결됐고 현재 구현(LLD 병행) 중이다. 구현이 끝이 아니라, QA 인계 전 개발팀이 통합·시스템 테스트로 동작을 확증하는 단계가 남고, 이어 QA·운영이 있다.
      - **스펙 — 분석/설계(HLD)**: SRS·DBML·OpenAPI·TCL baseline v1.0 동결 · 정합화(v1.0.1~v1.0.4) 지속 · LLD는 구현과 병행
      - **구현(LLD 병행)** — _구현 단계 내 진척(코딩 Task) · region-silo 재작업(8/3·PR #12241) 완료로 **P4 대부분 삭제·단일화** → Task 집합 축소·재산정 예정_: 1단계 코어 **P0~P6·P10 완료 + region-silo 재작업 완료** · 2단계 **P8 골격 완료(8-1·8-2·8-3)·P9 착수(9-1)** / P7·P11·P12는 ④ 연동 Spec 후 · Task별 검증 4종(unit·e2e·curl·DB)
      - **✅ region-silo(R2·spec-v1.0.5/1.0.6) 재작업 완료(8/3·PR #12241 머지 `9146ae3`)**: 아래 ✅완료 중 **P1 T-DATA-1-1(전역/리전 2-DB)·1-6(region_catalog 시드) · P3 T-ENR-3-2(GeoDNS default region 배정) · P4 전체(Region Resolver·GET /v1/regions·PUT /me/region·region 카탈로그 CRUD) · P6 T-PXY-6-2의 region 해석 단계**가 리전 완전 분리로 **삭제·단일화됨**(단일 datasource·region=배포 상수·Region Directory·리전 변경=마이그레이션·ClinicResolution=리전 echo·하드 FK). **완료 이력은 아래 표에 보존**(당시 PR 기준)하되 현행 코드는 단일 datasource. 검증: unit 534·e2e 157·CI green(build 20260803.1)·`verify-spec`/`verify-ci` 게이트 신설.
      - **개발 통합·검증(QA 인계 전)**: 통합 테스트 · 시스템 E2E(실 계약: AXS·CleverSpace·EzServer) · 성능·부하 · HA·복원력 · 보안 검토 → 동작 확증 후 QA 인계
      - **QA**: 릴리스 회귀 · QA TCL · V&V 산출물(IEC 62304 / ISO 13485)
      - **운영·릴리스**: staging/prod 배포(인프라) · AXS pilot
    - **상태 범례**: 🔥 **이번주 완료**(8/6 회의 이후 따끈·main merge) · ✅ 이전 완료(8/6 이전 merge) · 🟠 진행중/검토 · ⬜ 대기 · 🔴 외부/인프라 선결. **표기 규칙**: **8/3 주간회의 이전 1단계 코어(P0~P6)** = 완료 Phase 1행 · **8/3 이후 작업(P8·P9·P10·P11·인증 2-6·v1.0.12·P7)** = **Task 단위 전개**(회의 진척 가시화) · 미착수/전체 동일 상태 Phase = 1행.

      | Phase | 범위 | 상태 | PR·비고 |
      | --- | --- | --- | --- |
      | **P0 플랫폼 스캐폴드** | 0-1~0-6(4-way·로컬환경·포트어댑터·더블·Prisma·관측·에러·Config·CI·Dockerfile) | ✅ 완료 | #11971~11995 · 자동배포(CD)=③-I(Jack) |
      | **P1 데이터 모델** | 1-1~1-7(스키마·KMS envelope·Redis·audit append-only·시드) | ✅ 완료 | #12006~12040 · region-silo 단일 datasource 재작업 반영 |
      | **P2 인증** | 2-1~2-5(device private_key_jwt→RS256·operator Entra OIDC·RBAC) | ✅ 완료 | #12094~12143 · 2-6(JWKS)은 8/3 이후 Task 전개(아래) |
      | **P3 enrollment·생애주기** | 3-1~3-5(개시/완료·상태머신·재-enroll 회전·C/S 승인·kill·pending 만료) | ✅ 완료 | #12158~12171 · v1.0.12 IoT cert 발급 확장=아래 #12557 |
      | **P4 region resolution** | 4-1~4-5(Resolver·ClinicResolution·PATCH/PUT me·PHI PDP·카탈로그) | ✅ 완료 | #12173~12191 · region-silo로 대부분 단일화 |
      | **P5 호환성 게이트** | 5-1~5-3(Vatech-* 파싱→400·well-known 서빙·semver 게이팅) | ✅ 완료 | #12194~12200 · 게이트 실 배선=①One Pager 매트릭스 후(→P12-2) |
      | **P6 target-routed 프록시** | 6-1~6-3(라우터·SSRF·PEP 체인·verbatim bypass·복원력) | ✅ 완료 | #12203~12213 |
      | ─ **8/3 주간회의 이후 (Task 단위)** ─ | | | |
      | **P10** 10-1 | `POST /v1/fleet/heartbeat`·fleet_state·nextIntervalSeconds(§7.8.1) | ✅ 완료 | #12363 |
      | **P10** 10-2 | 중앙 CentralConfigService(gw.*)·스코프 병합 resolve | ✅ 완료 | #12364 |
      | **P10** 10-3 | 클라이언트 SW 인벤토리 수집(§7.8.5) | ✅ 완료 | #12366 |
      | **P10** 10-4 | Admin fleet/clients 조회 3종(P10 완결) | ✅ 완료 | #12368 |
      | **P8** 8-1 | webhook 수신 HMAC 검증·Receiver 골격(§7.6.2) | ✅ 완료 | #12369 |
      | **P8** 8-2 | eventId 멱등·store-then-ack·payload KMS 암호화 저장 | ✅ 완료 | #12411 |
      | **P8** 8-3 | webhook 저장 후 SQS enqueue(claim-check·재시도) | ✅ 완료 | #12414 · 골격(로컬 더블)·실연동 ④ 후 |
      | **P9** 9-1~9-3 | Dispatcher SQS 소비·대상해석·미해석 DLQ·복호 후 MQTT publish | ✅ 완료 | #12420 (3 Task 1 PR) |
      | **P9** 9-4 | app-side graceful scale-in drain(무유실·offline-hang 방지) | ✅ 완료 | #12471 · 실 KEDA 검증=③-I |
      | **P11** 11-1 | targets 레지스트리 CRUD(credential/secret KMS envelope) | ✅ 완료 | #12441 |
      | **P11** 11-2 | policies CRUD | ✅ 완료 | #12443 |
      | **P11** 11-3 | operators·RBAC 역할 생애주기(마지막 admin lockout 방지·재부여) | ✅ 완료 | #12456 |
      | **P11** 11-4 | webhook-events 조회·break-glass payload 열람(KMS 복호·PHI masking·감사) | ✅ 완료 | #12459 |
      | **P11** 11-5 | `GET /v1/admin/audit`(조회 전용)·audit 전면 커버리지 sweep | ✅ 완료 | #12469 |
      | **P11** 11-6 | 데이터 분류·크로스보더 동의 태깅(경량 스캐폴드·v1.0 no-op·gw/1.2 활성) | ✅ 완료 | #12470 |
      | **P2** 2-6 | GW JWKS 공개 엔드포인트(v1.0.11 승격)+③b device 토큰 claim 정합 | 🔥 이번주 | #12478 |
      | **v1.0.12** (B) | Admin API Entra-gated 공개 — CORS(#12487) | 🔥 이번주 | #12497 |
      | **v1.0.12** (A) | enroll CSR(PKCS#10)→IoT Core mTLS cert 발급(INACTIVE 게이팅)·승인 활성·revoke/kill/재-enroll 폐기(app-side·`IotCertPort`·#12491) | 🔥 이번주 | #12557 · 폐기=REVOKED+detach(kill 무력화 방지·독립리뷰 Critical 수정)·개인키 GW 미수신 |
      | **P7** 7-1 | External Connector 아웃바운드 OAuth2 토큰(client_credentials·soft-state 캐시·선제 갱신·dual-window·§7.1.3) | 🔥 이번주 | #12561 · 독립리뷰 High(fetch 타임아웃) 수정 |
      | **P7** 7-4 | 클리닉 self org-binding 자가 등록(`POST /v1/clinics/me/org-bindings`→org_mapping·§2.3.4) | 🔥 이번주 | #12562 · admin org-mappings CRUD 는 11-3 기완성 |
      | **P7** 7-2 | egress allowlist SSOT+PDP egress 집행(fail-closed·§7.5.3) | ✅ 완료 | T-REG-4-4(P4)에 기구현·#12187 계열 |
      | **P7** 7-5 | presigned 중계 리전 guardrail wiring(TC-REG-42·§7.3.3·verbatim 중계=P6 기구현) | 🟠 검토중 | PR(검토)·독립리뷰 false-negative 우회 다수 차단 |
      | **P7** 7-3 | AXS 커넥터 최초 실연동(verbatim·OAuth 주입·Org-ID) | 🔴 대기 | ④ AXS sandbox 실자격(Straumann·~8/18) |
      | **P9** 9-5 | device **실** IoT 프로비저닝(Thing/정책 attach·실 cert 발급 인프라) | ⬜ 대기 | 🔴 ③-I/④ IoT Core(cert 발급 app-side=위 v1.0.12(A) 완료·DBML `iot_certificate_id`=스펙 세션) |
      | **통합 검증** 시스템 E2E | 크로스-Phase 여정 — SYS-01(온보딩)·SYS-02(webhook 왕복 3앱)·SYS-04(kill 전파)·SYS-05(운영자 RBAC) | 🔥 이번주 | #12566·#12567·#12568 · 멀티앱(core+admin+receiver+dispatcher) 로컬 더블+실 DB/Valkey/SQS/MQTT/KMS · SYS-03=7-5·SYS-06/DISP-01=Phase e2e |
      | **P12 E2E·하드닝** | 12-1 AXS sandbox E2E · 12-2 compat E2E · 12-3 부하 · 12-4 HA/KEDA | ⬜ 대기 | 🔴 선결: 12-1=④ AXS · 12-2=①One Pager 매트릭스 · 12-3=부하환경 · 12-4=③-I 인프라 |

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
