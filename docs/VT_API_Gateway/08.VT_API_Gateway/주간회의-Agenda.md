# VT API Gateway — 8/20 주간회의 Agenda

- 이번 주 진행 _(프레임 · 8/20 회의 시 확정 · 상세·수치는 아래 논의 R#/공유 S# 한 곳에만)_
  - **[GW 백엔드]** **AXS 파일 전송 개정 구현 완료 — 4 PR 머지**(spec-v1.0.20~24) — 커넥터 전략(connector_type 파생·DBML 무변경)·다운로드 전체경로 E2E·파일 webhook 라우팅 E2E·업로드 토큰 위임 사이드카 _(상세 = 공유 S3)_
    - 업로드=fss OAuth(presigned 아님) → GW 가 create-document 응답에 위임 토큰 사이드카 부착→EzServer 직접 업로드(바이트 GW 미경유) · 다운로드=Blob SAS 미경유 유지
    - AXS 아웃바운드 E2E(토큰·Org-ID·verbatim·happy 200·fail-closed) 완료 유지
    - 잔여는 전부 외부 선결(③-I 공개 ingress·실 IoT Core / Straumann prod 자격 / 부하환경)
  - **[GW Console]** **P1 인증·RBAC 완료(9/9) → P2 진행(4/5) — ★개통 게이트 통과** — Entra 로그인·`/me` 부트스트랩 분기·역할×액션 매트릭스·App Shell(리전 컨텍스트)·홈 대시보드 + **디바이스 목록·상세·enrollment 승인·수명주기(SCR-DEV-01~03)** _(상세 = 공유 S4)_
  - **[제품 연동 스펙]** EzServer OnePager 수령 확인 (잔여)
  - _(이번 주 결정사항 = 회의 시 추가)_

- 논의 사항 (이번 주 · 신규 논의/결정 안건)
  - _(이번 주 결정사항 = 스펙 세션 정리 후 반영 · 회의 중 신규 안건 발생 시 여기 추가 · 보류·선결은 아래 「이월 논의 사항」 표 참조.)_

- 공유 사항 (결정 아님 · 정보 공유 · 매주 상시)
  - **[GW 스펙 결정·2026-08-13] webhook 하행 MQTT = envelope 없는 payload verbatim · 128KB 초과 = v1.0 미지원(명시 제한)** — 스펙(§7.6.6 "얇은 envelope")이 실제 구현(무-envelope verbatim)과 달라 구현 기준으로 정정. 하행은 원 payload를 wrapper 없이 verbatim 발행(EzServer 맥락 = 토픽 clinicId + payload 필드 messageId·eventType 등). IoT Core 128KB 초과 payload는 **v1.0 미처리 · 절대 자르지 않음**(알림/PHI 무결성) → 발행 실패 시 **DLQ·알람으로 표면화**(무통보 유실 없음). 대용량 오프로드+포인터 폴백은 gw/1.1+ 백로그. (AXS 파일 전송 PR #12669에 흡수)
  - **S1. 프로젝트 일정(Gantt) — 8/20 스냅샷** — 스펙 생애주기(작성→PR→baseline) + GW 구현 타임라인.
    - **진행률(구현)**:
      - **GW ≈ 97%**(**AXS 파일 전송 개정 4 PR 완료**[7-6 커넥터전략·12-8 다운로드·12-9 webhook·7-7 업로드위임+12-7]·spec-v1.0.24 — 코어·AXS 연동 구현 완료 · **잔여는 전부 외부 게이트**(GW 코드 아님): 12-6 인바운드[③-I ingress+실 IoT]·12-3 부하환경·12-4 HA[③-I Multi-AZ]·9-5 IoT 프로비저닝[③-I]·order 파일 presign[Straumann 시드])
      - **GW Console ≈ 45%**(IP Task 23/51 머지 — **P0·P1 완료** · **P2 진행 4/5·★개통 게이트 완료**)
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

        section GW 구현 → E2E → 출시 (구현 ~97% · ③ SRS 완료 직후 착수 · 2단계 병행 · Raymond 부분투입)
        1단계 GW 독립 코어 (③ 고정·④무관·P0~P6·P10·완료) :done, implindep, 2026-07-21, 21d
        2단계 AXS 연동 (P7~P12·P8/9/11 병행·P7 AXS 실연동·P12 부분) :active, implaxs, 2026-07-28, 21d
        AXS E2E (sandbox·12-1·업무 happy 커버 #12655·webhook 인바운드=③-I 대기)  :e2e, after implaxs, 14d
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

        section ③-C GW Console — gw/1.0 대응 v1.0 (구현 ~45%·P0·P1 완료·P2 진행 · frontend·별도 repo·전규현/Raymond)
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
      | **VatechAPIGateway** | — | 🟢 ↳3단계 흡수(호환 게이트·§7.7) | 🟢 ↳3단계 흡수(presigned 중계·§4.1.4) | 🟢 본체·라우팅·인증·호환·presigned 중계·경로B 흡수 | 🟢 리전 라벨 호스트·Region Directory·HA(K8s)·Route53·RDS(리전 단일) | ⬜ AXS OAuth 중계·Org-ID·온보딩·인바운드·고정IP | — | **③ SRS ✅ baseline v1.0 · 현행 동결 `spec-v1.0.24`**(정합화 누적) · ④ connector ⬜(보류) |
      | **GW Console**(③-C·frontend) | — | — | — | — | 🟢 Admin Web Console gw/1.0 대응(MS Entra 앱계층·Admin API Entra-gated) | ⬜ 온보딩·Org-ID 관리 등 **후속**(gw/1.1·1.2·부가·미정) | — | **✅ ③-C Sub-SRS baseline(`spec-v1.0`·#12602 머지 8/11)** · 구현=별도 frontend 세션 → **S4** |
      | **인프라** | — | — | — | 🟢 dev·qa·stag(단일 Region)·prod(Region별) | 🟢 Route53·K8s·비-AWS minio | 🟢 AXS 고정IP·샌드박스 | — | **🟢 ③-I IaC 구축 계획서 — PR #11973 병합(7/27)·Jack 상세 반영**(Raymond diagram+SRS추출→Jack) — 정본 `vt-api-gateway-infra` · **baseline tag 불요**(living doc) · **AWS 4계층** · **+ 8/4 KMS 키 토폴로지 provisioning ask**(spec-v1.0.7·handoff-infra 항목5 — 리전별 CMK `gw-payload`/`gw-target-cred`·pod별 grant·dev payload CMK 선생성) |
      | **외부(Straumann AXS)** | — | — | — | — | — | 🟡 **PPR sandbox 자격=확보(8/11)** · ⬜ prod(정식계약)=NDA 후(선결) | — | ④ 입력(외부 제공) |
      | **LMP(License Portal, 바텍)** | — | — | — | — | — | — | ⬜ (조건부) 제3자 서명 attestation | **enroll B안 시만**·ES 라이선스팀(R9·B-42) |

    - **스펙 문서 등록처·경로·baseline (SSOT)** — 각 제품 스펙 정본의 Repo·경로·태그. _(미정 = R3에서 등록처 확정 · OnePager는 담당팀 baseline 시 tag 부여)_

      | 단위 | 스펙 문서 | Repo (Azure DevOps) | 경로 | baseline tag |
      | --- | --- | --- | --- | --- |
      | **③ GW** | SRS(+OpenAPI·DBML·UnitTCL) | `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway` | `docs/specs/SRS.md` · `docs/specs/design/`(openapi·dbml) · `docs/specs/UnitTCL.md` | **`spec-v1.0.24`**(현행 동결 · baseline v1.0 후 정합화 누적) |
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

  - **S3. GW 백엔드(③) 구현 현황 — Phase·Task 스냅샷 (8/20·매주 갱신)** _(NestJS 코어·부모 SRS — Console은 S4)_
    - **어디까지 왔나 (8/20)**
      - 완료
        - 1단계 코어 — P0~P6·P10
        - 2단계 골격 — P8·P9·P11 (로컬 더블 기준·실연동 ④ AXS 후)
      - 직전 주(8/6~8/13) — v1.0.12(enroll CSR→IoT mTLS·Admin CORS)·**P7 커넥터 완료**(7-1~7-5·AXS 최초 실연동)·시스템 E2E(SYS-01/02/04/05)·프록시 복원력 하드닝·v1.0.15~21(enroll Reject·감사 사유·clinic.memo·표시필드 봉인·compat-matrix 발행·**admin device 조회 3라우트**·식별 헤더 2계층)
      - 이번 주(8/13~8/20) — GW 백엔드 main merge **없음**(잔여는 전부 ③-I·Straumann 선결) · **Console(③-C)이 P1 완료→P2 진행**(S4)·11-8(ClinicInfo 교정)
      - 남은 것 (외부·인프라 선결)
        - ④ AXS 실자격 → 7-3(커넥터 실연동)·12-1(sandbox E2E)
        - ③-I 인프라 → 9-5(실 IoT)·9-4(실 KEDA)·0-5(자동배포)·12-4(HA/KEDA)
        - ① One Pager 매트릭스 → 12-2(compat E2E) · 부하환경 → 12-3(부하)
      - 다음 단계 — 개발 통합·검증(통합·시스템 E2E·부하·HA·보안) → QA(회귀·V&V·IEC 62304/ISO 13485) → 운영·릴리스(staging/prod·AXS pilot)
    - **참고** — 스펙=HLD baseline(v1.0) 동결·LLD는 구현 병행 · region-silo 재작업(8/3·#12241)으로 P4 대부분 단일화(단일 datasource·region=배포 상수) · Task별 검증 4종(unit·e2e·curl·DB) · 매 Task 완료 시 갱신
    - **상태 범례**: 🔥 **이번주 완료**(8/13 회의 이후 main merge) · ✅ 이전 완료 · 🟠 진행중/착수예정 · ⬜ 대기 · 🔴 외부/인프라 선결. **표기 규칙(8/20)**: **이번주 완료(🔥)는 Task 단위**로 전개(진척 가시화) · **완료 Phase(지난주까지·전체 동일 상태)는 Phase 1행**으로 묶음 · **Phase 내 상태가 다른 Task만 별도 행**(예: P9-5) · 미착수 Phase = 1행.

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
      | ─ **2단계 완료 Phase (~8/6·Phase 1행)** ─ |  |  |  |
      | **P8 webhook 수신** | 8-1~8-3(HMAC 검증·eventId 멱등·store-then-ack·payload KMS 저장·SQS enqueue) | ✅ 완료 | #12369·#12411·#12414 · 골격(로컬 더블)·실연동 ④ 후 |
      | **P9 Dispatcher·분배** | 9-1~9-4(SQS 소비·대상해석·미해석 DLQ·복호 후 MQTT publish·graceful drain) | ✅ 완료 | #12420·#12471 · 9-5(실 IoT)=대기(아래)·실 KEDA=③-I |
      | **P10 fleet·중앙 config** | 10-1~10-4(heartbeat/fleet_state·CentralConfig·SW 인벤토리·admin fleet/clients 조회) | ✅ 완료 | #12363~12368 |
      | **P11 Admin CRUD** | 11-1~11-6(targets·policies·operators RBAC 생애주기·webhook-events break-glass·audit 전면·데이터분류 스캐폴드) | ✅ 완료 | #12441~12470 |
      | ─ **직전 주 완료 (8/6~8/13·Phase 1행)** ─ |  |  |  |
      | **P6 하드닝** 프록시 복원력 | 장애주입 e2e(504 TARGET_TIMEOUT·502·hang 없음·§7.5.4)+deadline-abort 정규화 | ✅ 완료 | #12569·#12570 · 독립리뷰가 오진단 정정(프로덕션 이미 504) |
      | **P7 External Connector·AXS 연동** | 7-1(아웃바운드 OAuth2 토큰·dual-window)·7-2(egress allowlist SSOT+PDP 집행·fail-closed)·7-3(**AXS 커넥터 최초 실연동**·토큰/Org-ID 주입·verbatim)·7-4(클리닉 self org-binding)·7-5(presigned 중계 리전 guardrail) | ✅ 완료 | #12561·#12562·#12564(7-2·7-5 공동)·#12584 · AXS PPR 샌드박스 자격 확보 후 실 왕복 실측 · 업무 API happy 해소(#12655·org id 교정) · 독립리뷰 Critical/High 다수 차단 |
      | **P11 Admin CRUD 확장** | 11-8 admin ClinicInfo 교정 `PATCH /v1/admin/clinics/{id}`(계약엔 있고 미구현이던 갭) → **11-8b에서 v1.0 봉인**(전 역할 403·Console 미노출·LMP=SoT divergence 방지·삭제 없이 재개방 가능) | ✅ 완료 | #12581·#12603 · `CLINIC_INFO_WRITE_ROLES=[]`→RbacGuard deny-by-default · 4역할 전부 403 e2e |
      | **시스템·compat E2E** | SYS-01(온보딩)·02(webhook 왕복 3앱)·04(kill 전파)·05(운영자 RBAC) + T-E2E-12-2 compat 게이팅(semver 3단계를 **실 HTTP 왕복**으로 재실행·프로덕션 코드 무변경) | ✅ 완료 | #12566~12568 · #12606 초판(17)→고정 fixture 운영 분리·33 케이스 확장(#12612) · 멀티앱 로컬 더블+실 DB/Valkey/SQS/MQTT/KMS |
      | **계약 개정 v1.0.12~21** | 12(A) enroll CSR→IoT cert 발급·(B) Admin API Entra-gated CORS · 15 명시적 Reject+감사 사유(`audit_log.reason`) · 16 `clinic.memo`+admin clinics 목록/상세 · 17 표시필드 PATCH 봉인(→P11 11-8b) · 18 compat-matrix YAML→JSON 발행 파이프라인 · **19 admin device 조회 3라우트**(Console P2 선결·BUG-001 해소) · 20/21 식별 헤더 2계층(`Clinic-Id` 하드 필수화) | ✅ 완료 | #12557·#12497(+#12657 로컬 origin)·#12576·#12578·#12603·#12612·#12613·#12637·#12646 · DB 마이그레이션 3건 · 전체 e2e 518 green |
      | ─ **이번주 완료 🔥 (8/13~8/20) + 진행 Phase(P12 AXS E2E·Task 단위)** ─ |  |  |  |
      | **T-E2E-12-1** AXS 아웃바운드 e2e | 실-AXS regression(토큰·Org-ID 주입·verbatim·**orders/patients happy 200**·org 미연동 403 fail-closed)·실 AXS gzip 버그 수정 | 🔥 이번주 | #12584/#12600/**#12655** · **성격별 3분할**(아웃바운드 완료/presign/인바운드) · happy 500 원인=우리 org id 오설정(`ea789014`→approve org `a1fb9b17`)·**customerNumber 불필요** |
      | **T-E2E-12-5** AXS presign 중계 e2e | presign 발급 중계·바이트 GW 미경유(E2E-SYS-03·아웃바운드) | ◑ 부분(#12660) | **업로드 presign 발급 verbatim 실측 완료**(create `storageUrl`·필드 원형·Org-ID 주입·5/5 green) · **캡처**: `storageUrl`=fss 호스트·서명 없음→fss API 경로 가능성(§4.1.4=스펙 세션 확인) · defer=다운로드 실물(content 선결)·order 파일(Straumann)·바이트 전송=non-goal |
      | **T-CONN-7-6** 커넥터 전략 | `connector_type` 파생(internal_bypass/oauth2_cc)·capability(inject_org_id·delegate_upload_token) 코드 상수·**DBML 무변경** | 🔥 이번주 | **#12673** · proxy.service 주입 분기→`ConnectorStrategy` dispatch(순수 리팩터·기존 7-3 회귀 0)·switch/never fail-open 차단 · external+credential無=verbatim(주입 off·거부 아님·C-07 확정) |
      | **T-E2E-12-8** AXS 다운로드 전체경로 | 문서조회→SAS 다운로드·바이트 **GW 미경유**(§957·Blob SAS)·발급 verbatim·리전 guardrail(TC-REG-42) | 🔥 이번주 | **#12679** · Blob SAS 더블(서명·만료 검증)·무인증 GET 200·만료/위조 403 · guardrail=**AWS-리전 presign 한정 best-effort**(Azure Blob=no-op·AXS 리전주권=org-link ④)·6/6 |
      | **T-E2E-12-9** 파일 webhook 라우팅 | 파일이벤트(uploaded/updated/deleted) GW 관통·`files[].id`·`storageUri` **무필터 verbatim**·무-envelope | 🔥 이번주 | **#12676** · 실 3앱 관통·eventType 무관 라우팅(organizationId만)·eventId 멱등·주권(타 clinic 0건)·4/4 |
      | **T-CONN-7-7** 업로드 토큰 위임 사이드카 + **T-E2E-12-7** | create-document 응답(body `storageUrl` 트리거)에 `X-Vatech-Upload-Authorization`(fresh 위임 토큰)·`-Organization-Id` 부착→EzServer fss 직접 업로드(바이트 미경유) | 🔥 이번주 | **#12684** · `applyResponse` 응답 훅·`acquireDelegatedToken`(캐시 우회 fresh·재사용 금지)·멱등 캐시 밖·redaction 마스킹·`filterResponseHeaders` 위조 봉인(rv High 반영)·5/5 · A-2(멱등 재생 실패=502 신호) spec-v1.0.24 확정 |
      | **T-E2E-12-6** AXS 인바운드+MQTT e2e | 실 AXS→GW webhook 왕복(E2E-SYS-02)+역방향 MQTT 다운링크 실 IoT | 🔴 대기 | ③-I **공개 ingress + 실 IoT Core** 선결(T-DISP-9-5 연관) · 로컬 더블(sys-02) 커버 유지 |
      | ─ **대기·무영향** ─ |  |  |  |
      | **P0** 0-5 | CI 파이프라인·Dockerfile(4타겟·스캔·lint·build·unit·e2e 게이트)=완료 · **자동배포(CD) 잔여** — ECR/ArgoCD·main→DEV·tag prefix→TEST/PROD(deploy stage `condition:false` 자리표시자·T-PLAT-0-5 `[~]부분완료`) | 🔴 부분 | ③-I(Jack Azure Flow 템플릿 수령 후) · Dockerfile es-base 전환(0-5b)=완료(#12163) |
      | **P9** 9-5 | device **실** IoT 프로비저닝(Thing/정책 attach·실 cert 발급 인프라) | 🔴 대기 | ③-I/④ IoT Core(cert 발급 app-side=v1.0.12(A) 완료·DBML `iot_certificate_id`=스펙 세션) |
      | **P12 E2E·하드닝** | **12-1 아웃바운드=완료(#12655)** · **12-5 presign 발급(#12660)** · **12-7 업로드위임(#12684)** · **12-8 다운로드(#12679)** · **12-9 webhook라우팅(#12676)** · **12-2 compat=완료(#12606)** · 12-6 인바운드+MQTT · 12-3 부하 · 12-4 HA/KEDA | ◑ 진행 | ✅ 12-5·12-7·12-8·12-9 완료(AXS 파일 전송 개정) · 🔴 잔여: 12-6=③-I 공개 ingress+실 IoT · 12-3=부하환경 · 12-4=③-I(Multi-AZ) |

  - **S3-1. 커버리지 현황 (구현과 분리 · merged=unit+e2e 합산 · 8/13 재측정·post-v1.0.12/P7/시스템-E2E · 매 Task 완료 시 갱신)** — 커버리지 스윕(1·2·3순위 101 케이스·PR #12372) 후 실측, 이후 Task마다 재측정. 정본 기준 = **merged**(단위+통합 합산). **정지트리 실측·merged floor 게이트 통과**(v1.0.12 A/B·7-1/2/4/5·시스템 E2E SYS-01/02/04/05 반영). _(8/13 재측정: **AXS 파일 전송 개정 4 PR**(7-6 커넥터전략·12-8 다운로드·12-9 webhook·7-7 업로드위임+12-7) + spec-v1.0.20~24 반영 — 신규 로직 전부 unit+e2e 동반이라 **전역·보안 floor + 핵심 보안파일 per-file branch(≥90%·proxy.service 등 16개 각 100%) 모두 통과** · e2e 545 green.)_

    | 스코프                                        | Statements | Branches    | Functions  | Lines      |
    | --------------------------------------------- | ---------- | ----------- | ---------- | ---------- |
    | **① 전역 (merged)**                           | **96.72%** | **91.88%**  | **93.89%** | **96.51%** |
    | **② 보안 도메인 (merged)**                    | **98.51%** | **95.98%**  | **100%**   | **98.42%** |
    | **③ 핵심 보안 파일 16개 (merged·개별)**       | —          | **각 100%** | —          | —          |
    | _참고: 전역 (unit-only)_                      | 77.73%     | 83.02%      | 72.15%     | 78.73%     |
    | **CI 게이트 floor — ① 전역**                  | 92         | 87          | 88         | 92         |
    | **CI 게이트 floor — ② 보안**                  | 95         | 89          | 95         | 95         |
    | **CI 게이트 floor — ③ 핵심파일(개별·branch)** | —          | **90**      | —          | —          |

  - **S4. GW Console(③-C) 현황 — frontend · 전용 repo (8/20)** _(GW 백엔드=S3와 분리 — repo·스택·세션 다름)_
    - **repo·스택**: `vt-api-gateway-console`(전용) · Next.js + Refine(headless) + shadcn/ui + TanStack Query · 부모 GW Admin API를 **코드젠으로 소비**(자체 백엔드 없음). **버전 확정(8/12·T-FE-0-1)** = Next 16.3.0(App Router·Turbopack)·React 19.2.8·Refine 5.0.12·TanStack Query 5.101.4·shadcn CLI 4.17.0(base=radix·Tailwind v4)·pnpm 9.15.9 · dev 포트 3100.
    - **폰트 = CleverSpace(호스트)와 통일(8/12)**: `'Noto Sans','Noto Sans KR','Segoe UI',sans-serif`. 단 로딩은 Google Fonts CDN 링크가 아니라 **`next/font` 자체 호스팅** — 런타임 외부 요청이 없어 CSP 허용 도메인을 늘리지 않는다(SRS §6.2·C-3). _(Next 템플릿 기본값 Geist는 한글 글리프가 없어 한글이 브라우저 기본 폰트로 떨어지던 문제도 함께 해소.)_
    - **SRS**: ✅ **baseline v1.0**(#12602 머지 8/11 · tag `spec-v1.0`). gw/1.0 대응 완전 규격 + gw/1.1·gw/1.2·후속은 방향. 리뷰(민진우·정우혁) 반영·스레드 resolve.
    - **구현 착수(8/12)**: 별도 **frontend 세션** 오픈 완료 → **P0(10/10)·P1(9/9) 완료(8/13) → P2 진행(4/5·★개통 게이트 완료)**. Task 단위 PR → 사람 머지(유인 모드·IP §7). **Entra/실 GW 없이 mock으로 대부분 진행 가능**(실배포 선결만 = C-2 Entra·C-10 도메인·C-3 CORS = ③-I/IT).
    - **로컬 실데이터 확인 시점**: GW Admin이 Entra-gated라 **P1(인증·RBAC) 완료 후**부터 로컬 GW(Docker)+로컬 Postgres 실데이터를 브라우저로 상시 확인 가능(P8 대기 불필요). 그 전에는 MSW mock 화면.
    - **⚠ Entra 실환경 검증은 아직 0회(8/13)**: `T-FE-1-1`이 OIDC를 **코드로는 실배선**했으나 실 테넌트 로그인은 IT 앱 등록 회신 이후다. 그때 소진할 체크리스트(선행 5·확인 9·함정 5·배포 호스트 전용 1)를 **`_backlog-console.md` §"Entra 실환경 검증 대기"** 에 확정해 뒀고, IP `T-FE-8-1`이 이를 DoD로 참조한다.
    - **GW(백엔드)와의 경계**: Console = Admin API(§7.9) 소비 + well-known/Region Directory 읽기만. **구현 경계** — enroll cert 발급·operator authz 복제·compat-matrix 발행은 **GW/③-I 소관(Console 아님)**. Console→부모 계약 반영은 부모 spec PR로(예: 표시필드 PATCH 봉인=`spec-v1.0.17`).
    - **참고** — 계약=Console SRS baseline(`spec-v1.0`) 동결·부모 계약 핀 `spec-v1.0.20` · Task별 검증(`typecheck`·`lint`·`format:check`·`build` + 각 Task `dod[]`) · **PR 전 독립 적대 리뷰 게이트**(`rv_prompt`·CodeReviewAgent 동일 규칙) 통과 필수 · 매 Task 완료 시 갱신
    - **상태 범례**(S3와 동일): 🔥 **이번주 완료**(8/13 회의 이후 main merge) · ✅ 이전 완료 · 🟠 진행중/착수예정 · ⬜ 대기 · 🔴 외부/인프라 선결. **표기 규칙(8/20)**: **이번주 완료(🔥)는 Task 단위**로 전개(진척 가시화) · **완료 Phase(지난주까지·전체 동일 상태)는 Phase 1행**으로 묶음 · **Phase 내 상태가 다른 Task만 별도 행**(예: P0-1) · 미착수 Phase = 1행.

      | Phase / Task | 범위 | 상태 | PR·비고 |
      | --- | --- | --- | --- |
      | ─ **선행 스펙·계획 (완료·1행)** ─ |  |  |  |
      | **Console SRS** | gw/1.0 대응 완전 규격 + gw/1.1·1.2·후속 방향 | ✅ 완료 | #12602 머지 8/11 · baseline `spec-v1.0` · 리뷰(민진우·정우혁) 반영 |
      | ─ **지난주까지 완료 (~8/13·Phase 1행)** ─ |  |  |  |
      | **P0 플랫폼 스캐폴드** | 0-1~0-10(Next 16.3+Refine 5 headless+shadcn 스캐폴드·부모 OpenAPI 코드젠+커서 어댑터·MSW 목(accessState×역할)·authProvider 스위치+deny-by-default·App Shell 3영역+3상태·env/dataProvider 실물·i18n(Lingui)·테스트 하네스+CI 8게이트·README 신규 클론 실검증·리뷰용 mock 정적 프리뷰) | ✅ 완료 | #12617~#12644 · **폰트 CleverSpace 통일**(Noto Sans/KR·next/font 자체 호스팅) · **목이 prod 번들에 실리는 사고를 게이트가 2회 적발**(리터럴 `NODE_ENV` 가드·미설정 `NEXT_PUBLIC_*` 미치환) → `verify:bundle` 양방향화 · **부모 계약 버그 2건 발견**(커서 엔벨로프 미통일→v1.0.19 · admin device 조회 3라우트 미구현→BUG-001) · 잔여: Build validation 등록(사람 1회)·배포 인프라 grant(③-I) |
      | ─ **이번주 완료 🔥 (8/13~8/20·Task 단위) + 진행 Phase(P1)** ─ |  |  |  |
      | **P1** 1-1 | SCR-AUTH-01 로그인·세션 — **Entra OIDC(Auth Code+PKCE) 실배선**(`@azure/msal-browser`·캐시 sessionStorage) · `/login` 자동 리다이렉트+실패 사유+수동 fallback · `/auth/callback` 교환·복귀 경로 · 미인증 게이팅 | 🔥 이번주 | **#12658**(머지 `0ea8af0`) · 176 unit+component·e2e 7·a11y 2·커버리지 88.8/85.7/86.8/91.1 · **자체 적발 3건**(MSAL v5는 `navigateToLoginRequestUrl`이 config가 아니라 호출 인자이고 **기본값 true** → 빠뜨리면 콜백 화면이 렌더 전에 밀려나 복귀 경로·실패 사유가 동시에 죽음 / 실패한 초기화 Promise가 캐시에 남아 새로고침 전까지 로그인 영구 차단 / fallback 버튼이 정작 필요한 30초간 잠김) · ⚠ **실 Entra 로그인은 미검증**(목 경로까지) → 8-1·`_backlog-console.md` 체크리스트 · ⚠ **배포 딥링크 결함 실측**: CloudFront(OAC+404→`index.html`)만으론 `/auth/callback`이 홈으로 떨어져 code 미처리 → **CloudFront Function 경로 rewrite 필요**(③-I 요청서 §2 보강 대상) |
      | **P1** 1-2 | `/me` 부트스트랩 분기(accessState 3분기·역할 우선순위 착지) + `app/(shell)` 레이아웃으로 게이팅 집약 + dataProvider `custom` | 🔥 이번주 | **#12659**(머지 `5073c25`) · 213 unit+component·e2e 14·a11y 4 · **자체 적발**: `/me` 200+빈 본문에 셸이 `TypeError`로 통째 사망(dataProvider가 빈 본문을 null로 준다 — T-FE-0-9의 그 계약 특성) → 오류+재시도로 전환, **가드 제거 대조**로 회귀 테스트 유효성 확인 · 착지 대상 화면(P2·P6) 미존재라 **구현된 경로에만 착지**(없는 경로=로그인 직후 404=로그인 실패와 구분 불가), 위험 방향은 테스트가 `app/` 트리와 대조해 차단 |
      | **P1** 1-5 **risk:auth** | SRS §7.2 역할×액션 매트릭스(**21행×4역할**) 코드화 + accessControlProvider 실판정 + Sidebar 메뉴 게이팅(무권한 비노출) | 🔥 이번주 | **#12663**(머지 `09e9a62`) · 270 unit+component·e2e 19·커버리지 90.2/86.9/89.0/92.0 · **자체 적발 2건**: ① **실제 앱에서 메뉴 전멸** — `useCan` 결과를 TanStack Query가 캐시하는데 키에 세션이 없고 이펙트가 자식→부모 순이라 "부트스트랩 전=거부"가 굳음(컴포넌트 테스트로는 원리상 못 잡음 → **e2e 추가**, 가드 되돌린 대조에서 6건 실패로 유효성 확인) ② 매트릭스를 SRS에서 **독립 전사**해 대조하다 불일치 1건 적발(감사 로그 developer 열 — 구현이 맞음) · **미충족(의도적)**: `[manual]` 서버 403 실강제는 실 GW 없이 증명 불가 → 8-1로 이관 |
      | **P1** 1-3 | SCR-AUTH-02 App Shell 완성 — Region Directory 연동 리전 컨텍스트 · 승인 대기 badge · 운영자 메뉴(로그아웃) · App Bar 슬롯을 셸이 기본 충전 | 🔥 이번주 | **#12665**(머지 `597adf9`) · 308 unit+component·e2e 26·a11y 4·커버리지 91.2/86.7/91.4/93.4 · **리전 1개면 스위처 없이 컨텍스트 표시**(선택지 1개 select는 조작하는 척만 함) · 단일 리전은 env `GW_ADMIN_BASE` 유지(Directory host로 덮으면 로컬 개발 즉사) · 리전 전환 시 이전 리전 데이터는 버리되 `/me`는 유지(역할=전 리전 균일 복제·결정 G) · 로컬 스텁 `regions.json`을 **prod 시드니→dev 서울(apne2)** 교정 · ⚠ **Directory 스키마에 `adminHost` 없음**(Console이 부르는 호스트가 계약에 없고 DNS 관례로만 존재) → 스펙 세션 전달 |
      | **P1** 1-4 | SCR-AUTH-03 홈·대시보드 — 비-PHI 요약 6종(디바이스 상태별·fleet 온라인·승인 대기·연동 대상·매트릭스 상태·최근 감사)+드릴다운 | 🔥 이번주 | **#12666**(머지 `14f5c47`) · 367 unit+component·e2e 26·커버리지 92.6/87.7/93.0/94.4 · **계약에 집계 엔드포인트가 하나도 없다**(전 리소스 커서 페이지네이션·`total` 없음) → 한 페이지를 세고 **더 있으면 `100+`로 드러냄**(200건인데 100으로 보이면 다 처리한 줄 안다) · fleet은 비율이라 더 위험 → **표본 크기 병기** · `targets`만 맨 배열이라 정확한 총계 · 카드별 독립 로드/실패(부분 표시·재시도) · 무권한 카드는 비렌더 · MSW 목 4종 확장(P2~P6 재사용) |
      | **P1** 1-6 | SCR-RBAC-01 권한 요청 — 역할 체크박스 멀티선택+사유·최소 1개 검증·409 중복 분리 · `no_access` 분기를 안내→요청 화면 이동으로 교체 | 🔥 이번주 | **#12667**(머지 `44a689d`) · 382 unit+component·e2e 31·a11y 4(폼 라벨 연결) · **라우트를 `(shell)` 밖에 배치** — 주 사용자가 no_access인데 셸 안이면 BootstrapGate가 막아 **정작 권한을 요청할 방법이 없어진다** · 보유·대기 역할은 체크박스 잠금(409 예방) · 스코프 global 고정(FR-CON-04/07·최종 역할은 Admin 확정) · ⚠ 거부 사유 표시는 계약상 필드 불명확으로 1-7에서 확인 후 부착 |
      | **P1** 1-7 | SCR-RBAC-02 승인 큐·조정 — requested 큐 오래된순·**역할 단위 부분 승인**·거부 사유 인라인 · 화면 단위 권한 게이팅(`RequireCan`) | 🔥 이번주 | **#12668**(머지 `b993fa7`) · 405 unit+component·e2e 35·a11y 5 · **행=운영자가 아니라 요청 역할 1건**(운영자로 묶으면 부분 승인 표현 불가) · 1-6 보류였던 **거부 사유 표시 해소**(`note`가 요청/결정 겸용이고 `decidedAt`이 유일한 구분 신호) · **목 인프라 결함 선제 수정**: `mockPath`가 OpenAPI `{param}`을 MSW `:param`으로 안 바꿔 매처가 조용히 미적용 — P2 이후 단건 경로 전부가 겪을 자리 |
      | **P1** 1-8 | SCR-RBAC-03 운영자 목록 — 상태·역할 필터 + **커서 페이지네이션**(P0 어댑터 실화면 첫 검증) | 🔥 이번주 | **#12670** · 434 unit+component·e2e 40·a11y 6 · 페이지 번호 대신 **더 보기**(계약에 총계·페이지 번호 없음) · 빈 필터 미전송(빈 문자열=정확일치 0건) · 실효 역할만 표시 · **목 결함 수정**: `page()`가 커서를 소비하지 않아 더 보기가 같은 25건을 재첨부(오류 없이 목록만 길어져 미노출) — T-FE-0-7 리뷰가 어댑터에서 잡았던 유형이 목 쪽에 재발 |
      | **P1** 1-9 **risk:auth** | SCR-RBAC-04 운영자 상세·역할 관리 — 역할 직접 부여/회수·정지/복구 + **시스템 마지막 admin 회수 방지 가드** | 🔥 이번주 | **#12671**(머지 `a923f1e`) · **P1 완료(9/9)** · 445 unit+component·e2e 46·a11y 7 · 가드는 "내 admin을 뺏는가"가 아니라 **"시스템에 admin이 남는가"**(SRS §7.2) — `limit=2`로 마지막 여부만 확인(계약에 total 없음) · **UI 가드는 편의일 뿐이라 2층**(버튼 비활성 + 409를 다른 문구로 안내·최종 강제는 서버) · ⚠ **정적 export가 동적 라우트를 못 만듦**(`generateStaticParams` 요구) → `operators/detail?id=`로 전환, 같은 제약이 2-2·3-2·4-3·5-2에도 있어 IP outputs[] 일괄 교정 |
      | **개발환경** 로컬 실 GW 연동 | Console이 Entra 없이 **로컬 GW admin API 실데이터**를 조회하는 경로 개통 — 로컬 OIDC 발급자(`pnpm dev:oidc`)+`NEXT_PUBLIC_GW_LIVE` 스위치 | 🔥 이번주 | **#12674·#12677** · **실측**: 토큰 미첨부 401/첨부 200 · admin 시드 후 대시보드가 실 GW **6개 호출 전부 200**(카드 수치 0 = 빈 DB를 실제로 읽은 증거) · 부모 레포 무수정(그쪽 구현 진행 중) · **번들 유출을 게이트가 적발**(모듈 경계 함수 호출은 안 접힘 — T-FE-0-4·0-10에 이은 3번째) → 리터럴 인라인으로 해소 · ⚠ **GW e2e가 로컬 DB를 truncate해 개발 시드가 소실**됨 → 부모 백로그 **B-13** 등록 |
      | **P2** 2-1 | SCR-DEV-01 디바이스 목록 — `status`·`clinicId` 필터 + 커서 페이지네이션 · clinic **요약 임베드**(2차 조회 없음) | 🔥 이번주 | **#12680**(머지 `f2372d5`) · 487 unit+component·e2e 54·a11y 8·커버리지 91.3/87.8/89.8/92.6 · **region은 컬럼이 아니다**(배포 상수 → 단일 리전 안에서 전 행 동일 · 상단 App Bar가 1회 표시·FR-CON-09 규정) · **상태 필터는 계약 enum 5개 그대로**(줄이면 종단 상태 `rejected`·`revoked` 디바이스를 찾을 방법이 없어짐) · clinic-less는 "미배정"으로 **명시**(빈칸이면 데이터 누락과 구분 불가) · 클리닉 필터는 **제출 시 적용**(불투명 id라 타이핑마다 요청하면 대부분 0건 조회) · URL `?clinicId=` 씨앗 수용(P3 드릴스루 대비) · ⚠ **부수 결함 자체 적발**: 로컬 실 GW용 `.env.local`의 `GW_LIVE=true`가 Playwright dev 서버로 새어 MSW를 끄고 **e2e 전 스펙이 실 GW로 나가 붕괴**(46건 중 2건만 통과) — CI엔 `.env.local`이 없어 **CI 초록·로컬만 실패**하는 유형 → `webServer.env`에서 명시 차단 |
      | **P2** 2-2 | SCR-DEV-02 디바이스 상세 — FR-CON-09 3탭(상태·수명주기 / 인증·키 / 소속 clinic) 조회 전용 | 🔥 이번주 | **#12682**(머지 `7ecbf96`) · 505 unit+component·e2e 63·a11y 9·커버리지 91.1/87.7/89.3/92.4 · **상태의 의미를 함께 표기** — 값만 보면 `rejected`(한 번도 활성화된 적 없는 enroll 거부)와 `revoked`(운영 중이던 것 폐기)가 구분 안 됨·취할 행동이 다름 → `Record<DeviceStatus,…>`로 두어 계약에 상태가 늘면 **컴파일이 깨지게** 함 · **client id·공개키는 비가림**(계약 "비밀 아님" 명시 · 가리면 GW 로그 `client_id` 대조 불가 = 진단 차단) · 미발급은 빈칸 아닌 "미발급+이유" · clinic은 **읽기전용 임베드**(2차 조회 없음·테스트가 호출 횟수 검증) · **클리닉 링크는 미배선**(클리닉 화면 부재 → 정적 배포 404 = "링크 깨짐"과 구분 불가·드릴스루=3-4) · **탭=shadcn/radix 도입**(기존 의존성·신규 0 — 직접 구현 시 화살표 키 이동이 조용히 누락되는데 axe가 못 잡음·P3/P4 재사용) · ⚠ **대조 실행에서 자체 테스트 결함 적발**: 시각 비교가 라벨을 포함해 바꿔치기해도 통과 → 값만 비교로 교정·재대조 확인 |
      | **P2** 2-3 ★개통 게이트 | SCR-DEV-03 enrollment 승인 큐 — 승인=`PATCH status=active` / 거부=`status=rejected`+`reason` | 🔥 이번주 | **#12683**(머지 `455f01e`) · 530 unit+component·e2e 72·a11y 10·커버리지 91.2/87.2/89.9/92.4 · **승인 전 확인을 명시적으로 수령** — FR-CON-10 검증(설치+리전 적정성)은 눈으로 하는 일이라 코드가 대신 못 함 · 바로 누르게 두면 큐를 훑으며 연달아 승인해 **검증 단계가 사실상 소멸** · 확인은 **행 단위**(큐 전체 1개면 한 번 체크 후 나머지 통과) · **거부 사유 UI 필수 강제**(부모 API는 optional이나 거부=종단·복구 불가 → SRS가 UI를 더 엄격히 규정) · **승인엔 사유 미첨부**(빈 문자열이면 감사 로그에서 "사유 없이 결정"과 구분 불가) · **현재 리전+담당 국가 표시**(디바이스 응답에 region 컬럼 자체가 없음=배포 상수 → Region Directory `countries`) · **멱등**(낡은 행엔 버튼 대신 현재 상태) · 화면은 **결정 권한**(cs·admin)으로 개방 · ⚠ **누락 자체 적발**: 착지 경로 목록에 `/devices`(2-1 누락)·`/devices/pending` 미등록 → **cs·developer가 홈에 착지**하던 것 교정 · ⚠ **e2e가 실제 결함 적발**: 리전 요약이 모듈 저장소를 렌더 1회만 읽어 Directory 지연 시 안내 미표시(컴포넌트 테스트로는 원리상 불가) → 훅 구독으로 교정 |
      | **P2** 2-4 | 수명주기 suspend/resume — 상세 [상태·수명주기] 탭의 `active ↔ suspended` + 확인창 | 🔥 이번주 | **#12685**(머지 `a00faab`) · 551 unit+component·e2e 79·a11y 10·커버리지 91.3/87.5/89.8/92.5 · **확인창이 결과를 행동으로 기술**("상태를 suspended로"는 상태명 전사일 뿐 결과 미전달 · 대상 deviceId 병기 = 오선택 감지) · **갈 곳 없으면 액션 미배치**(pending=enrollment 소관·권한 상이 / rejected·revoked=종단) — 비활성 버튼은 "무권한"과 "상태상 불가"를 구분 못 함 · **사유는 선택**(SRS의 UI 강제는 거부·kill 둘뿐 = **모두 비가역**인데 정지는 복구 가능 · 빈 값/공백 미전송) · **실패 시 확인창 유지**(Radix 기본=즉시 닫기 → 오류 표시 위치 소멸 = "적용된 줄" 오인) · **AlertDialog=shadcn/radix 도입**(의존성 0 · 포커스 트랩·Esc·aria-modal은 axe 미검출 · 2-5 kill 재사용) · 목에 §7.2.3 **전이표** 추가 · ⚠ **기존 테스트 경합 적발**: 역할별 착지 e2e 3건이 리다이렉트 **전** URL에 즉시 일치해 통과(2-3에서 경로를 채웠는데도 초록이던 이유) → `waitForURL`로 교정 |
      | ─ **대기·잔여** ─ |  |  |  |
      | **P2** enrollment·디바이스 | 잔여 2-5(kill=revoke · **비가역 파괴적 액션**) | ◑ 진행 **4/5** | 2-1(#12680)·2-2(#12682)·**2-3 ★개통 게이트**(#12683)·2-4(#12685) · 2-5는 `POST …/kill`(PATCH 아님)·사유 UI 필수·위험색 분리·**`[manual]` 사람 클릭 검증 필요**(비가역·재서비스=재-enroll뿐) |
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
