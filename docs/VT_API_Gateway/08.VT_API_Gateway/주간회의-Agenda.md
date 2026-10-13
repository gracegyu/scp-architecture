# VT API Gateway — 10/15 주간회의 Agenda

> ⚠ **10/8 회의는 열리지 않았다(문서로 대체).** 아래 「결정 필요」는 **한 주 더 묵은 안건**이다.

- 🔴 **결정 필요 — 이번 주에는 받아야 하는 것**

  | # | 안건 | 왜 지금 |
  | --- | --- | --- |
  | **1** | **SonarQube 토큰 폐기** | 코드는 고쳤으나 **이미 찍힌 로그 102개가 남아 있다.** 콘솔 작업이라 사람이 해야 한다 |
  | **2** | **SBOM 트리거 구조** | 잡 16개가 제품 코드를 안 본다. **주기 단축으로 안 풀린다** |
  | **3** | **의존성 정기 점검 주기** | 14건 → 0으로 만들었지만 **또 2주 뒤 같은 자리에 선다** |
  | **4** | **RTO/RPO 목표** | HA 합격기준. 환경이 생겨도 이것 없이는 못 끝낸다 |
  | **5** | **10월 출시 목표 유지 여부** | 9/30 「개발환경 연동 완료」를 넘겼고 **원인 둘이 그대로다** |

  - ⚠ **1·2는 보안 사안이고 사람이 손대야 끝난다.** 코드로 할 수 있는 부분은 이미 끝냈다.

