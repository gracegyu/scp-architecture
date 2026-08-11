# VT API Gateway — 8/13 주간회의 Agenda

> **과거 주차(6/25~8/6)는 [`주간회의-Agenda-Archive.md`](주간회의-Agenda-Archive.md)로 이관·보존**(가끔 조회용). 본 문서는 **8/13 현행 주차만** 유지한다. 틀(논의/공유/이월)은 이전 주와 동일하며 **Gantt(S1)·스펙 작성 테이블(S2)은 매주 상시 포함**한다. _※ `(프레임)` 표시 항목은 8/13 회의 시 확정한다._

- 이번 주 진행 _(프레임 · 8/13 회의 시 확정 · 상세·수치는 아래 논의 R#/공유 S# 한 곳에만)_
  - **(8/6~8/13 완료) 2단계 자율 구현 진척** — v1.0.12(enroll CSR→IoT Core mTLS cert·Admin API Entra-gated CORS)·P7 커넥터 골격(7-1/2/4/5)·시스템 E2E(SYS-01/02/04/05)·프록시 복원력 하드닝·v1.0.15(enroll Reject·감사 사유)·v1.0.16(clinic.memo·admin clinics 목록/상세)·11-8(admin ClinicInfo 교정) → **Task 단위 상세·PR = 공유 S3**
  - **(잔여) EzServer OnePager 수령 확인.**
  - _(이번 주 결정사항 = 회의 시 추가)_

- 논의 사항 (이번 주 · 신규 논의/결정 안건)
  - _(이번 주 결정사항 = 스펙 세션 정리 후 반영 · 회의 중 신규 안건 발생 시 여기 추가 · 보류·선결은 아래 「이월 논의 사항」 표 참조.)_

- 공유 사항 (결정 아님 · 정보 공유 · 매주 상시)
  - **S1. 프로젝트 일정(Gantt) — 8/13 스냅샷** — 스펙 생애주기(작성→PR→baseline) + GW 구현 타임라인.
    - **정본 = 본 Agenda(S1 Gantt).** _개발 Roadmap 결정.md는 폐기(더 이상 사용 안 함) — 이 스냅샷이 현행 정본이며 여기서 직접 갱신한다._
    - **8/6→8/13 변경**:
      - 2단계 자율 구현 진척: v1.0.12(enroll CSR→IoT mTLS·Admin CORS)·P7 골격(7-1/2/4/5)·시스템 E2E·프록시 복원력 하드닝·v1.0.15·v1.0.16·11-8 — 상세=S3
    - **막대 색**: 작성=기본 · PR=강조 · ◆=baseline/마일스톤 · 빨강=외부/미정 선결
    - **선결(빨강)**: AXS **prod** 자격(NDA 후·Straumann) _(PPR sandbox 자격=확보 8/11 · IO Scanner=AXS webhook 흡수·GW 무관·R1 종료)_
    - **목표 = 10월 출시**(역산·잠정 — 2단계는 AXS **PPR 자격 확보로 착수 가능**·잔여 변수 = **prod 자격(NDA후)·부하환경**)
    - **병행 별도 프로젝트**: `SectionView Module 구현`(7/13~2주·Raymond·**GW 아님**·완료)은 `▷ 병행` 섹션에 표기
    - **GW 구현 = 2단계 병행(유지)** — 1단계 GW 독립 코어(P0~P6·P10)는 ③ baseline 고정으로 **정상 진행**(IO Scanner 보류 영향 없음). 2단계 AXS 연동(P7~P12)은 **PPR sandbox 자격 확보로 착수 가능**(prod 자격=NDA후·§S3).

    ```mermaid
    gantt
        title v1.0 = Straumann(AXS) 첫 외부연동 — 10월 출시 목표(역산·잠정)
        dateFormat YYYY-MM-DD
        axisFormat %m/%d
        todayMarker stroke-width:3px,stroke:#d33,opacity:0.6

        section ③ GW SRS + API/DBML (계약 SSOT · baseline v1.0 동결)
        작성 (본문+OpenAPI·DBML)       :done, srsw, 2026-06-15, 28d
        PR 리뷰·수정                  :done, srspr, 2026-07-13, 2026-07-20
        baseline v1.0 (7/20 확정·spec-v1.0.1 정합화 7/22) :milestone, done, srsbl, 2026-07-20, 0d

        section GW 구현 → E2E → 출시 (③ SRS 완료 직후 착수 · 2단계 병행 · Raymond 부분투입)
        1단계 GW 독립 코어 (③ 고정·④무관·P0~P6·P10·진행중) :active, implindep, 2026-07-21, 21d
        2단계 AXS 연동 (P7~P12·④ AXS 보류 해제 후)   :implaxs, after implindep, 7d
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
        ② Teddy 상세작성·리뷰·수정 :active, ezpr, after ezw, 21d
        ③ baseline :milestone, ezbl, after ezpr, 0d

        section ③-P-CS CleverSpace OnePager (① 초안+PR=Raymond → ② CleverSpace팀(Larry) 상세·리뷰·수정 → ③ baseline)
        ① 초안+PR (Raymond·PR #12239·EzCloud) :done, cssub, 2026-07-27, 5d
        ② CleverSpace팀(Larry) 상세작성·리뷰·수정 :active, cspr, after cssub, 14d
        ③ baseline :milestone, csbl, after cspr, 0d

        section ③-P-CO CleverOne OnePager (① 초안+인계=Raymond·SharePoint → ② CleverOne팀(Nick) 상세·리뷰·수정 → ③ baseline)
        ① 초안+인계 (Raymond·SharePoint gw_adaptation) :done, cosub, 2026-07-27, 5d
        ② CleverOne팀(Nick) 상세작성·리뷰·수정 :active, copr, after cosub, 14d
        ③ baseline :milestone, cobl, after copr, 0d

        section ④ AXS 연동 프로파일 (경량 스펙·구현 아님 — 구현=GW 2단계 P7 · IO Scanner=AXS webhook 흡수·GW 무관)
        AXS PPR(pre-prod) sandbox 자격 확보(8/11·Frank/Thomas) :done, cred, 2026-08-11, 1d
        연동 프로파일 정리 (target config·AXS OpenAPI 참조·org_mapping 의미·경량·스펙) :axsw, after cred, 14d
        프로파일 확정                  :milestone, axsbl, after axsw, 0d
        AXS prod 자격(NDA 후·Straumann·선결) :crit, credp, 2026-08-18, 21d

        section ③-C GW Console — gw/1.0 대응 v1.0 (Flow 최소기능·MS Entra 앱계층 인증 · SRS 8/5·전규현/Raymond)
        SRS 작성 (8/5 착수)            :active, consrsw, 2026-08-05, 6d
        SRS PR 리뷰·수정 (차주초)       :consrspr, 2026-08-11, 14d
        v1.0 최소 구현 (Flow 동작 최소) :conv1, after consrspr, 28d
        v1.0 최소기능 완료             :milestone, conv1m, after conv1, 0d
        section ③-C GW Console 후속 (gw/1.1·gw/1.2·GW-무관 부가 — 일정 미고정·상당 후행)
        후속 확장 (해당 GW 역량 활성 후·부가는 요청 시 그때그때) :conv2, after conv1m, 30d
        확장 진행(수시)             :milestone, conv2m, after conv2, 0d

        section v1.0 이후 (deferred · post-v1.0)
        CleverOne 연동 *구현* (스펙은 지금·구현 post-v1.0) :codef, after rel, 14d

        section ▷ 병행 · 별도 프로젝트 (GW 아님)
        SectionView Module 구현 (Raymond·완료) :done, sv, 2026-07-13, 2026-07-30
    ```

  - **S2. 스펙 작성 테이블 — 제품별 개발 항목 종합 (제품 × 단계) · 매주 스냅샷** · **정본 = 본 Agenda(S2)** (_Roadmap 결정.md 폐기 — 이 표가 현행 정본_)
    - **각 셀 앞 이모지 = 그 항목을 다루는 스펙의 작성 진행**: ✅ baseline · 🟢 PR · 🟡 작성중 · ⬜ 미작성 (— = 해당 없음)

      | 제품 | 0단계(IO Scanner 수집 — **AXS webhook 흡수·GW 무관·R1 종료**) | 1단계(호환성) | 2단계(presigned) | 3단계(GW 일원화) | 4단계(멀티리전) | 5단계(Straumann) | 후속 | 스펙 산출물(단위·유형) |
      | --- | --- | --- | --- | --- | --- | --- | --- | --- |
      | **CleverSpace** | — | 🟡 서버 버전 체크·well-known·오류코드 | 🟡 presigned 발급 API 신규 | 🟡 GW 경유 수신 정합 | ⬜ 멀티 Region 구축 | — | — | **🟢 ③-P-CS CleverSpace OnePager 인계(PR #12239·EzCloud `docs/onepager/gw_adaptation`)** — CleverSpace 팀(Larry) 검토 |
      | **CleverOne**(OnePager 지금·연동 구현 post-v1.0) | — | 🟡 Vatech-\* 헤더·well-known·fallback | 🟡 presigned 업로드 이용 | 🟡 Direct→GW 경유 | ⬜ Region 선택 UI(대안)·ClinicID | — | — | **🟢 ③-P-CO CleverOne OnePager 인계(SharePoint gw_adaptation)** — CleverOne 팀(Nick) 검토 · 담당=Nick·작성=Raymond |
      | **EzServer(EZ)** | ⬜ IO Scanner 데이터 수신(방식 R1·**보류**·TBD) | 🟡 헤더 대리 전달 | 🟡 전송 로직(presigned 직접) | 🟡 GW 경유 전환 | 🟡 ClinicID·Region·클리닉 등록(잠정) | 🟡 AXS(갈래A)·presigned 직접(IO Scanner 세부=TBD) | ⬜ Rust 재개발 | **🟡 ③-P-EZ One Pager 초안 작성됨**(Raymond→EzServer 팀) — `specs/03p-ez-ezserver/EzServer-GW적응-OnePager.md` · ④(갈래A) |
      | **CleverLab** | — | — | — | — | — | ⬜ AXS 오더·상태·확정(갈래B)·presigned | — | ④ Sub-SRS(갈래B) |
      | **VatechAPIGateway** | — | 🟢 ↳3단계 흡수(호환 게이트·§7.7) | 🟢 ↳3단계 흡수(presigned 중계·§4.1.4) | 🟢 본체·라우팅·인증·호환·presigned 중계·경로B 흡수 | 🟢 리전 라벨 호스트·Region Directory·HA(K8s)·Route53·RDS(리전 단일) | ⬜ AXS OAuth 중계·Org-ID·온보딩·인바운드·고정IP | — | **③ SRS ✅ baseline(spec-v1.0.4)** · region-silo `spec-v1.0.5` PR 리뷰중 · ④ connector ⬜(보류) |
      | **GW Console** | — | — | — | — | 🟡 Admin Web Console gw/1.0 대응 최소(MS Entra 앱계층 인증·Admin API Entra-gated) | ⬜ 온보딩·Org-ID 관리 등 **후속**(gw/1.1·1.2·부가·미정) | — | ⬜ ③-C Sub-SRS gw/1.0 대응 baseline **9월 착수 예정**(R5 당김 결정·전규현/Raymond) |
      | **인프라** | — | — | — | 🟢 dev·qa·stag(단일 Region)·prod(Region별) | 🟢 Route53·K8s·비-AWS minio | 🟢 AXS 고정IP·샌드박스 | — | **🟢 ③-I IaC 구축 계획서 — PR #11973 병합(7/27)·Jack 상세 반영**(Raymond diagram+SRS추출→Jack) — 정본 `vt-api-gateway-infra` · **baseline tag 불요**(living doc) · **AWS 4계층** · **+ 8/4 KMS 키 토폴로지 provisioning ask**(spec-v1.0.7·handoff-infra 항목5 — 리전별 CMK `gw-payload`/`gw-target-cred`·pod별 grant·dev payload CMK 선생성) |
      | **외부(Straumann AXS)** | — | — | — | — | — | 🟡 **PPR sandbox 자격=확보(8/11)** · ⬜ prod(정식계약)=NDA 후(선결) | — | ④ 입력(외부 제공) |
      | **LMP(License Portal, 바텍)** | — | — | — | — | — | — | ⬜ (조건부) 제3자 서명 attestation | **enroll B안 시만**·ES 라이선스팀(R9·B-42) |

    - **스펙 문서 등록처·경로·baseline (SSOT)** — 각 제품 스펙 정본의 Repo·경로·태그. _(미정 = R3에서 등록처 확정 · OnePager는 담당팀 baseline 시 tag 부여)_

      | 단위 | 스펙 문서 | Repo (Azure DevOps) | 경로 | baseline tag |
      | --- | --- | --- | --- | --- |
      | **③ GW** | SRS(+OpenAPI·DBML·UnitTCL) | `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway` | `docs/specs/SRS.md` · `docs/specs/design/`(openapi·dbml) · `docs/specs/UnitTCL.md` | **`spec-v1.0.4`**(최신 baseline) · region-silo `spec-v1.0.5`(PR 리뷰중) |
      | **③-C GW Console** | Sub-SRS | `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console` (별도 repo·GW 소유→이관) | **작성 중(초안·경로=R3 확정 대기)** | **작성 중(8/5 착수)·차주초 PR 예정** |
      | **④ AXS** | **경량 연동 프로파일**(스펙·구현 아님) | 〃 vt-api-gateway (GW 소유) | `docs/specs/04-subsrs-straumann-axs/` | **연동 config·AXS OpenAPI 참조·org_mapping 의미**(경량)·**PPR sandbox 자격 확보·착수 가능**(prod=NDA후·구현=2단계 P7) |
      | **③-I 인프라** | IaC 구축계획서 | `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-infra` | `docs/IaC-구축계획서.md` | **PR #11973 병합(7/27)** · baseline tag 불요(living doc) |
      | **③-P-EZ EzServer** | GW적응 OnePager | `https://dev.azure.com/ewoosoft/ezserver/_git/ezserver_suite` (branch `v6.5.x`) | `doc/onepager/gw_adaptation/Confidential_gw_adaptation_onepager.md` | 미부여(EzServer 팀 baseline 예정·R3 확인) |
      | **③-P-CS CleverSpace**(=EzCloud) | GW적응 OnePager | `ezicloud/ezcloud`(https://dev.azure.com/ewoosoft/ezicloud/_git/ezcloud) | `docs/onepager/gw_adaptation/CleverSpace-GW적응-OnePager.md` | **PR #12239**([링크](https://dev.azure.com/ewoosoft/ezicloud/_git/ezcloud/pullrequest/12239))·팀 baseline 예정 |
      | **③-P-CO CleverOne** | GW적응 OnePager | SharePoint `ProjectDoc/Clever One/srs/OnePager/gw_adaptation`([문서](https://vatechcorp.sharepoint.com/:t:/s/es/IQC500caygYpS78euV2xO5WyAfzZF2kbz_09J20UbackH2k?e=tQLWOJ) · [폴더](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Forms/AllItems.aspx?id=%2Fsites%2Fes%2FProjectDoc%2FClever%20One%2Fsrs%2FOnePager%2Fgw%5Fadaptation&viewid=5a018594%2D6322%2D4139%2Db7ee%2De9dd4aa4d23a&p=true&ga=1)) | 〃(SVN 제품·git 아님) | — (SharePoint·team baseline) |
      | **③-P-LMP LMP** | OnePager(조건부) | **미정 (ES 라이선스팀?)** | — | — |
      | **CleverLab** | ④ Sub-SRS(갈래B) | 미정 (보류) | — | — |

      > **진행 배경 (누적·상시)**
      >
      > - **IO Scanner = AXS webhook 흡수·GW 무관**(R1 종료) · **④ AXS = 경량 연동 프로파일·PPR 자격 확보** → **1·2·3단계 우선 유지**.
      > - **③-P-CS CleverSpace·③-P-CO CleverOne OnePager 2개**(각 1·2·3단계=호환성+presigned+GW일원화 통합) **= Raymond·7/27 병행 착수**(deferred→active · CleverOne Nick→Raymond → 담당팀 전달).
      > - **①호환성·②Presigned One Pager 별도 미작성 → 두 제품 OnePager에 흡수**(딱 2개 문서 · presigned=CleverSpace 발급 API+CleverOne 이용, 둘 다 GW 경유라 양쪽 변경).
      > - ③ GW SRS = **baseline v1.0 동결(7/20)·spec-v1.0.1 정합화(7/22)**.
      > - ③-I Infra = **PR #11973 병합 완료(7/27)**(Jack 상세·baseline tag 불요·living doc) · ③-P-EZ EzServer 초안 = Raymond→Teddy 상세.
      > - **AWS 환경 4계층(dev·qa·stag·prod)** 결정 반영.
      > - CleverOne OnePager는 지금 작성(연동 *구현*만 post-v1.0).
      > - 순서·의존 = 본 Agenda S1 Gantt(Roadmap 결정.md 폐기).

  - **S3. GW 구현 현황 — Phase·Task 스냅샷 (8/13·매주 갱신)**
    - **어디까지 왔나 (8/13)**
      - 완료
        - 1단계 코어 — P0~P6·P10
        - 2단계 골격 — P8·P9·P11 (로컬 더블 기준·실연동 ④ AXS 후)
      - 이번 주(8/6~8/13) — v1.0.12(enroll CSR→IoT mTLS·Admin CORS)·P7 커넥터 골격(7-1/2/4/5)·시스템 E2E(SYS-01/02/04/05)·프록시 복원력 하드닝·v1.0.15(enroll Reject·감사 사유)·v1.0.16(clinic.memo·admin clinics 목록/상세)·11-8(ClinicInfo 교정)
      - 남은 것 (외부·인프라 선결)
        - ④ AXS 실자격 → 7-3(커넥터 실연동)·12-1(sandbox E2E)
        - ③-I 인프라 → 9-5(실 IoT)·9-4(실 KEDA)·0-5(자동배포)·12-4(HA/KEDA)
        - ① One Pager 매트릭스 → 12-2(compat E2E) · 부하환경 → 12-3(부하)
      - 다음 단계 — 개발 통합·검증(통합·시스템 E2E·부하·HA·보안) → QA(회귀·V&V·IEC 62304/ISO 13485) → 운영·릴리스(staging/prod·AXS pilot)
    - **참고** — 스펙=HLD baseline(v1.0) 동결·LLD는 구현 병행 · region-silo 재작업(8/3·#12241)으로 P4 대부분 단일화(단일 datasource·region=배포 상수) · Task별 검증 4종(unit·e2e·curl·DB) · 매 Task 완료 시 갱신
    - **상태 범례**: 🔥 **이번주 완료**(8/6 회의 이후 main merge) · ✅ 이전 완료 · 🟠 진행중/착수예정 · ⬜ 대기 · 🔴 외부/인프라 선결. **표기 규칙(8/13)**: **이번주 완료(🔥)는 Task 단위**로 전개(진척 가시화) · **완료 Phase(지난주까지·전체 동일 상태)는 Phase 1행**으로 묶음 · **Phase 내 상태가 다른 Task만 별도 행**(예: P9-5) · 미착수 Phase = 1행.

      | Phase / Task | 범위 | 상태 | PR·비고 |
      | --- | --- | --- | --- |
      | ─ **1단계 코어 (완료·Phase 1행)** ─ |  |  |  |
      | **P0 플랫폼 스캐폴드** | 0-1~0-6(4-way·로컬환경·포트어댑터·더블·Prisma·관측·에러·Config·CI·Dockerfile) | ✅ 완료 | #11971~11995 · 자동배포(CD)=③-I(Jack) |
      | **P1 데이터 모델** | 1-1~1-7(스키마·KMS envelope·Redis·audit append-only·시드) | ✅ 완료 | #12006~12040 · region-silo 단일 datasource 반영 |
      | **P2 인증** | 2-1~2-6(device private_key_jwt→RS256·operator Entra OIDC·RBAC·JWKS 공개 엔드포인트) | ✅ 완료 | #12094~12143·#12478(2-6 JWKS·v1.0.11 승격) |
      | **P3 enrollment·생애주기** | 3-1~3-5(개시/완료·상태머신·재-enroll 회전·C/S 승인·kill·pending 만료) | ✅ 완료 | #12158~12171 |
      | **P4 region resolution** | 4-1~4-5(Resolver·ClinicResolution·PATCH/PUT me·PHI PDP·카탈로그) | ✅ 완료 | #12173~12191 · region-silo로 대부분 단일화 |
      | **P5 호환성 게이트** | 5-1~5-3(Vatech-\* 파싱→400·well-known 서빙·semver 게이팅) | ✅ 완료 | #12194~12200 · 게이트 실배선=①One Pager 후(→P12-2) |
      | **P6 target-routed 프록시** | 6-1~6-3(라우터·SSRF·PEP 체인·verbatim bypass·복원력) | ✅ 완료 | #12203~12213 · 복원력 하드닝=이번주(아래) |
      | ─ **2단계 완료 Phase (지난주까지·Phase 1행)** ─ |  |  |  |
      | **P8 webhook 수신** | 8-1~8-3(HMAC 검증·eventId 멱등·store-then-ack·payload KMS 저장·SQS enqueue) | ✅ 완료 | #12369·#12411·#12414 · 골격(로컬 더블)·실연동 ④ 후 |
      | **P9 Dispatcher·분배** | 9-1~9-4(SQS 소비·대상해석·미해석 DLQ·복호 후 MQTT publish·graceful drain) | ✅ 완료 | #12420·#12471 · 9-5(실 IoT)=대기(아래)·실 KEDA=③-I |
      | **P10 fleet·중앙 config** | 10-1~10-4(heartbeat/fleet_state·CentralConfig·SW 인벤토리·admin fleet/clients 조회) | ✅ 완료 | #12363~12368 |
      | **P11 Admin CRUD** | 11-1~11-6(targets·policies·operators RBAC 생애주기·webhook-events break-glass·audit 전면·데이터분류 스캐폴드) | ✅ 완료 | #12441~12470 |
      | ─ **이번주 완료 🔥 (8/6~8/13·Task 단위) + 진행 Phase(P7)** ─ |  |  |  |
      | **v1.0.12** (A) | enroll CSR(PKCS#10)→IoT Core mTLS cert 발급(INACTIVE 게이팅)·승인 활성·revoke/kill/재-enroll 폐기(REVOKED+detach·app-side·`IotCertPort`) | 🔥 이번주 | #12557 · 개인키 GW 미수신·독립리뷰 Critical 수정 |
      | **v1.0.12** (B) | Admin API Entra-gated 공개 — CORS | 🔥 이번주 | #12497 |
      | **시스템 E2E** | SYS-01(온보딩)·02(webhook 왕복 3앱)·04(kill 전파)·05(운영자 RBAC) | 🔥 이번주 | #12566~12568 · 멀티앱(core+admin+receiver+dispatcher) 로컬 더블+실 DB/Valkey/SQS/MQTT/KMS |
      | **P6 하드닝** 프록시 복원력 | 장애주입 e2e(504 TARGET_TIMEOUT·502·hang 없음·§7.5.4)+deadline-abort 정규화 fix | 🔥 이번주 | #12569·#12570 · 독립리뷰가 오진단 정정(프로덕션 이미 504) |
      | **v1.0.15** (A·B) | enroll 명시적 Reject(`device_status +rejected`·pending→rejected 종단·PATCH devices) + 감사 사유(`audit_log.reason`·payload reason 필수·kill/reject 저장)(T-ENR-3-7) | 🔥 이번주 | #12576 · DB 마이그레이션 2건 · device write RBAC=cs·admin · 독립리뷰 2회 |
      | **v1.0.16** clinic.memo | clinic 식별 메모(`clinic.memo`) + **admin clinics 목록/상세 신규**(memo·deviceCount·orgBindingStatus·v1.0.10 note 해소)·admin·cs 편집·device-self 제외·변경 감사 `clinic.memo.update`(T-ADM-11-7) | 🔥 이번주 | #12578 · DB 마이그레이션 1건 · LMP 표시필드와 별개(enroll/self-PATCH 미간섭) · 독립리뷰 actionable 0 |
      | **P11** 11-8 | admin ClinicInfo 교정 `PATCH /v1/admin/clinics/{id}`(name·country·address·phone·website·admin·cs·audit `clinic.info.update`·mapping_version 불변)(T-ADM-11-8·스펙-코드 갭) | 🔥 이번주 | #12581 · 계약 기존(OpenAPI patchAdminClinicsById) 미구현이던 갭 · 검증 로직 core self-PATCH 와 libs 공유 추출 · 독립리뷰 High/Med 0 |
      | **P7** 7-1 | External Connector 아웃바운드 OAuth2 토큰(client_credentials·soft-state 캐시·dual-window·§7.1.3) | 🔥 이번주 | #12561 · 독립리뷰 High(fetch 타임아웃) 수정 |
      | **P7** 7-4 | 클리닉 self org-binding 자가 등록(`POST /v1/clinics/me/org-bindings`→org_mapping·§2.3.4) | 🔥 이번주 | #12562 |
      | **P7** 7-5 | presigned 중계 리전 guardrail wiring(TC-REG-42·§7.3.3·verbatim 중계=P6 기구현) | 🔥 이번주 | #12564 · 독립리뷰 Critical/High 다수 차단 |
      | **P7** 7-2 | egress allowlist SSOT+PDP egress 집행(fail-closed·§7.5.3) | 🔥 이번주 | #12564(7-5 와 공동 PR) · egress 집행 로직은 P4 T-REG-4-4(#12187)에 기구현 → 이번주 7-2 Task 로 확인·종결 |
      | **P7** 7-3 | AXS 커넥터 최초 실연동(verbatim·OAuth 주입·Org-ID) | 🔴 대기 | ④ AXS sandbox 실자격(Straumann·~8/18) |
      | ─ **대기·무영향** ─ |  |  |  |
      | **P9** 9-5 | device **실** IoT 프로비저닝(Thing/정책 attach·실 cert 발급 인프라) | 🔴 대기 | ③-I/④ IoT Core(cert 발급 app-side=v1.0.12(A) 완료·DBML `iot_certificate_id`=스펙 세션) |
      | **v1.0.13/14** | 코드 **무영향** — 13=org_mapping 범용 번역표 판정(문서) · 14=authz 복제 DynamoDB Global Table+Streams(gw/1.2·v1.0 복제대상 0) | — | 스펙 핀만 상향(#12555·#12558) |
      | **P12 E2E·하드닝** | 12-1 AXS sandbox E2E · 12-2 compat E2E · 12-3 부하 · 12-4 HA/KEDA | ⬜ 대기 | 🔴 선결: 12-1=④ AXS · 12-2=①One Pager · 12-3=부하환경 · 12-4=③-I |

  - **S3-1. 커버리지 현황 (구현과 분리 · merged=unit+e2e 합산 · 8/13 재측정·post-v1.0.12/P7/시스템-E2E · 매 Task 완료 시 갱신)** — 커버리지 스윕(1·2·3순위 101 케이스·PR #12372) 후 실측, 이후 Task마다 재측정. 정본 기준 = **merged**(단위+통합 합산). **정지트리 실측·merged floor 게이트 통과**(v1.0.12 A/B·7-1/2/4/5·시스템 E2E SYS-01/02/04/05 반영). _(v1.0.15 T-ENR-3-7·v1.0.16 T-ADM-11-7 반영 재측정은 각 머지 후 정지트리에서 수행 — 신규 로직 전부 unit+e2e 동반이라 floor 유지 예상.)_

    | 스코프                                        | Statements | Branches    | Functions  | Lines      |
    | --------------------------------------------- | ---------- | ----------- | ---------- | ---------- |
    | **① 전역 (merged)**                           | **96.50%** | **91.82%**  | **93.46%** | **96.28%** |
    | **② 보안 도메인 (merged)**                    | **98.49%** | **95.91%**  | **100%**   | **98.39%** |
    | **③ 핵심 보안 파일 16개 (merged·개별)**       | —          | **각 100%** | —          | —          |
    | _참고: 전역 (unit-only)_                      | 77.73%     | 83.02%      | 72.15%     | 78.73%     |
    | **CI 게이트 floor — ① 전역**                  | 92         | 87          | 88         | 92         |
    | **CI 게이트 floor — ② 보안**                  | 95         | 89          | 95         | 95         |
    | **CI 게이트 floor — ③ 핵심파일(개별·branch)** | —          | **90**      | —          | —          |

- 이월 논의 사항 (6/25·7/2·7/9 미결 — 계속)

  | # | 항목 | 타입 | 상태 |
  | --- | --- | --- | --- |
  | 4 | Webhook 클라우드 분배(CleverLab 갈래B) | [논의] | v1.0 제외 — Open 후 결정 |
  | 6 | AXS **prod** 자격(Straumann 정식계약) | [정보] | **PPR sandbox=확보(8/11)** · prod=NDA 후(pilot·실 E2E 선결) |
  | 7 | 경로 B EOS 시점 | [논의] | 리뷰서 workaround·지속성 확정(§2.8) — EOS *시점*만 PM·CS/CO OnePager 미정(①흡수) |
  | 8 | v1.0 목표 RPS·동시 세션 | [정보] | 인프라/규모 PL 입력 대기 |
  | 9 | RTO/RPO·유지보수 윈도우 | [정보] | 인프라 설계 단계 — failover 요건은 R2(저장소 전역일관 vs 리전분리·Q3) 결정과 연계 |
  | 10 | 감사·consent 보존 기간 | [정보] | 법무 확인 대기 |
  | 11 | 호환성 매트릭스 확정본 | [정보] | CleverSpace/CleverOne OnePager 의존(①폐지·흡수) — 초안 7/27 작성·확정값은 담당팀 baseline 후 |
  | 14 | 관측성 앱↔인프라 계약 확정 — ①로그 필드 스키마(현행 pino 기본 필드 ↔ §6.3.2 최소셋 매핑·Appendix B #14) ②메트릭 export 배선(OTLP reader→Grafana Alloy 엔드포인트) | [논의·설계] | **추후 확정** — 트리거=③-I 관측 스택 구축 or P6 프록시 착수(먼저). Raymond 초안(필드 매핑표+엔드포인트 요구)→Jack(인프라) 비동기 합의. **앱 계약(stdout JSON+OTel·redaction) 이미 구현·무블로킹** |
  - **차주 이월 후보**: 이월-R2(목표일정·출시일 재검토) 미확정 시 다음 주 이월.
