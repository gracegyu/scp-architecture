# VT API Gateway — 8/27 주간회의 Agenda

- **이번 주 진행 (~8/27 회의) — 이번 주 완료·진행한 실제 작업**

  - **진행률(구현 스냅샷)**
    - **GW 백엔드 ≈ 90%** — v1.0 계획 기능 feature-complete(8/24) · 잔여 = ③-I 실 인프라 게이트 · 개발 통합검증 · 계약 경화
    - **GW Console ≈ 85%** — P0~P7 완료 · P8 외부 선결 · 실 dev GW 정합성 확인 진행(확인 끝나기 전까지 완료로 세지 않음)

  - **완료 · 주요 작업**
    - **[config 재정립]** 중앙 설정 = device/clinic-facing 전용 재정립
      - 내부 운영값(로그레벨·프록시 타임아웃·heartbeat 기본주기·offline 배수)을 설정 테이블이 아니라 **환경변수로 분리**(SRS §6.8.1 신설)
      - 예전 "허용 값만 노출(allowlist)·노출 배지" 개념 폐지 · v1.0 실사용 설정 키 = heartbeat 주기 하나 · 디바이스 pull(자기 실효 설정 조회) v1.0 개방
      - 스펙 PR 2건 머지·태그(`spec-v1.0.61`·Console `spec-v1.0.5`) · **구현 완료(GW #13005·Console #13004 머지)**
    - **[OpenAPI code-first]** API 명세 자동 생성·서빙 일원화
      - 구현 코드가 명세 정본(문서-구현 drift 원천 차단) · **CI 드리프트 게이트**로 어긋나면 빌드 실패
      - 문서 서빙 앱 3개(core·admin·receiver)가 각자 포트에서 `/api-docs`(UI)+raw(`/api-docs/yaml`·`/json`) 서빙 · dispatcher(:3003)는 HTTP API 없어 없음 · admin 문서 = Console codegen 소스
      - **로컬 서빙 URL**:

        | 앱 (계약) | 문서 UI | raw 파일 |
        | --- | --- | --- |
        | core (device·public) | `http://localhost:3000/api-docs` | `/api-docs/yaml` · `/json` |
        | admin (운영자) | `http://localhost:3001/api-docs` | `/api-docs/yaml` · `/json` |
        | receiver (webhook 수신) | `http://localhost:3002/api-docs` | `/api-docs/yaml` · `/json` |

      - **dev 한정 서빙** — 로컬(개발) 3앱 자동 on · 배포는 `NODE_ENV=production`이라 앱별 스위치(`GW_{ADMIN,CORE,RECEIVER}_OPENAPI_ENABLED`)로만 켜지며 **현재 dev/test는 admin만 on · sandbox·prod는 off**(계약 구조 노출 방지). 배포 dev admin 문서 = `https://admin.apne2.gw.dev.ezcld.net/api-docs`(admin 부팅 후)
      - core·receiver·admin·target 전반 code-first 전환(구현 대부분 완료)
    - **[region-silo 잔재 정리]** 리전 완전분리(각 배포=한 리전) 전환의 잔재 제거 — 중앙 설정 스코프·감사 action·운영자 관리대상에서 "리전" 제거
      - **중앙 설정(config)**: 예전엔 리전별로 두고 동기화하려 했으나, 리전 스코프 제거로 **리전 간 config 동기화 자체가 불필요**해졌다(전역/클리닉/디바이스로 통일)
      - 정당한 리전 사용처(배포 상수·호스트 라벨·데이터 주권·운영자 역할)는 유지 · 스펙 정리 완료·코드 반영 진행
    - **[환경 4-tier + OpenAPI 스위치]** `env-reference.md` 4열(dev·test·sandbox·prod) 정리·Jack에 값 채움 요청
      - dev 실측: core·receiver·dispatcher 기동 · admin=Entra 대기
    - **[데이터 규모 대응]** 대량 데이터를 감당하는 관리 UI로 보강 — **구현 완료**
      - **문제**: clinic·device·webhook 등 데이터가 **최대 몇 개까지 늘지 스펙에 정의가 없어**, 목록 스크롤·전량 드롭다운 위주의 UI로는 대량(clinic 10만·device 10만·**webhook 1억**·audit 100만 규모)을 효과적으로 관리할 수 없었다.
      - **대응**: 먼저 **최대 규모를 스펙·계약에 명시**(spec-v1.0.42~46)하고, 그 규모를 감당하도록 **검색형 선택기**(이름 부분검색·id 겸용)·**필터**(기간·상태·리소스 축)·**서버 집계 카드**(표본 카운트 대신 집계 EP)·**커서 페이지네이션 한계 표시**·**보존경계 안내**를 UI에 넣었다.
      - GW(인덱스 마이그레이션·이름검색 `q`·webhook 기간 커서 window·집계 EP 3종·수동 create) + Console(검색형 선택기·집계 카드·목록 규모 표시) 양쪽 구현 완료.
    - **[부하/HA 테스트 계획]** `docs/qa/load-ha-test-plan.md` 초안 작성(테스트 대상·k6·시나리오·주입·부하 EC2·FIS 절차)
      - 인프라 확정분(사이징·FIS·RTO/RPO)=Jack · test 인프라 구축 후
    - **[운영자 표시 개선]** 감사·"최근 변경 이력"·RBAC 화면에서 운영자를 **ID 대신 `이름 <이메일>`로 표시**
      - 운영자 참조 응답에 표시 요약 임베드(`AuditLog.actorSummary`·`RoleGrant.decidedByOperator`·읽기전용·operator id/subject 키는 불변) — clinic 요약 임베드 패턴(#47) 재사용
      - device·clinic·target·operator 등 **모든 최근-변경 이력이 동일 AuditLog를 읽어 한 필드로 커버** · 스펙 PR GW #13009(spec-v1.0.62)·Console #13010(spec-v1.0.6) **둘 다 머지** · **GW(조인으로 값 채움)+Console(렌더) 양쪽 구현 착수**

    - **[작업 결과 알림(Toast)]** 저장·승인·삭제 결과가 화면에 뜨지 않던 문제 — **구현 진행 중**
      - **문제**: 운영자가 버튼을 눌러도 **됐는지 안 됐는지 알 수 없었다.** 실측하니 변경 동작 27곳 중 결과를 알리는 표시는 **7곳뿐**이고, 나머지는 목록이 새로 고쳐지는 것으로 **짐작해야** 했다. 실패는 더 나빴다 — 알림을 받는 배선이 아예 없어 **오류가 조용히 사라졌다.**
      - **대응**: 앱 전역 **Toast**(화면 하단에 잠깐 떴다 사라지는 알림·"스낵바"라고도 부름) 도입 + 알림 수신부를 **한 곳에** 배선. 화면마다 문구를 넣지 않아도 **모든 변경 동작이 결과를 말한다.**
      - **경계(중요)**: Toast 는 사라지므로 **모든 것을 옮기지 않는다** — ① 조치가 필요한 오류(권한 요청·재시도 안내)는 화면에 그대로 남기고(4초 뒤 사라지는 자리에 "권한을 요청하세요"를 둘 수 없다) ② **긴급 정지 같은 파괴적 동작의 실행 기록**(실행자·시각·감사 기록됨)도 화면에 남긴다. Toast 는 **더하는 쪽**이다.
      - **용어**: 코드·라이브러리가 모두 `toast` 라 문서도 **Toast 로 통일**한다(Snackbar 는 Material Design 용어).
      - **범위**: **Console 단독** — 계약·GW 영향 0건. SRS 미규정 항목이라 PL 제안으로 착수했고 IP 에 Task 등재.

  - **진행 중 · 선결 대기**
    - **[GW dev 배포·통합]** core·receiver·dispatcher dev 기동 확인 · admin=Entra 등록 후 통합 착수(③-I #3)
    - **[GW Console 통합]** 실 dev GW + Entra 접목 · 완료 화면 포함 정합성 확인 마무리
    - **[Entra 앱 등록]** dev admin+Console 2앱 — **[IT-9442](https://vts.vatech.com/projects/IT/issues/IT-9442)**(Jack 입력·절차/회신 양식 제공 완료) · **admin 부팅 선결**(③-I #3·#4)
    - **[제품 연동 스펙]** EzServer OnePager 수령 확인(잔여)

  - _(이번 주 결정사항 = 회의 시 추가)_

- 논의 사항 (이번 주 · 신규 · R#)
  - _(회의 중 신규 논의/결정 안건 발생 시 **R1·R2…** 로 추가 · 선결·보류는 아래 「이월 논의 사항」 표.)_

- **[③-I Jack 인프라 요청 추적]** — 회의에서 상태·ETA 확인. (PR: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/12653)

  | # | 요청 | 수신 | dev | prod |
  | --- | --- | --- | --- | --- |
  | 1 | Region Directory 호스팅 | ③-I | ✅ publish(8/18·`regions.gw.dev.ezcld.net`) | ☐ 도메인 후 |
  | 2 | GW Console dev 호스팅(`console.gw.dev.ezcld.net`) | ③-I | ✅ 개통(8/19·CD 파이프라인·딥링크 rewrite) | ☐ 도메인 후 |
  | 3 | **dev GW 백엔드 배포·env 주입**(`DATABASE_URL`[공용 `common-dev-db`·`gw` DB·apne2]·`REDIS_URL`·`GW_REGION`=apne2·AWS **Pod Identity**·`NODE_ENV` 차트 주입) | ③-I | 🟠 core·receiver·dispatcher **✅ 기동** · admin=Entra 대기 | ☐ |
  | 4 | **운영자 Entra 앱 등록**(GW Admin API + Console SPA·2앱·PKCE) | IT·③-I | 🟠 **진행중 · [IT-9442](https://vts.vatech.com/projects/IT/issues/IT-9442)**(Jack 입력·절차·회신 양식 제공 완료)·마감 8/21 경과·**admin 부팅 선결** | ☐ 도메인 후 |
  | 5 | **env-reference 환경별 값 채움**(test·sandbox·prod endpoint·호스트·리전) | ③-I | ✅ dev · ☐ test/sandbox/prod | ☐ |
  | 6 | **dev-seed grant**(`gw-dev-seed` 변수그룹·KMS·Environment 승인게이트) | ③-I | ☐ 요청 전달(8/20) | — |
  | 7 | **`pg_trgm` CREATE EXTENSION 권한**(clinic 검색 선결 · env-reference §2.1) | ③-I | ✅ 문제 없음(Jack 확인 8/20 — `gw_app`=`gw` DB OWNER·trusted extension) | ☐ prod 동일 확인 |
  | 8 | **KMS CMK provisioning**(webhook payload·target 자격 alias·리전별 · 8/4 키 토폴로지 · env-reference §2.4) | ③-I | ☐ (webhook/target 실사용 시) | ☐ 리전별 |
  | 9 | **admin API dev ingress 노출**(`admin.apne2.gw.dev.ezcld.net`·Entra-gated 공개 ingress) — Console이 실 dev DB 데이터를 조회하려면 admin 부팅에 더해 이 ingress가 있어야 함(없으면 admin이 떠도 Console이 못 부름) | ③-I | ✅ **ingress 구축 확인**(8/25 curl: 443 OPEN·ALB 응답) — 단 전 경로 **503(ALB에 healthy target 0·즉시응답)** = **admin 미기동**이 원인(ingress 문제 아님)·**#4 Entra→admin 부팅 시 해소** | ☐ 도메인 후 |

- **[GW 구현 선결 추적 · 외부 인프라·자격]** — E2E·배포가 외부 선결로 막힌 항목. 소유별 상태·ETA 확인.

  | # | 선결 항목 | 소유 | dev | prod |
  | --- | --- | --- | --- | --- |
  | 1 | 공개 ingress(AXS→GW webhook 수신) | ③-I | ☐ | ☐ |
  | 2 | 실 IoT Core(MQTT 다운링크·Thing/policy·IRSA·`MQTT_URL`) | ③-I | ☐ | ☐ |
  | 3 | 자동배포 파이프라인(main→DEV·tag→TEST/PROD) | ③-I | 🟠 dev 배포 됨(3앱) · 자동화·tag→TEST/PROD 잔여(Jack Azure Flow 템플릿→ECR/ArgoCD) | ☐ |
  | 4 | Parameter Store write IAM + ESO + AWS 커넥션(compat publish 포함) | ③-I | ☐ | ☐ |
  | 5 | **test 환경 프로비저닝**(별도 인프라·GW=infra 분류·상시 최소 baseline+임시 확장·부하/HA 사이즈업 포함) | ③-I | ☐ **요청 완료·마감 8/26** | ☐ |
  | 6 | AXS 자격 | Straumann·영업 | ✅ sandbox(8/11) | ☐ prod(NDA후) |
  | 7 | 파일 붙은 lab order 시드 | Straumann·④ | ☐ (sandbox) | — |
  | 8 | **마이그레이션 배포 Job 배선**(K8s Job + ArgoCD PreSync hook · migrate 이미지 ECR push[앱과 같은 SHA] · 매 배포 前 1회 `migrate deploy`·성공 gating·fail-closed) | ③-I | 🟠 **GW 몫 완료**(#12926 · migrate 이미지 타겟·실행명령·env·local `make dev-up` 자동) · ③-I K8s Job+PreSync 배선 대기 | ☐ |

  _(`—`=해당 없음.)_

- 공유 사항 (결정 아님 · 논의사항인지 애매한 것을 임의 결정해 공유 · 매주 상시)

  - **webhook payload 보존·아카이브 방식(gw/1.1)** — 무한 누적되는 webhook payload(PHI·KMS 암호문) 관리 방식을 임의로 결정해 공유: **리전 로컬 S3 아카이브 후 삭제**(파티셔닝 미채택)·무인 K8s CronJob(시간 기준)·export→검증→배치삭제·잡 단위 감사·tombstone 없음. SRS §7.6.9에 설계 골격+다이어그램 반영(gw/1.1·v1.0=저볼륨 미구현·알람만). 확정 필요 값(리전별 ① DB 잔존 기간 ② S3 보관 기간·+가동 임계값)은 법무 의존이라 **이월 논의 #15**에서 추적(Appendix B #5·#36).

  - **S1. 프로젝트 일정(Gantt) — 8/27 스냅샷**
    - **진행률(구현)**: **GW ≈ 90%**(v1.0 계획 기능 구현 완결·8/24 feature-complete · 잔여=③-I 실 인프라 게이트·개발 통합검증·계약 경화[OpenAPI 코드-first 일원화]) · **GW Console ≈ 85%**(P0~P7 완료·P8 외부 선결·실 GW 정합성 확인 진행 — 확인 끝나기 전까지 완료로 세지 않음)
    - **목표 = 10월 출시**(역산·잠정 — 잔여 변수 = prod 자격[NDA후]·부하/HA 환경)
    - **범례** — 막대: 작성=기본·PR=강조·◆=baseline/마일스톤·**빨강=외부/미정 선결** / 선결(빨강): AXS **prod** 자격(NDA 후·Straumann)

    ```mermaid
    gantt
        title v1.0 = Straumann(AXS) 첫 외부연동 — 10월 출시 목표(역산·잠정)
        dateFormat YYYY-MM-DD
        axisFormat %m/%d
        todayMarker stroke-width:3px,stroke:#d33,opacity:0.6

        section ③ GW SRS + API/DBML (계약 SSOT · baseline v1.0 동결)
        작성 (본문+OpenAPI·DBML)       :done, srsw, 2026-06-15, 28d
        PR 리뷰·수정                  :done, srspr, 2026-07-13, 2026-07-20
        baseline v1.0 (7/20 확정)      :milestone, done, srsbl, 2026-07-20, 0d

        section GW 구현 → E2E → 출시 (구현 feature-complete · 잔여=③-I 실인프라 게이트)
        1단계 GW 독립 코어 (P0~P6·P10·완료) :done, implindep, 2026-07-21, 31d
        2단계 AXS 연동 (P7~P12·AXS 실연동·부하/HA 하네스·코드 완료) :done, implaxs, 2026-07-28, 2026-08-24
        GW 구현 완료 (코드 feature-complete) :milestone, impldone, 2026-08-24, 0d
        AXS E2E·통합 (sandbox 커버·실 인바운드/IoT=③-I 대기) :e2e, 2026-08-24, 2026-09-30
        개발환경 연동 완료(9월·R2)      :milestone, dev9, 2026-09-30, 0d
        v1.0 production 연동 완료(10월·R2·재검토) :milestone, rel, 2026-10-31, 0d

        section ③-I 인프라 IaC (계획서 병합=완료·living doc · AWS 4종 dev·test·sandbox·prod)
        ① 초안+PR (Raymond)            :done, infw, 2026-07-20, 2d
        ② Jack 상세·리뷰·수정 (PR #11973 병합 7/27) :done, infpr, 2026-07-21, 6d
        ③ 계획서 PR 병합 완료          :milestone, infbl, 2026-07-27, 0d
        Infra 구축·자동배포 완료(8월·R2) :milestone, infra8, 2026-08-31, 0d

        section ③-P-EZ EzServer 연동 스펙 (① 초안=Raymond → ② Teddy 상세 → ③ baseline)
        ① 초안+PR (Raymond)            :done, ezw, 2026-07-20, 5d
        ② Teddy 상세·리뷰·수정         :active, ezpr, after ezw, 63d
        ③ baseline                     :milestone, ezbl, after ezpr, 0d

        section ③-P-CS CleverSpace OnePager (① Raymond → ② Larry 상세 → ③ baseline)
        ① 초안+PR (Raymond·#12239)     :done, cssub, 2026-07-27, 5d
        ② CleverSpace팀(Larry) 상세    :active, cspr, after cssub, 56d
        ③ baseline                     :milestone, csbl, after cspr, 0d

        section ③-P-CO CleverOne OnePager (① Raymond → ② Nick 상세 → ③ baseline)
        ① 초안+인계 (Raymond·SharePoint) :done, cosub, 2026-07-27, 5d
        ② CleverOne팀(Nick) 상세       :active, copr, after cosub, 56d
        ③ baseline                     :milestone, cobl, after copr, 0d

        section ④ AXS 연동 프로파일 (경량 스펙·구현=GW 2단계 P7)
        AXS PPR sandbox 자격 확보(8/11) :done, cred, 2026-08-11, 1d
        연동 프로파일 정리             :axsw, after cred, 14d
        프로파일 확정                  :milestone, axsbl, after axsw, 0d
        AXS prod 자격(NDA 후·선결)     :crit, credp, 2026-08-18, 21d

        section ③-C GW Console — v1.0 (frontend·별도 repo·P0~P7 완료·P8=외부 선결)
        SRS 작성 (8/5)                 :done, consrsw, 2026-08-05, 6d
        v1.0 구현 (mock-first)         :done, conv1, 2026-08-12, 2026-08-24
        v1.0 구현 완료                 :milestone, conv1m, 2026-08-24, 0d
        GW 통합테스트 (실 dev GW·Entra·8월말까지) :active, contest, 2026-08-24, 2026-08-31
        통합테스트 완료                :milestone, contestm, 2026-08-31, 0d

        section v1.0 이후 (deferred · post-v1.0)
        CleverOne 연동 구현 (스펙은 지금·구현 post-v1.0) :codef, after rel, 14d
    ```

  - **S2. 스펙 작성 테이블 — 제품 × 단계 · 매주 스냅샷** · **정본 = 본 Agenda(S2)**
    - 각 셀 앞 이모지 = 스펙 작성 진행: ✅ baseline · 🟢 PR · 🟡 작성중 · ⬜ 미작성 (— = 해당 없음)

      | 제품 | 1단계(호환성) | 2단계(presigned) | 3단계(GW 일원화) | 4단계(멀티리전) | 5단계(Straumann) | 스펙 산출물 |
      | --- | --- | --- | --- | --- | --- | --- |
      | **CleverSpace** | 🟡 버전체크·well-known·오류코드 | 🟡 presigned 발급 API | 🟡 GW 경유 수신 | ⬜ 멀티 Region | — | 🟢 ③-P-CS OnePager 인계(#12239·Larry 검토) |
      | **CleverOne** | 🟡 Vatech-* 헤더·fallback | 🟡 presigned 이용 | 🟡 Direct→GW 경유 | ⬜ Region 선택·ClinicID | — | 🟢 ③-P-CO OnePager 인계(SharePoint·Nick 검토) |
      | **EzServer(EZ)** | 🟡 헤더 대리 전달 | 🟡 전송 로직(presigned) | 🟡 GW 경유 전환 | 🟡 ClinicID·Region·등록 | 🟡 AXS(갈래A)·presigned 직접 | 🟡 ③-P-EZ OnePager 초안(Raymond→Teddy) |
      | **CleverLab** | — | — | — | — | ⬜ AXS 오더·확정(갈래B) | ④ Sub-SRS(갈래B·보류) |
      | **VatechAPIGateway** | 🟢 호환 게이트(§7.7) | 🟢 presigned 중계(§4.1.4) | 🟢 본체·라우팅·인증·호환 | 🟢 리전 라벨·Region Directory·HA | ⬜ AXS OAuth·Org-ID·온보딩·고정IP | ③ SRS ✅ baseline · **현행 `spec-v1.0.41`** |
      | **GW Console**(③-C) | — | — | — | 🟢 Admin Web Console(Entra 앱계층) | ⬜ 온보딩·Org-ID 후속(gw/1.1·1.2) | ✅ ③-C Sub-SRS baseline(`spec-v1.0`) → S4 |
      | **인프라** | — | — | 🟢 **dev·test·sandbox·prod(4종)** | 🟢 Route53·K8s | 🟢 AXS 고정IP·샌드박스 | 🟢 ③-I IaC 계획서(PR #11973·living doc) + KMS 키 토폴로지 |
      | **외부(Straumann AXS)** | — | — | — | — | 🟡 PPR sandbox=확보(8/11) · ⬜ prod=NDA 후 | ④ 입력(외부 제공) |

    - **스펙 문서 등록처·baseline (SSOT)**

      | 단위 | 스펙 문서 | Repo · 경로 | baseline tag |
      | --- | --- | --- | --- |
      | **③ GW** | SRS(+OpenAPI·DBML·UnitTCL) | `vt-api-gateway` · `docs/specs/` | **`spec-v1.0.41`**(현행 동결) |
      | **③-C GW Console** | Sub-SRS | `vt-api-gateway-console` · `docs/specs/SRS.md` | ✅ `spec-v1.0`(8/11) |
      | **④ AXS** | 경량 연동 프로파일 | `vt-api-gateway` · `docs/specs/04-subsrs-straumann-axs/` | 경량(PPR 자격 확보·착수 가능) |
      | **③-I 인프라** | IaC 구축계획서 | `vt-api-gateway-infra` · `docs/IaC-구축계획서.md` | PR #11973(living doc) |
      | **③-P-EZ EzServer** | GW적응 OnePager | `ezserver_suite`(`v6.5.x`) · `doc/onepager/gw_adaptation/` | 미부여(팀 baseline 예정) |
      | **③-P-CS CleverSpace** | GW적응 OnePager | `ezicloud/ezcloud` · `docs/onepager/gw_adaptation/` | PR #12239(팀 baseline 예정) |
      | **③-P-CO CleverOne** | GW적응 OnePager | SharePoint `gw_adaptation` | — (팀 baseline) |

  - **S3. GW 백엔드(③) 현황 — Phase 요약 (8/27)** _(NestJS 코어·부모 SRS · Console은 S4)_

    | Phase | 범위 | 상태 |
    | --- | --- | --- |
    | **P0~P6·P10** 1단계 코어 | 스캐폴드·데이터모델·인증(JWKS)·enrollment·region·호환게이트·프록시·fleet/config | ✅ 완료 |
    | **P7** External Connector·AXS | 아웃바운드 OAuth2·egress fail-closed·AXS 실연동·커넥터 전략·presigned 중계 | ✅ 완료 |
    | **P8~P11** 2단계 | webhook 수신·Dispatcher/분배·Admin CRUD(RBAC·break-glass·audit) | ✅ 완료 |
    | **P12** E2E·하드닝 | 12-1 아웃바운드·12-2 compat·12-5 presign·12-7 업로드위임·12-8 다운로드·12-9 webhook라우팅 | ✅ 완료분 · ◑ 진행 |
    | **P12** 잔여 | 12-6 인바운드+MQTT(③-I ingress+실 IoT) · 12-3 부하 실측(하네스 완료·③-I test) · 12-4 HA(③-I Multi-AZ) | 🔴 외부 선결 |
    | **P9-5** 실 IoT 프로비저닝 | (a) 코드 완료(어댑터·mock) · (b) 실 IoT Core mTLS 실증 | ◑ (a)완료·(b)③-I |
    | **P0-5** 자동배포(CD) | ECR/ArgoCD·main→DEV·tag→TEST/PROD | 🔴 ③-I |

    - 커버리지(merged·8/20): 전역 96.7 / 91.9 / 93.9 / 96.5 · 보안 도메인 98.5 / 96.0 / 100 / 98.4 · 핵심 보안파일 16개 각 100% — **CI floor 게이트 통과**.

  - **S4. GW Console(③-C) 현황 — Phase 요약 (8/27)** _(frontend · `vt-api-gateway-console` · Next 16 + Refine 5 + shadcn · GW Admin API 코드젠 소비)_

    | Phase | 범위 | 상태 |
    | --- | --- | --- |
    | **Console SRS** | gw/1.0 완전 규격 | ✅ baseline `spec-v1.0`(8/11) |
    | **P0** 플랫폼 스캐폴드 | Next+Refine+shadcn·코드젠·MSW 목·App Shell·i18n·CI 8게이트 | ✅ 완료 |
    | **P1** 인증·RBAC | Entra OIDC(PKCE)·`/me` 부트스트랩·역할×액션 매트릭스·권한요청/승인·운영자 관리 | ✅ 완료(9/9) |
    | **P2** 디바이스 | 목록·상세·enrollment 승인·suspend/resume·kill | ✅ 완료(5/5) |
    | **P3** 클리닉 | 목록·상세·memo·드릴스루 | ✅ 완료(4/4) |
    | **P4** 연동 대상 | 목록·폼(자격 마스킹)·정책·org-mapping | ✅ 완료(4/4) |
    | **P5** webhook·break-glass | 이벤트 메타·DLQ triage·payload 열람(PHI) | ✅ 완료(3/3) |
    | **P6** fleet·config·매트릭스·감사 | 대시보드·SW 인벤토리·중앙 config·매트릭스 뷰어·감사(리소스 축) | ✅ 완료 |
    | **P7** 공통 UX·i18n·동시성·보안 | 세션만료·403·오류분류·stale-write·i18n·보안/a11y 게이트 | ✅ 완료(7/7) |
    | **P8** 실 e2e·배포 | Entra dev 전환·staging 실연동·baseline 승인·prod 배포 | 🔴 외부 선결(Entra·staging GW·CORS·도메인) |

    - **GW 정합성 확인 진행 중**(실 GW 접목 전 완료 화면 포함 대조) · **잔여 `[manual]` 검증**(kill·break-glass·보안 실검사 = PL 1회 클릭) · 커버리지(unit+component·8/20): 전역 91.9 / 86.7 / 86.9 / 92.5 · 민감 로직 94.7 / 90.6 / 95.0 / 96.9 — **CI floor 통과**.

- 이월 논의 사항 (계속)

  | # | 항목 | 타입 | 상태 |
  | --- | --- | --- | --- |
  | 4 | Webhook 클라우드 분배(CleverLab 갈래B) | [논의] | v1.0 제외 — Open 후 결정 |
  | 6 | AXS **prod** 자격(Straumann 정식계약) | [정보] | PPR sandbox=확보(8/11) · prod=NDA 후 |
  | 7 | 경로 B EOS 시점 | [논의] | EOS 시점만 PM·CS/CO OnePager 미정 |
  | 8 | v1.0 목표 RPS·동시 세션 | [논의] | **부하 테스트 계획 수립** — 목표치 확정 필요·인프라 후 실측 → 이번 주 진행 [부하/HA] |
  | 9 | RTO/RPO·유지보수 윈도우 | [논의] | **HA 테스트 계획 수립** — 목표치 확정 필요(HA 실측 선결)·R2 연계 → 이번 주 진행 [부하/HA] |
  | 10 | 감사·consent 보존 기간 | [정보] | 법무 확인 대기 |
  | 11 | 호환성 매트릭스 확정본 | [정보] | CleverSpace/CleverOne OnePager 의존 — 담당팀 baseline 후 |
  | 14 | 관측성 앱↔인프라 계약(로그 필드 스키마·메트릭 export 배선) | [논의·설계] | 추후 확정 — 트리거=③-I 관측 스택 구축 · 앱 계약(stdout JSON+OTel·redaction) 이미 구현·무블로킹 |
  | 15 | Webhook payload 보존·아카이브 기간(리전별) | [논의] | **법무 확정 대기** — 리전별 ① DB 잔존 기간 ② S3 보관 기간(+가동 임계값). 설계 골격=SRS §7.6.9(gw/1.1)·Appendix B #5·#36 → 이번 주 공유 [webhook 아카이브] |