- **이번 주(10/15) 진행**

  - ✅ **[제품 연동 스펙] device 면 target 카탈로그 — 계약 신설부터 양쪽 구현까지 닫혔다**
    - 클라이언트가 target 목록과 연동 입력 폼을 하드코딩하지 않고 GW에서 받는다. **새 target이 추가돼도 클라이언트 릴리스가 없다.**
    - GW `spec-v1.0.97` · Console `spec-v1.0.15` · 구현 PR 4건 머지. 운영자가 Console에서 넣은 표시명이 **클리닉 화면까지 그대로 간다**
    - ⭐ **AlliedStar가 두 번째 target으로 들어올 때 클라이언트 릴리스 없이 붙는지를 실제로 검증할 수 있게 됐다** — 지금까지는 문서상 목표였다
    - ⭐ **구현이 스펙 결함 셋을 먼저 잡았다** — 공백 판정 · 길이 판정 시점 · clinic-less 엣지. 앞의 둘은 고쳤고 셋째는 v1.0에서 발생하지 않아 유예(B-25). **셋 다 리뷰 2라운드와 승인을 통과한 문장이었다**
    - ✅ 베이스 도메인 확정값 문서 정합화도 완료 — **test·sandbox·prod Entra 앱 등록이 지금 가능**해졌다

  - ✅ **[보안] 취약점 14건 → 0건** (GW 12 · Console 2 · DT 서버 기준 확인)
    - 전부 **전이 의존**이고 **이미 올려 둔 버전에 새 advisory가 붙은 것**이다 — 우리 코드 문제가 아니다
    - 🛑 **보안 지표만의 문제가 아니었다** — 그 12건이 `audit --audit-level high` 게이트를 막아 **`main`과 전 PR이 적색**이었다. 지표로만 보면 안 보이는 비용이다
    - ⭐ **CRITICAL 둘 다 신뢰 경로에 안 닿았다** — GW `proxy-addr`는 **설계가 이미 막아 뒀고**(인증=HMAC·source IP 비신뢰·`trust proxy` off·rate-limit 키가 `::ffff:` 제거), Console `next/og`는 정적 export라 서버가 없다
    - 🛑 **근본 원인은 「결정 필요」 2·3번이다** — SBOM 잡 16개가 **Jenkinsfile 레포를 폴링**해 제품 코드 변경을 못 본다. 마지막 실행이 10/1이었던 것도 그 때문이고, **지금 사내 SBOM은 담당자의 문서 커밋이 갱신하고 있다**

  - 🟢 **[IoT 다운링크] GW 코드 머지 완료 — 환경값 주입만 남았다**
    - ✅ 실 IoT 배선 + 시드 진입점 머지([#15215](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/15215)) · 시드 파이프라인은 ③-I가 클러스터 안 Job 방식으로 전환([#15212](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/15212)) · **둘 다 CI 녹색**
      - 34파일 · +1066/−390 · **신규 테스트 17건**(단위 15 + **실 DB 통합 2**) · 단위 2165·e2e 674 통과
    - ✅ **dev 새 이미지도 올라갔다** — 그 머지 커밋으로 배포 파이프라인 4종이 돌았다(10/12)
    - 남은 것은 **환경값 3종 주입(③-I) → enroll 1건 → 다운링크 1회** 뿐이다. E2E 하네스는 이미 있다
    - 🛑 **이번에 막은 것이 전부 「조용히」 형태였다 — 셋이 같은 병이다**
      - **엔드포인트 값이 비면 가짜 어댑터로 떨어진다**(IoT·KMS) — 한 달을 잡아먹은 그 원인
      - **더미 자격을 넣으면 Pod Identity를 가로막는다** — 반대 방향이다. 넣지 말아야 할 것을 넣어서
      - **시더가 실패해도 종료 코드가 0이면 Job이 성공으로 잡힌다** — 데이터가 안 들어갔는데 들어간 줄 안다
      - 셋 다 **부팅에서 막고 기동 로그에 남기도록** 고쳤다. 실 어댑터면 로그, 가짜면 **경고**로 올라온다
    - ⚠ **같은 병이 6곳 더 남아 있다** — dispatcher·receiver·admin의 KMS·SQS 모듈에 더미 자격이 그대로다. **그 앱들이 실 AWS를 쓰는 순간 재발**한다
    - ⭐ **목(mock)으로는 못 잡는 결함을 하나 잡았다** — 시더가 **첫 삽입에서 즉사**하는 상태였는데 단위 테스트는 전부 초록이었다. **실 DB 왕복만이 증명하는 부류**라 통합 테스트를 신설했다
    - ⓘ `import` 한 줄이 **이미지에 들어가는 파일 목록을 바꾼다** — 루트 파일을 참조하면 빌드 산출 경로가 생기는데 Dockerfile이 그 경로를 복사하지 않아 Job이 죽는다. 구현 위치를 옮겨 피했다

  - **[인프라] 미결 넷**
    - 🔴 **SonarQube 토큰** — 코드 수정 완료(10/7·5개 지점). ⚠ **근본 수정은 못 했다**(설치된 `sonar-scanner-cli 5.0.1`이 환경변수 방식을 안 받는다). **남은 것은 폐기**(「결정 필요」 1번)
    - ❓ **백업 새 버킷 수명주기·버전 관리 확인(Jack)** — 최소 권한이라 호스트에서 못 읽는다. 옛 계정 정리 시점도 함께
    - **BM2 전체 복구 시연** — 가장 위험한 항목(암호화 키 복호화)은 격리 컨테이너로 검증했다. `restore1→2→3` 전체는 **격리 VM이 필요**하다
    - **`EzServer-SonarQube` 8연속 실패** — 담당 Thomas·진단 전달 완료. 9/16 Rust/Dart를 Windows 에이전트로 옮긴 뒤부터이고, 노드·디스크·메모리·권한·시계·연결은 실측으로 배제했다
    - ⓘ **Rust 파이프라인 네이티브 전환 · 「0파일 분석인데 게이트 통과」 가드**(31개 중 9개)는 **org-wide·Jack 소관**이라 GW 쪽에 검증된 업데이트가 없다
    - **DT config 2건 삭제** [PR #14635](https://dev.azure.com/ewoosoft/sbom/_git/jenkins/pullrequest/14635) — ⚠ **리뷰 3주째**

- **남은 작업 — 전부 외부 선결** (⭐ **GW·Console 코드로 앞당길 잔여 = 0**)

  | # | 남은 작업 | 우리 쪽 상태 | 막는 것 | 소유 |
  | --- | --- | --- | --- | --- |
  | 1 | **Entra admin consent 승인** | ✅ dev 2앱 배선 완료 · admin API 부팅 확인(401) | 🔴 [IT-9442](https://vts.vatech.com/projects/IT/issues/IT-9442) 승인 1건(조직 1회) — **미승인이라 Console 실로그인 불가** | IT·③-I |
  | 2 | **test 환경 프로비저닝** | — | 🔴 요청 완료 · **마감 8/26 · 미착수** | ③-I |
  | 3 | **IoT 다운링크 E2E**(webhook→IoT 1회) | ✅ **코드 머지 + dev 배포 완료** · E2E 하네스 보유 | **환경값 3종 주입만** | ③-I |
  | 4 | 자동배포 tag→TEST/PROD | main→DEV는 **실동작 확인** | #2 (환경 생기면 태그 트리거만 추가) | ③-I |
  | 5 | 부하 실측 · HA 실측 | ✅ 하네스·스크립트·파이프라인 | #2 **+ RTO/RPO 목표 미확정** | ③-I · **PL** |
  | 6 | presign E2E(환자문서 order-file) | ✅ create/download 실측 | 파일 붙은 lab order 시드 | Straumann |
  | 7 | Console 배포 보안 헤더(CSP·HSTS 등) | ✅ 8/26 실측 — **전부 부재** 확인 | CloudFront response headers policy 미배선 | ③-I |
  | 8 | Console prod 배포 | ✅ 프리뷰 배포 파이프라인 | prod 도메인 | PL · ③-I |
  | 9 | dev 재배포·재시드 | ✅ 계약 양쪽 머지 완료 | **dev에 안 떠 있어** 실화면 확인 불가 | ③-I |
  - 🔴 **최우선 블로커 둘 — 회의에서 밀 것**
    - **① Entra admin consent** — 풀리면 dev 통합검증이 통째로 풀린다
    - **② test 환경** — 풀리면 **부하·HA 2건이 동시에 해제**된다(#4·#5)
    - ✅ **IoT 다운링크는 블로커에서 뺀다 — 선결이 해소됐다**(아래 「이번 주 진행」)
  - ❓ **PL 결정 대기 = RTO/RPO 목표**(HA 합격기준) — 환경이 생겨도 이것 없이는 #5를 끝낼 수 없다

- **논의 사항 (이번 주 · 신규 · R#)**
  - _(신규 안건 없음 — 위 「결정 필요」가 이월분이다)_

- **공유 사항** (결정 아님 · 논의사항인지 애매한 것을 임의 결정해 공유 · 매주 상시)

  - 🛑 **[패턴] 「있는 줄 알았던 가드가 사실은 안 걸리고 있었다」 — 이번 주에만 다섯**

    각각은 다른 사람이 다른 맥락에서 찾았는데 **형태가 같다.** 따로 보면 잔고장이고 **모아 보면 구조 문제**다.

    |                           | 있다고 믿은 것              | 실제                                                                |
    | ------------------------- | --------------------------- | ------------------------------------------------------------------- |
    | **SBOM 스캔**             | 매일 돈다                   | 제품 레포를 **안 본다**(Jenkinsfile 레포 폴링) — 6일간 0회          |
    | **SonarQube 토큰 마스킹** | `withSonarQubeEnv`가 가린다 | **평문으로 로그 102개**에 남았다                                    |
    | **SonarQube 분석**        | 31개 프로젝트가 검사된다    | **9개는 0파일 분석인데 게이트 통과**                                |
    | **Console 커버리지**      | 측정된다                    | 잡이 테스트를 안 돌려 **"한 줄도 커버 안 됨"으로 기록**             |
    | **Console CI 워커 상한**  | CI에서 2로 묶인다           | Azure는 `CI`가 아니라 **`TF_BUILD`**를 세팅 — **한 번도 안 걸렸다** |
    - ⭐ **공통점 — 전부 「초록」이었다.** 실패로 드러나지 않아서 아무도 안 봤다. 꺼져 있는 것보다 나쁘다 — **없으면 없는 줄 알지만 초록은 검증됐다는 뜻으로 읽힌다**
    - ⭐ **그래서 고치는 방법도 같다 — 가드가 걸리는지를 검사하는 테스트를 둔다.** 설정을 되돌리면 그 파일이 빨개지게. 주석으로 남기면 다음 사람이 같은 자리에 다시 선다
      - ⭐ **다섯 번째 건이 그 방법을 이미 해 본 사례다** — Console PR [#14587](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14587)
        - 그 가드는 **2026-09-02 메모리 고갈 사고**(98~99%·에이전트 offline)를 막으려고 넣은 것이다. **막으려던 사고를 다시 부를 수 있는 상태**로 있었다
        - ⚠ **같은 함정에 두 번 빠졌다** — `playwright.config.ts`가 먼저 당해 `CI ?? TF_BUILD`로 고쳐 뒀는데(PR 12744), **그 뒤에** 들어온 vitest 가드가 그걸 몰랐다(PR 13489). **교훈이 파일 하나에만 적혀 있으면 다음 사람은 그 파일을 안 본다**
        - 그래서 **설정 본문을 읽어 `TF_BUILD`를 함께 보는지 검사하는 테스트**를 뒀다. 되돌리면 **그 파일만** 빨개진다
    - ❓ **물을 것** — 우리가 "있다"고 믿는 다른 가드들은 실제로 걸리고 있나. 한 번 전수로 확인할 값이 있어 보인다

  - **[품질] SonarQube — 양쪽 다 전 항목 A 유지**

    |             | Gate   | Coverage                 | Security            | Reliability | Maintainability |
    | ----------- | ------ | ------------------------ | ------------------- | ----------- | --------------- |
    | **GW**      | OK     | 96.5                     | A · 핫스팟 **100%** | A           | A               |
    | **Console** | **OK** | **91.6**(신규 코드 92.1) | A · 핫스팟 100%     | A           | A · **78→53**   |
    - ⭐ **Console 78 → 53은 고친 것이 아니라 판정이다**(아래 근거). P14 신규 코드(~500줄)는 unit+e2e가 촘촘해 **커버리지 플로어에 영향 없다**
    - ⚠ GW 수치는 **마지막 main 스캔 기준**이고 그 뒤 새 스캔 근거를 사내 도구로 가져오지 못했다 — **대시보드 재확인 권장**(바뀌었을 가능성은 낮다)
    - ⚠ **교차 스위트 e2e 플레이크** — 전체 실행마다 **다른 스위트**가 DB 접속·404로 실패하고 격리하면 전부 통과한다. 이번 작업 **이전부터** 있었고 원인 미규명이다. **CI 신뢰도 문제**라 적어 둔다
    - ⭐ **"고친 것" 과 "안 고치기로 한 것" 을 가른 것이 요점이다** — 판정도 조치이고, 근거를 남겨 **다음 사람이 같은 것을 다시 파지 않게** 한다
      - **`void` 55건** — 일부러 안 기다린다는 표시다. 떼면 _"실수로 `await` 을 놓친 것"_ 과 **구분이 안 된다**. ⚠ 규칙이 틀렸다고 적지 않았다 — 그 위험은 **`no-floating-promises` 로 떠다니는 프라미스 자체를 막는 쪽**이 맞고 도입은 별도 판단으로 뒀다
      - **`role="status"` 16건** — 규칙이 제안하는 `<output>` 은 **인라인 요소**라 바꾸면 시각 baseline 이 대거 흔들린다. 접근성 결과는 같고(암묵 role 이 `status`) axe 테스트도 통과 중이다
      - **CSS 2건은 `False Positive`** — `@theme`·`@custom-variant` 는 **Tailwind v4 의 정식 문법**이다. ⚠ DT 의 `js-yaml` 을 `Not Affected` 로 둔 것과 **정반대 경우**다 — 거기선 스캐너가 옳았고 여기선 틀렸다. **섞어 적으면 기록이 사실과 달라진다**
      - **핫스팟 ReDoS 7건은 `SAFE`** — 입력 길이를 공격자가 정하지 못한다(빌드 타임 env·우리가 배포하는 리전 디렉터리·계약에서 생성한 경로 템플릿). ⭐ 결정적 근거는 **정적 export 라 서버가 없다**는 것 — 자원 고갈이 성립하지 않는다
      - ⭐ **1건은 오탐이었다** — `6.3.1.3` 을 IP 로 읽었는데 **앱 버전 문자열**이었다
    - ⚠ **위 「0파일 분석인데 게이트 통과」 와 같은 집안 문제였다** — Console 커버리지가 0 이던 것도 **잡이 테스트를 안 돌려서**였지 코드 문제가 아니었다. 스캐너는 _"측정 안 함"_ 을 **_"한 줄도 커버 안 됨"_** 으로 기록한다
    - ⚠ **코드를 안 바꿨는데 수치가 움직인다** — 9/22 스캔에서 유지보수성이 78 → 124 로 늘었다(제외 범위가 걷히며 8월 이슈가 돌아옴). **등급은 개수가 아니라 가장 나쁜 항목으로 정해지므로**, 건수 추이만 보면 오독한다

  - **S1. 프로젝트 일정(Gantt) — 10/15 스냅샷**
    - **진행률(구현)** — GW ≈ 93% · Console ≈ 92%. **둘 다 코드 feature-complete**이고 잔여는 전부 위 표의 외부 선결이다
    - ⚠ **9/30 「개발환경 연동 완료」 목표를 넘겼다** — 원인은 코드가 아니라 **Entra consent·test 환경** 둘이다. 10월 출시 목표를 유지할지 **일정 재설정이 필요**하다
    - **범례** — 막대: 작성=기본·PR=강조·◆=baseline/마일스톤·**빨강=외부/미정 선결**

    ```mermaid
    gantt
        title v1.0 = Straumann(AXS) 첫 외부연동 · 10월 출시 목표 (10/15 현재)
        dateFormat YYYY-MM-DD
        axisFormat %m/%d
        todayMarker stroke-width:3px,stroke:#d33,opacity:0.6

        section ③ GW SRS + API/DBML (계약 SSOT · baseline v1.0 동결)
        작성·PR·baseline v1.0 (완료 7/20) :done, srs, 2026-06-15, 2026-07-20

        section GW 구현 → dev 통합 → 출시 (코드 feature-complete · dev 통합=Entra·③-I 게이트)
        1단계 GW 독립 코어 (P0~P6·P10·완료) :done, implindep, 2026-07-21, 31d
        2단계 AXS 연동 (P7~P12·코드 완료) :done, implaxs, 2026-07-28, 2026-08-24
        GW 코드 feature-complete       :milestone, done, impldone, 2026-08-24, 0d
        운영자 Entra dev consent (IT-9442·승인 대기·블로커) :crit, active, entra, 2026-09-09, 2026-10-15
        dev 통합·E2E (인프라 완료 9/3·Entra consent·E2E 실행 대기) :crit, active, e2e, 2026-09-03, 2026-10-31
        개발환경 연동 완료 (9/30 목표 — 미달·재설정 필요) :milestone, crit, dev9, 2026-09-30, 0d
        v1.0 production 연동 완료(목표·10월·재검토) :milestone, rel, 2026-10-31, 0d

        section ③-I 인프라 IaC (dev 핵심 완료 9/3 · 자동배포·test/prod 잔여)
        dev 배포·인프라 핵심 (앱 3기동·ingress·IoT·Param Store·KMS 완료 9/3) :done, infcore, 2026-08-19, 2026-09-03
        잔여 dev (자동배포 tag→TEST/PROD·dispatcher 안정화) :active, infrem, 2026-09-03, 2026-10-31
        test 환경 프로비저닝 (요청 8/26·미착수)  :crit, inftest, 2026-09-01, 2026-10-15

        section ③-P-EZ EzServer 연동 스펙 (① 초안=Raymond → ② Thomas 상세 → ③ baseline)
        ① 초안+PR (Raymond)            :done, ezw, 2026-07-20, 5d
        ② Thomas 상세·리뷰·수정         :active, ezpr, after ezw, 83d
        ③ baseline                     :milestone, ezbl, after ezpr, 0d

        section ③-P-CS CleverSpace OnePager (① Raymond → ② Larry 상세 → ③ baseline)
        ① 초안+PR (Raymond·#12239)     :done, cssub, 2026-07-27, 5d
        ② CleverSpace팀(Larry) 상세    :active, cspr, after cssub, 76d
        ③ baseline                     :milestone, csbl, after cspr, 0d

        section ③-P-CO CleverOne OnePager (① Raymond → ② Nick 상세 → ③ baseline)
        ① 초안+인계 (Raymond·SharePoint) :done, cosub, 2026-07-27, 5d
        ② CleverOne팀(Nick) 상세       :active, copr, after cosub, 76d
        ③ baseline                     :milestone, cobl, after copr, 0d

        section ④ AXS 연동 (코드·sandbox e2e=완료 · 실 dev 통합=③-I 대기 · prod=NDA 후)
        AXS 연동 구현·sandbox e2e green(P7·하네스) :done, axsimpl, 2026-08-11, 2026-08-24
        ④ Sub-SRS 경량 문서(완료 8/27·spec-v1.0.69) :done, axssub, 2026-08-27, 1d
        AXS 실 dev 통합 (IoT Core 완료·E2E 실행 대기·dispatcher) :crit, active, axsint, 2026-09-03, 2026-10-31
        AXS prod 자격(NDA 후·선결·미확보) :crit, active, credp, 2026-08-18, 2026-10-15

        section ③-C GW Console — v1.0 (별도 repo · 코드=완료 · dev 통합=Entra 대기)
        v1.0 구현 (mock-first)         :done, conv1, 2026-08-12, 2026-08-24
        v1.0 코드 구현 완료            :milestone, done, conv1m, 2026-08-24, 0d
        GW·Entra 통합테스트 (Entra 승인 대기·미완) :crit, active, contest, 2026-08-24, 2026-10-31

        section v1.0 이후 (deferred · post-v1.0)
        CleverOne 연동 구현 (스펙은 지금·구현 post-v1.0) :codef, after rel, 14d
    ```

  - **S2. 스펙 작성 테이블 — 제품 × 단계 · 매주 스냅샷** · **정본 = 본 Agenda(S2)**
    - 각 셀 앞 이모지 = 스펙 작성 진행: ✅ baseline · 🟢 PR · 🟡 작성중 · ⬜ 미작성 (— = 해당 없음)

      | 제품 | 1단계(호환성) | 2단계(presigned) | 3단계(GW 일원화) | 4단계(멀티리전) | 5단계(Straumann) | 스펙 산출물 |
      | --- | --- | --- | --- | --- | --- | --- |
      | **CleverSpace** | 🟡 버전체크·well-known·오류코드 | 🟡 presigned 발급 API | 🟡 GW 경유 수신 | ⬜ 멀티 Region | — | 🟢 ③-P-CS OnePager 인계(#12239·Larry 검토) |
      | **CleverOne** | 🟡 Vatech-\* 헤더·fallback | 🟡 presigned 이용 | 🟡 Direct→GW 경유 | ⬜ Region 선택·ClinicID | — | 🟢 ③-P-CO OnePager 인계(SharePoint·Nick 검토) |
      | **EzServer(EZ)** | 🟡 헤더 대리 전달 | 🟡 전송 로직(presigned) | 🟡 GW 경유 전환 | 🟡 ClinicID·Region·등록 | 🟡 AXS(갈래A)·presigned 직접 | 🟡 ③-P-EZ OnePager 초안(Raymond→Teddy) |
      | **AlliedStar** | ⬜ (9/28 킥오프·GW 경유 결정) | — | ⬜ GW 경유 수신 | — | — | ⬜ 미착수 — **두 번째 target** |
      | **CleverLab** | — | — | — | — | ⬜ AXS 오더·확정(갈래B) | ④ Sub-SRS(갈래B·보류) |
      | **VatechAPIGateway** | 🟢 호환 게이트(§7.7) | 🟢 presigned 중계(§4.1.4) | 🟢 본체·라우팅·인증·호환 | 🟢 리전 라벨·Region Directory·HA | ⬜ AXS OAuth·Org-ID·온보딩·고정IP | ③ SRS ✅ baseline · **현행 `spec-v1.0.96`** |
      | **GW Console**(③-C) | — | — | — | 🟢 Admin Web Console(Entra 앱계층) | ⬜ 온보딩·Org-ID 후속(gw/1.1·1.2) | ✅ ③-C Sub-SRS baseline(`spec-v1.0`) · 현행 `spec-v1.0.15` |
      | **인프라** | — | — | 🟢 **dev·test·sandbox·prod(4종)** | 🟢 Route53·K8s | 🟢 AXS 고정IP·샌드박스 | 🟢 ③-I IaC 계획서(PR #11973·living doc) + KMS 키 토폴로지 |
      | **외부(Straumann AXS)** | — | — | — | — | 🟡 PPR sandbox=확보(8/11) · ⬜ prod=NDA 후 | ④ 입력(외부 제공) |

    - **스펙 문서 등록처·baseline (SSOT)**

      | 단위 | 스펙 문서 | Repo · 경로 | baseline tag |
      | --- | --- | --- | --- |
      | **③ GW** | SRS(+OpenAPI·DBML·UnitTCL) | `vt-api-gateway` · `docs/specs/` | **`spec-v1.0.97`**(현행) |
      | **③-C GW Console** | Sub-SRS | `vt-api-gateway-console` · `docs/specs/SRS.md` | ✅ baseline `spec-v1.0`(8/11) · 현행 **`spec-v1.0.15`** |
      | **④ AXS** | 경량 연동 프로파일 | `vt-api-gateway` · `docs/specs/04-subsrs-straumann-axs/` | 경량(PPR 자격 확보·착수 가능) |
      | **③-I 인프라** | IaC 구축계획서 | `vt-api-gateway-infra` · `docs/IaC-구축계획서.md` | PR #11973(living doc) |
      | **③-P-EZ EzServer** | GW적응 OnePager | `ezserver_suite`(`v6.5.x`) · `doc/onepager/gw_adaptation/` | 미부여(팀 baseline 예정) |
      | **③-P-CS CleverSpace** | GW적응 OnePager | `ezicloud/ezcloud` · `docs/onepager/gw_adaptation/` | PR #12239(팀 baseline 예정) |
      | **③-P-CO CleverOne** | GW적응 OnePager | SharePoint `gw_adaptation` | — (팀 baseline) |

- **이월 논의 사항 (계속)**

  | #   | 항목                                       | 타입   | 상태                                                                                     |
  | --- | ------------------------------------------ | ------ | ---------------------------------------------------------------------------------------- |
  | 4   | Webhook 클라우드 분배(CleverLab 갈래B)     | [논의] | v1.0 제외 — Open 후 결정                                                                 |
  | 6   | AXS **prod** 자격(Straumann 정식계약)      | [정보] | PPR sandbox=확보(8/11) · prod=NDA 후                                                     |
  | 7   | 경로 B EOS 시점                            | [논의] | EOS 시점만 PM·CS/CO OnePager 미정                                                        |
  | 8   | v1.0 목표 RPS·동시 세션                    | [논의] | 목표치 확정 필요 · test 환경 후 실측 [부하]                                              |
  | 9   | RTO/RPO·유지보수 윈도우                    | [논의] | ❓ **PL 결정 대기** — HA 합격기준. 환경이 생겨도 이것 없이는 HA 실측을 끝낼 수 없다 [HA] |
  | 10  | 감사·consent 보존 기간                     | [정보] | 법무 확인 대기                                                                           |
  | 11  | 호환성 매트릭스 확정본                     | [정보] | CleverSpace/CleverOne OnePager 의존 — 담당팀 baseline 후                                 |
  | 15  | Webhook payload 보존·아카이브 기간(리전별) | [논의] | **법무 확정 대기** — 리전별 ① DB 잔존 기간 ② S3 보관 기간(+가동 임계값)                  |
