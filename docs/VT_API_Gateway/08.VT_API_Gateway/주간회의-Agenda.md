# VT API Gateway — 8/13 주간회의 Agenda

> **과거 주차(6/25~8/6)는 [`주간회의-Agenda-Archive.md`](주간회의-Agenda-Archive.md)로 이관·보존**(가끔 조회용). 본 문서는 **8/13 현행 주차만** 유지한다. 틀(논의/공유/이월)은 이전 주와 동일하며 **Gantt(S1)·스펙 작성 테이블(S2)은 매주 상시 포함**한다. _※ `(프레임)` 표시 항목은 8/13 회의 시 확정한다._

- 이번 주 진행 _(프레임 · 8/13 회의 시 확정 · 상세·수치는 아래 논의 R#/공유 S# 한 곳에만)_
  - **[GW 백엔드]** (8/6~8/13 완료) **2단계 자율 구현 진척** — v1.0.12(enroll CSR→IoT Core mTLS cert·Admin API Entra-gated CORS)·P7 커넥터(7-1/2/4/5 골격 + **7-3 AXS 최초 실연동**)·시스템 E2E(SYS-01/02/04/05)·프록시 복원력 하드닝·v1.0.15(enroll Reject·감사 사유)·v1.0.16(clinic.memo·admin clinics 목록/상세)·11-8(admin ClinicInfo 교정)+**v1.0.17 11-8b(표시필드 PATCH v1.0 봉인)**·**T-E2E-12-1(실-AXS e2e 스캐폴드)·12-2(compat 게이팅 e2e)**·**v1.0.18 T-CFG-5-4(compat-matrix YAML→JSON 발행 파이프라인)** → **Task 단위 상세·PR = 공유 S3**
  - **[GW Console]** (8/11~8/12 완료) **Sub-SRS + 구현 착수** — 전용 repo `vt-api-gateway-console`에 **SRS baseline v1.0**(#12602 머지·tag `spec-v1.0`·리뷰 민진우·정우혁 반영) + **P0 구현 착수·5 Task 머지**(0-1 스캐폴드[스택 버전 확정·**폰트를 CleverSpace와 통일**]·0-2 코드젠+커서 어댑터·0-3 MSW 목·0-4 authProvider[risk:auth]·0-5 App Shell·0-6 dataProvider 실물) → 상세 = 공유 **S4**.
  - **[제품 연동 스펙]** (잔여) EzServer OnePager 수령 확인.
  - _(이번 주 결정사항 = 회의 시 추가)_

- 논의 사항 (이번 주 · 신규 논의/결정 안건)
  - **[결정] GW Admin API 커서 페이지네이션 응답 엔벨로프 통일 (부모 OpenAPI `spec-v1.0.19`)** — Console 구현(`T-FE-0-2`) 중 발견. `cursor`·`limit` 파라미터를 받는 오퍼레이션 **13개 중 10개가 맨 배열을 반환**해 `nextCursor`를 실을 자리가 없다 → **계약상 2페이지 이후를 요청할 방법이 없다.**
    - 엔벨로프(3): `getAdminFleet`·`getAdminClients`·`getAdminClinicClients` / **맨 배열(10)**: `getAdminDevices`·`getAdminOperators`·`getAdminAccessRequests`·`getAdminClinics`·`getAdminClinicDevices`·`getAdminAudit`·`getAdminOrgMappings`·`getAdminWebhookEvents`·`getAdminConfig`·`getAdminPolicies`
    - 영향: SCR-DEV-01·SCR-RBAC-03·SCR-AUDIT-01·SCR-WH-01 등 **Console 목록 화면 대부분**(P2~P6). IP `T-FE-1-8`·`T-FE-2-1` 등의 dod가 커서 페이지네이션을 요구하는데 계약상 성립하지 않는다. GW 백엔드 구현이 이미 배열을 반환한다면 **응답 형태 변경 = breaking change**라 GW 측 작업도 동반된다.
    - 부수: `limit` 기본값이 오퍼레이션마다 **20/50으로 갈리고** 4개는 `maximum` 미선언 → 함께 정리 권장.
    - 조치안: 부모 스펙 세션에서 `{items, nextCursor}`로 통일(공용 `*Page` 스키마 재사용). Console은 그때까지 **다음 페이지 없음으로 degrade**(어댑터가 두 형태 모두 처리하므로 계약 수정 시 Console 코드 변경 불요).
  - _(이번 주 결정사항 = 스펙 세션 정리 후 반영 · 회의 중 신규 안건 발생 시 여기 추가 · 보류·선결은 아래 「이월 논의 사항」 표 참조.)_

- 공유 사항 (결정 아님 · 정보 공유 · 매주 상시)
  - **트랙 구분(혼동 방지)** — **GW 백엔드(③)** = S1 Gantt · S2 스펙 테이블 · **S3 구현 현황**(부모 SRS `spec-v1.0.18`·NestJS 코어·구현 Task) / **GW Console(③-C)** = **S4 현황**(전용 repo `vt-api-gateway-console`·frontend·Console SRS. 두 트랙은 **repo·스택·세션이 다르다.** _이번주 진행 항목은 **[GW 백엔드]/[GW Console]/[제품 연동 스펙]** prefix로 트랙을 표시한다._
  - **S1. 프로젝트 일정(Gantt) — 8/13 스냅샷** — 스펙 생애주기(작성→PR→baseline) + GW 구현 타임라인.
    - **진행률(구현)**:
      - **GW ≈ 93%**(IP Task 69/74 머지·코어 구현 완료 — 잔여 5개는 ③-I 인프라·Straumann 의존 통합/E2E/배포로 GW 코드가 아님)
      - **GW Console ≈ 12%**(IP Task 6/51 머지 — P0 0-1~0-6: 스캐폴드·코드젠·MSW·authProvider·App Shell·dataProvider)

    - **목표 = 10월 출시**(역산·잠정 — 2단계는 AXS **PPR 자격 확보로 착수 가능**·잔여 변수 = **prod 자격(NDA후)·부하환경**)
    - **범례** — **막대 색**: 작성=기본 · PR=강조 · ◆=baseline/마일스톤 · **빨강=외부/미정 선결** / **선결(빨강)**: AXS **prod** 자격(NDA 후·Straumann) _(PPR sandbox 자격=확보 8/11 · IO Scanner=AXS webhook 흡수·GW 무관·R1 종료)_

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

        section GW 구현 → E2E → 출시 (구현 ~93% · ③ SRS 완료 직후 착수 · 2단계 병행 · Raymond 부분투입)
        1단계 GW 독립 코어 (③ 고정·④무관·P0~P6·P10·완료) :done, implindep, 2026-07-21, 21d
        2단계 AXS 연동 (P7~P12·P8/9/11 병행·P7 AXS 실연동·P12 부분) :active, implaxs, 2026-07-28, 21d
        AXS E2E (sandbox·12-1 스캐폴드·happy=Straumann 대기)  :e2e, after implaxs, 14d
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

        section ③-C GW Console — gw/1.0 대응 v1.0 (구현 ~5% · frontend·별도 repo·전규현/Raymond)
        SRS 작성 (8/5)                :done, consrsw, 2026-08-05, 6d
        SRS baseline (#12602·8/11)     :milestone, done, consrspr, 2026-08-11, 0d
        v1.0 구현 (별도 frontend 세션·mock-first) :active, conv1, 2026-08-12, 28d
        v1.0 최소기능 완료             :milestone, conv1m, after conv1, 0d
        section ③-C GW Console 후속 (gw/1.1·gw/1.2·GW-무관 부가 — 일정 미고정·상당 후행)
        후속 확장 (해당 GW 역량 활성 후·부가는 요청 시 그때그때) :conv2, after conv1m, 30d
        확장 진행(수시)             :milestone, conv2m, after conv2, 0d

        section v1.0 이후 (deferred · post-v1.0)
        CleverOne 연동 *구현* (스펙은 지금·구현 post-v1.0) :codef, after rel, 14d
    ```

  - **S2. 스펙 작성 테이블 — 제품별 개발 항목 종합 (제품 × 단계) · 매주 스냅샷** · **정본 = 본 Agenda(S2)** (_Roadmap 결정.md 폐기 — 이 표가 현행 정본_)
    - **각 셀 앞 이모지 = 그 항목을 다루는 스펙의 작성 진행**: ✅ baseline · 🟢 PR · 🟡 작성중 · ⬜ 미작성 (— = 해당 없음)

      | 제품 | 0단계(IO Scanner 수집 — **AXS webhook 흡수·GW 무관·R1 종료**) | 1단계(호환성) | 2단계(presigned) | 3단계(GW 일원화) | 4단계(멀티리전) | 5단계(Straumann) | 후속 | 스펙 산출물(단위·유형) |
      | --- | --- | --- | --- | --- | --- | --- | --- | --- |
      | **CleverSpace** | — | 🟡 서버 버전 체크·well-known·오류코드 | 🟡 presigned 발급 API 신규 | 🟡 GW 경유 수신 정합 | ⬜ 멀티 Region 구축 | — | — | **🟢 ③-P-CS CleverSpace OnePager 인계(PR #12239·EzCloud `docs/onepager/gw_adaptation`)** — CleverSpace 팀(Larry) 검토 |
      | **CleverOne**(OnePager 지금·연동 구현 post-v1.0) | — | 🟡 Vatech-\* 헤더·well-known·fallback | 🟡 presigned 업로드 이용 | 🟡 Direct→GW 경유 | ⬜ Region 선택 UI(대안)·ClinicID | — | — | **🟢 ③-P-CO CleverOne OnePager 인계(SharePoint gw_adaptation)** — CleverOne 팀(Nick) 검토 · 담당=Nick·작성=Raymond |
      | **EzServer(EZ)** | ⬜ IO Scanner 데이터 수신(방식 R1·**보류**·TBD) | 🟡 헤더 대리 전달 | 🟡 전송 로직(presigned 직접) | 🟡 GW 경유 전환 | 🟡 ClinicID·Region·클리닉 등록(잠정) | 🟡 AXS(갈래A)·presigned 직접(IO Scanner 세부=TBD) | ⬜ Rust 재개발 | **🟡 ③-P-EZ One Pager 초안 작성됨**(Raymond→EzServer 팀) — `specs/03p-ez-ezserver/EzServer-GW적응-OnePager.md` · ④(갈래A) |
      | **CleverLab** | — | — | — | — | — | ⬜ AXS 오더·상태·확정(갈래B)·presigned | — | ④ Sub-SRS(갈래B) |
      | **VatechAPIGateway** | — | 🟢 ↳3단계 흡수(호환 게이트·§7.7) | 🟢 ↳3단계 흡수(presigned 중계·§4.1.4) | 🟢 본체·라우팅·인증·호환·presigned 중계·경로B 흡수 | 🟢 리전 라벨 호스트·Region Directory·HA(K8s)·Route53·RDS(리전 단일) | ⬜ AXS OAuth 중계·Org-ID·온보딩·인바운드·고정IP | — | **③ SRS ✅ baseline v1.0 · 현행 동결 `spec-v1.0.18`**(정합화 누적) · ④ connector ⬜(보류) |
      | **GW Console**(③-C·frontend) | — | — | — | — | 🟢 Admin Web Console gw/1.0 대응(MS Entra 앱계층·Admin API Entra-gated) | ⬜ 온보딩·Org-ID 관리 등 **후속**(gw/1.1·1.2·부가·미정) | — | **✅ ③-C Sub-SRS baseline(`spec-v1.0`·#12602 머지 8/11)** · 구현=별도 frontend 세션 → **S4** |
      | **인프라** | — | — | — | 🟢 dev·qa·stag(단일 Region)·prod(Region별) | 🟢 Route53·K8s·비-AWS minio | 🟢 AXS 고정IP·샌드박스 | — | **🟢 ③-I IaC 구축 계획서 — PR #11973 병합(7/27)·Jack 상세 반영**(Raymond diagram+SRS추출→Jack) — 정본 `vt-api-gateway-infra` · **baseline tag 불요**(living doc) · **AWS 4계층** · **+ 8/4 KMS 키 토폴로지 provisioning ask**(spec-v1.0.7·handoff-infra 항목5 — 리전별 CMK `gw-payload`/`gw-target-cred`·pod별 grant·dev payload CMK 선생성) |
      | **외부(Straumann AXS)** | — | — | — | — | — | 🟡 **PPR sandbox 자격=확보(8/11)** · ⬜ prod(정식계약)=NDA 후(선결) | — | ④ 입력(외부 제공) |
      | **LMP(License Portal, 바텍)** | — | — | — | — | — | — | ⬜ (조건부) 제3자 서명 attestation | **enroll B안 시만**·ES 라이선스팀(R9·B-42) |

    - **스펙 문서 등록처·경로·baseline (SSOT)** — 각 제품 스펙 정본의 Repo·경로·태그. _(미정 = R3에서 등록처 확정 · OnePager는 담당팀 baseline 시 tag 부여)_

      | 단위 | 스펙 문서 | Repo (Azure DevOps) | 경로 | baseline tag |
      | --- | --- | --- | --- | --- |
      | **③ GW** | SRS(+OpenAPI·DBML·UnitTCL) | `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway` | `docs/specs/SRS.md` · `docs/specs/design/`(openapi·dbml) · `docs/specs/UnitTCL.md` | **`spec-v1.0.18`**(현행 동결 · baseline v1.0 후 정합화 누적) |
      | **③-C GW Console** | Sub-SRS | `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console` (전용 repo) | `docs/specs/SRS.md` | **✅ `spec-v1.0`**(baseline·#12602 머지 8/11) |
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

  - **S3. GW 백엔드(③) 구현 현황 — Phase·Task 스냅샷 (8/13·매주 갱신)** _(NestJS 코어·부모 SRS — Console은 S4)_
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
      | **P11** 11-8 | admin ClinicInfo 교정 `PATCH /v1/admin/clinics/{id}`(name·country·address·phone·website·audit `clinic.info.update`·mapping_version 불변)(T-ADM-11-8·스펙-코드 갭) | 🔥 이번주 | #12581 · 계약 기존(OpenAPI patchAdminClinicsById) 미구현이던 갭 · 검증 로직 core self-PATCH 와 libs 공유 추출 · **v1.0.17로 재봉인(아래 11-8b)** |
      | **v1.0.17** 11-8b | ClinicInfo 표시필드 PATCH **v1.0 봉인**(전 역할 403·Console 미노출) — LMP=SoT divergence 방지·식별은 clinic.memo(T-ADM-11-8b) | 🔥 이번주 | #12603 · `CLINIC_INFO_WRITE_ROLES=[]`→RbacGuard deny-by-default · 엔드포인트/service/검증 삭제없이 유지(재개방 X→O escape hatch) · 4역할 전부 403 e2e · 독립리뷰 actionable 0 · DB 변경 없음 |
      | **P7** 7-1 | External Connector 아웃바운드 OAuth2 토큰(client_credentials·soft-state 캐시·dual-window·§7.1.3) | 🔥 이번주 | #12561 · 독립리뷰 High(fetch 타임아웃) 수정 |
      | **P7** 7-4 | 클리닉 self org-binding 자가 등록(`POST /v1/clinics/me/org-bindings`→org_mapping·§2.3.4) | 🔥 이번주 | #12562 |
      | **P7** 7-5 | presigned 중계 리전 guardrail wiring(TC-REG-42·§7.3.3·verbatim 중계=P6 기구현) | 🔥 이번주 | #12564 · 독립리뷰 Critical/High 다수 차단 |
      | **P7** 7-2 | egress allowlist SSOT+PDP egress 집행(fail-closed·§7.5.3) | 🔥 이번주 | #12564(7-5 와 공동 PR) · egress 집행 로직은 P4 T-REG-4-4(#12187)에 기구현 → 이번주 7-2 Task 로 확인·종결 |
      | **P7** 7-3 | AXS 커넥터 최초 실연동(아웃바운드 커넥터 토큰·Organization-ID 주입·verbatim·fail-closed) | 🔥 이번주 | #12584(Phase1) · AXS PPR 샌드박스 자격 확보 → 아웃바운드 배선(토큰/Org-ID 주입·스푸핑 차단)·실 AXS 왕복 실측 · 업무 API happy=AXS org **consent 선결**(Straumann 수령 대기) |
      | **T-E2E-12-1** 실-AXS e2e | 실-AXS regression 스위트(skip-가드·`test:e2e:axs`)+아웃바운드 실측 3케이스 · **실 AXS 가 GW gzip content-encoding 버그 노출·수정**(모든 gzip 업스트림 영향) | 🔥 이번주 | #12600(Phase2) · 업무 happy=consent·인바운드 webhook=공개 ingress·CI 게이트=변수그룹 후속 |
      | **T-E2E-12-2** compat 게이팅 e2e | semver 3단계 게이팅(TC-CFG-18~22·major 차단·minor 경고·patch 무시·헤더 누락·originator/Via worst)을 **실 HTTP 왕복**으로 재실행(실 미들웨어+실 가드·**프로덕션 코드 무변경·순수 테스트**) | 🔥 이번주 | #12606 초판(17)→ **v1.0.18에서 고정 fixture로 운영 분리·33 케이스 확장(#12612)** · 가드=opt-in·실 EP 미배선이라 테스트 probe 에 실 가드 부착 · 독립리뷰 High/Med 0 |
      | **v1.0.18** T-CFG-5-4 compat-matrix 발행 | 호환성 매트릭스 **YAML(SSOT)→JSON 렌더러·발행 파이프라인·검증**(정합화·계약/DB 무변경) — 발행 게이트(스키마·표준 errorCode/제품 allowlist·id 유일·≤8KB) · 생성 JSON 미커밋(gitignore·SSOT=yaml) · **행동 e2e는 고정 fixture로 운영과 분리**·yaml→json→서빙 파이프라인 e2e 신설 | 🔥 이번주 | #12612 + #12613(파이프라인 분리) · **compat-matrix.yml=validate 전용**(GW 단독·**등록됨·Azure 실행 succeeded**·PR 게이트) / **compat-matrix-publish.yml=publish**(③-I grant 선결이라 repo 저작만·**등록은 ③-I 나중에**·Azure는 커넥션을 파싱시점 검사라 분리 불가피) · 독립리뷰 2회(High/Med 0·48/48 실행검증) · 실 min 값=One Pager 후 |
      | ─ **대기·무영향** ─ |  |  |  |
      | **P0** 0-5 | CI 파이프라인·Dockerfile(4타겟·스캔·lint·build·unit·e2e 게이트)=완료 · **자동배포(CD) 잔여** — ECR/ArgoCD·main→DEV·tag prefix→TEST/PROD(deploy stage `condition:false` 자리표시자·T-PLAT-0-5 `[~]부분완료`) | 🔴 부분 | ③-I(Jack Azure Flow 템플릿 수령 후) · Dockerfile es-base 전환(0-5b)=완료(#12163) |
      | **P9** 9-5 | device **실** IoT 프로비저닝(Thing/정책 attach·실 cert 발급 인프라) | 🔴 대기 | ③-I/④ IoT Core(cert 발급 app-side=v1.0.12(A) 완료·DBML `iot_certificate_id`=스펙 세션) |
      | **P12 E2E·하드닝** | 12-1 AXS sandbox E2E(부분·#12600) · **12-2 compat E2E=완료(#12606·이번주)** · 12-3 부하 · 12-4 HA/KEDA | ◑ 진행 | 🔴 잔여 선결: 12-1 happy=④ AXS consent · 12-3=부하환경 · 12-4=③-I(Multi-AZ) |

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

  - **S4. GW Console(③-C) 현황 — frontend · 전용 repo (8/13)** _(GW 백엔드=S3와 분리 — repo·스택·세션 다름)_
    - **repo·스택**: `vt-api-gateway-console`(전용) · Next.js + Refine(headless) + shadcn/ui + TanStack Query · 부모 GW Admin API를 **코드젠으로 소비**(자체 백엔드 없음). **버전 확정(8/12·T-FE-0-1)** = Next 16.3.0(App Router·Turbopack)·React 19.2.8·Refine 5.0.12·TanStack Query 5.101.4·shadcn CLI 4.17.0(base=radix·Tailwind v4)·pnpm 9.15.9 · dev 포트 3100.
    - **폰트 = CleverSpace(호스트)와 통일(8/12)**: `'Noto Sans','Noto Sans KR','Segoe UI',sans-serif`. 단 로딩은 Google Fonts CDN 링크가 아니라 **`next/font` 자체 호스팅** — 런타임 외부 요청이 없어 CSP 허용 도메인을 늘리지 않는다(SRS §6.2·C-3). _(Next 템플릿 기본값 Geist는 한글 글리프가 없어 한글이 브라우저 기본 폰트로 떨어지던 문제도 함께 해소.)_
    - **SRS**: ✅ **baseline v1.0**(#12602 머지 8/11 · tag `spec-v1.0`). gw/1.0 대응 완전 규격 + gw/1.1·gw/1.2·후속은 방향. 리뷰(민진우·정우혁) 반영·스레드 resolve.
    - **구현 착수(8/12)**: 별도 **frontend 세션** 오픈 완료 → P0 진행중(`T-FE-0-1` 스캐폴드 **PR #12617 머지**). Task 단위 PR → 사람 머지(유인 모드·IP §7). **Entra/실 GW 없이 mock으로 대부분 진행 가능**(실배포 선결만 = C-2 Entra·C-10 도메인·C-3 CORS = ③-I/IT).
    - **로컬 실데이터 확인 시점**: GW Admin이 Entra-gated라 **P1(인증·RBAC) 완료 후**부터 로컬 GW(Docker)+로컬 Postgres 실데이터를 브라우저로 상시 확인 가능(P8 대기 불필요). 그 전에는 MSW mock 화면.
    - **GW(백엔드)와의 경계**: Console = Admin API(§7.9) 소비 + well-known/Region Directory 읽기만. **구현 경계** — enroll cert 발급·operator authz 복제·compat-matrix 발행은 **GW/③-I 소관(Console 아님)**. Console→부모 계약 반영은 부모 spec PR로(예: 표시필드 PATCH 봉인=`spec-v1.0.17`).
    - **참고** — 계약=Console SRS baseline(`spec-v1.0`) 동결·부모 계약 핀 `spec-v1.0.18` · Task별 검증(`typecheck`·`lint`·`format:check`·`build` + 각 Task `dod[]`) · **PR 전 독립 적대 리뷰 게이트**(`rv_prompt`·CodeReviewAgent 동일 규칙) 통과 필수 · 매 Task 완료 시 갱신
    - **상태 범례**(S3와 동일): 🔥 **이번주 완료**(8/6 회의 이후 main merge) · ✅ 이전 완료 · 🟠 진행중/착수예정 · ⬜ 대기 · 🔴 외부/인프라 선결. **표기 규칙(8/13)**: **이번주 완료(🔥)는 Task 단위**로 전개(진척 가시화) · **완료 Phase(지난주까지·전체 동일 상태)는 Phase 1행**으로 묶음 · **Phase 내 상태가 다른 Task만 별도 행**(예: P0-1) · 미착수 Phase = 1행.

      | Phase / Task | 범위 | 상태 | PR·비고 |
      | --- | --- | --- | --- |
      | ─ **선행 스펙·계획 (완료·1행)** ─ |  |  |  |
      | **Console SRS** | gw/1.0 대응 완전 규격 + gw/1.1·1.2·후속 방향 | ✅ 완료 | #12602 머지 8/11 · baseline `spec-v1.0` · 리뷰(민진우·정우혁) 반영 |
      | ─ **이번주 완료 🔥 (8/6~8/13·Task 단위) + 진행 Phase(P0)** ─ |  |  |  |
      | **P0** 0-1 | Next 16.3.0+Refine 5(headless)+shadcn(radix·Tailwind v4)+TanStack Query 스캐폴드 · dev 포트 3100 · `app/`+`src/`(별칭 `@/*`→`./src/*`) · ESLint+Prettier · 온보딩 README · `.env.example` · **폰트 CleverSpace 통일**(Noto Sans/KR·next/font 자체 호스팅) | 🔥 이번주 | **#12617**(머지 `5d20fbc`) · 독립리뷰 2라운드 반영 12건·스킵 1건(테스트 하네스=0-8) · 실결함 3건 수정(한글 폰트 폴백 미종결·`font-mono` 무동작·Node 20.9/20.10 config 로드 사망) · dataProvider=자리표시자(0-2/0-6에서 교체) · 정적 export 전환=0-10 이연 |
      | **P0** 0-2 | 부모 OpenAPI 코드젠(openapi-typescript Node API)+타입 클라이언트(openapi-fetch)+커서 페이지네이션 어댑터+`codegen:api --check` 드리프트 감지·Vitest unit 프로젝트(25 케이스) | 🔥 이번주 | **#12621**(머지 `6223e8b`) · 독립리뷰 2라운드 반영 8건·스킵 3건 · 생성물 커밋·헤더에 계약 리비전 git 실측 · **부모 계약 이슈 발견**(커서 페이지네이션 — 아래 이월 논의 참조) |
      | **P0** 0-3 | MSW 목 — accessState 3케이스 × 역할 4종 시나리오(`?mock=` 전환)·`/v1/admin/me` 핸들러(경로를 계약 경로로 타입 제한·origin 와일드카드)·browser/server 진입점 | 🔥 이번주 | **#12623**(머지 `ff8f127`) · **리뷰가 High 1건 적발**: 목이 prod 번들에 남아 있었다(=인증 우회 경로 배포) → 리터럴 `NODE_ENV` 가드로 해소, 청크 1.2M→900K·MSW 참조 1→0 실측 · 활성 조건 = `AUTH_MODE=mock` AND `NODE_ENV!==production` |
      | **P0** 0-4 **risk:auth** | authProvider `AUTH_MODE=mock\|entra` 스위치(entra=OIDC 배선 골격·토큰 sessionStorage·401 로그아웃/403 유지) + accessControlProvider **deny-by-default** 골격 + `verify:bundle` 배포본 검사 스크립트 | 🔥 이번주 | **#12626**(머지 `19eac25`) · **risk:auth 기계 검증**: `.next/static`+`.next/server` 266파일에서 우회 표지·mock fixture·MSW **0건**, 가드 제거 대조 빌드 1건 검출로 검사 유효성 확인 · 구현 중 tree-shaking 실패 2건 자체 적발(조건을 함수로 감싸면 안 접힘 = 0-3 MSW와 동일 유형·미사용 export 표지는 항상 제거돼 무용지물) · 리뷰 반영 3건 |
      | **P0** 0-5 | App Shell 3-영역 골격(App Bar·Sidebar·메인+브레드크럼·각 영역=슬롯)+로딩/오류/빈 공통 컴포넌트(무한 로딩 금지·재시도)·vitest component 프로젝트(jsdom+RTL) 신설 | 🔥 이번주 | **#12627**(머지 `d15b076`) · `test:component` 15 케이스 · Sidebar 역할 게이팅은 의도적 미적용(deny-by-default라 지금 걸면 전 항목 소멸 → 1-3에서) · 리뷰 반영 4건 + **High 1건 실측 반증**(한글 폰트 정상 - @font-face 126개·U+AC00 포함) |
      | **P0** 0-6 | env 설정(`NEXT_PUBLIC_*`·목 기본값/실연동 fail-fast) + **dataProvider 실물**(자리표시자 교체·커서 어댑터 연결·리소스↔계약경로를 `keyof paths`로 타입 고정) + Region Directory/well-known 정적 스텁 | 🔥 이번주 | **#12631**(머지 `37896b0`) · `test:unit` 89 케이스 · **리뷰 High**: `.env.example`이 빈 값이라 문서대로 `cp` 하면 목 모드가 즉시 실패(`??`가 빈 문자열을 못 걸름) — 회귀 테스트가 잘못된 이유로 통과하던 것까지 적발 · **계약 실측**: 6개 리소스는 단건 경로 자체가 없고 자리표시자 이름도 리소스마다 다름 |
      | ─ **대기·잔여** ─ |  |  |  |
      | **P0** 0-7~0-10 | i18n Lingui(0-7)·테스트 하네스+CI 게이트(0-8)·README(0-9)·리뷰용 mock 정적배포(0-10) | ⬜ 대기 | P0 진행중(10 중 6 완료) · **다음 착수=0-7**(i18n Lingui 스캐폴드) · **`verify:bundle` CI 배선=0-8**(그 전까지 로컬 수동) |
      | **P1** 인증·RBAC·홈 | 1-1~1-9(로그인·`/me` 부트스트랩 분기·리전 스위처·역할별 홈·권한 요청/승인·운영자 관리) | ⬜ 대기 | risk:auth(1-5 매트릭스·1-9 last-admin 가드) · **완료 시 로컬 GW 실데이터 확인 가능** |
      | **P2** enrollment·디바이스 | 2-1~2-5(디바이스 목록/상세·enrollment 승인/거부·수명주기 suspend/resume/kill) | ⬜ 대기 | ★서비스 개통 게이트 · 2-5 kill=비가역 사람 확인 |
      | **P3** 클리닉 | 3-1~3-4(목록/상세·LMP 읽기전용·식별 memo 편집·Device↔Clinic 드릴스루) | ⬜ 대기 | 표시필드 PATCH=봉인(미노출·`spec-v1.0.17`) |
      | **P4** 연동 대상·정책·org-mapping | 4-1~4-4(target 등록 3섹션 폼·삭제 409 가드·정책 편집·org-mapping 관리) | ⬜ 대기 | credential 마스킹 · stale-write 베이스라인(4-3) |
      | **P5** webhook·break-glass | 5-1~5-3(이벤트 메타 조회·payload break-glass 열람 PHI) | ⬜ 대기 | risk:security(5-3 PHI 마스킹) · 열람 역할=C-5 확정 대기(잠정 admin) |
      | **P6** fleet·config·매트릭스·감사 | 6-1~6-5(fleet 대시보드·SW 인벤토리·중앙 config·**매트릭스 뷰어**·감사 로그) | ⬜ 대기 | 매트릭스 발행은 GW 소관(Console=뷰어) |
      | **P7** 공통 UX·i18n·동시성·보안 | 7-1~7-7(세션 만료·403·오류 재시도·stale-write 전체 적용·i18n·보안 리뷰·접근성/시각회귀 게이트) | ⬜ 대기 | risk:security(7-6 저장 점검) |
      | **P8** 실 e2e·시각회귀·배포 | 8-1~8-4(Entra dev 전환·staging GW e2e·시각 baseline 승인·prod 배포) | 🔴 대기 | 선결 C-2(Entra)·C-10(도메인)·C-3(CORS)=③-I/IT · C-10 미확정 시 8-4는 BLOCKER |

  - **S4-1. 커버리지 계획 (frontend · 착수 후 실측 · S3-1 대응)** — Console도 커버리지 측정·CI floor 게이트를 둔다(SRS §3.5·§3.6.2). **BE와 방식 차이**: BE의 merged(unit+e2e 합산·보안파일 개별 100%) 대신, Console은 **Vitest(v8) 기준 unit+component 커버리지**를 정본으로 하고 e2e는 여정 커버리지로 별도 관리. **실측 값은 `T-FE-0-8`(테스트 하네스) 이후·각 Task 완료 시** 아래 표에 채운다(현재 미착수라 값 없음).
    - **측정 대상·비대상**: 라인% = Vitest(unit+component) · **e2e(Playwright)** = 핵심 여정 커버리지 체크리스트(로그인·enroll 승인·break-glass·RBAC 403·리전 컨텍스트) · **시각회귀·접근성(axe)** = %가 아닌 pass/fail 게이트.

      | 스코프                                                            | Statements | Branches  | Functions | Lines     | 비고                             |
      | ----------------------------------------------------------------- | ---------- | --------- | --------- | --------- | -------------------------------- |
      | **① 전역 (unit+component)**                                       | 측정 예정  | 측정 예정 | 측정 예정 | 측정 예정 | Vitest(v8) · 착수 후 실측        |
      | **② 민감 로직** (권한 게이팅·PHI 마스킹·stale-write·dataProvider) | 측정 예정  | 측정 예정 | 측정 예정 | 측정 예정 | BE '보안 도메인' 대응 서브스코프 |
      | **CI 게이트 floor**                                               | TBD(LLD)   | TBD(LLD)  | TBD(LLD)  | TBD(LLD)  | 임계값=LLD 확정(§3.5·§3.6.2)     |

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
