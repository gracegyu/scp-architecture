# VT API Gateway — 9/17 주간회의 Agenda

- **이번 주 진행 (~9/17 회의) — 지난 주(9/10) 완료 요약 + 이번 주 착수**
  - **진행률(구현 스냅샷)**
    - **GW 백엔드 ≈ 93%**(8/26 재평가 · Task **90/96 완료**) — v1.0 계획 기능 **구현 완결** · 마무리 = 개발 통합·검증
      - 8/24 feature-complete 이후 **P13 정합 6건 추가 머지** · 잔여 6건은 전부 **GW 코드 완료**
      - **마무리 조건 = 개발 통합·검증** — ③-I 실 인프라 위 실측을 통과해야 완료로 셈
      - ⚠ **남은 6건이 전부 외부 선결** — 코드가 안 써진 게 아니라 실환경이 없어 확인을 못 함(③-I 인프라 5[마이그레이션 Job·IoT Core·공개 ingress·부하 staging·HA Multi-AZ] · Straumann lab order 시드 1 · PL RTO/RPO 목표 1)
      - **GW 코드로 앞당길 잔여 = 0**
    - **[GW Console](https://console.gw.dev.ezcld.net) ≈ 92%**(8/26 재평가 · Task **61/67 완료** · 부분 4 · 미착수 2) · [dev console 열기](https://console.gw.dev.ezcld.net)
      - P0~P6 완료 · **P7 6/7** · **P9 13/15** · P8 1/4
      - ⚠ **남은 6건이 전부 외부 선결** — 코드가 안 써진 게 아니라 **실환경이 없어 확인을 못 한다**(Entra 앱 등록·dev 재배포·test 환경·prod 도메인·CloudFront 헤더). **Console 코드로 앞당길 잔여 = 0**
      - **성격 셋** — 통합 검증 3(`8-1`·`8-2`·`9-17`) · 남의 작업 2(`7-6` ③-I 배선 · `8-4` PL 배포) · 내부 조사 1(`9-13` 플레이크)
      - ⚠ **"검증이니 곧 끝난다" 가 아니다** — 검증은 어긋난 것을 **찾는** 일이고 찾으면 Console 작업이 된다(`9-17` 1단계만으로 갭 2건). 남은 8% 는 **폭을 아직 모르는 일**이다 → S1 상세

  - **이번 주(9/17) 착수·진행 · 선결 대기**
    - **[GW·Console × DT·SonarQube 온보딩] ✅ 완료(9/10)** ⭐ _(회의 결정 직후 당일 완료)_ — **4 커버리지(GW·Console × DT·SonarQube) 전부 실데이터 확인·Quality Gate 둘 다 Pass**.
      - **결과**
        - DT SBOM components — GW **424** · Console **260**(CycloneDX 1.6).
        - SonarQube — GW **17.5k LoC**(버그 5 · 취약점 0 · hotspot 21) · Console **24.2k**(버그 5 · 취약점 0 · hotspot 15).
        - ⚠ **커버리지 0%** — 파이프라인이 테스트를 돌리지 않는다. 잡에 test+coverage 를 붙일지 **별도 논의**.
      - **부수 성과 — 전 제품에 있던 잠복 버그 5건을 찾아 고쳤다**(`python/sbom_extractor.py`)
        - **핵심은 "종료코드 삼킴"** — DT·ABS 업로드와 trivy 가 실패해도 빌드는 SUCCESS 로 끝났다. **DT 가 비어 있는데 초록불**이던 것이 이 때문이다.
        - 그 외 — 불완전 SBOM 업로드 · POSIX `rmtree` 실패.
        - **Windows 에이전트에선 드러나지 않다가 Linux 이관에서 노출**됐다.
        - **Verify Upload 스테이지 추가** — 종료코드를 믿지 않고 DT 를 직접 조회해 확인한다.
        - **trivy 0.70.0 고정** — 0.71+ 는 CycloneDX 1.7 을 산출하는데 DT 4.13.3 은 1.6 까지만 받아 400 으로 거절한다. DT 업그레이드 없이 해소.
        - 상세 = `sbom/jenkins` repo.
      - **만든 것**(`sbom/jenkins` · main)
        - `vars/sharedPipelineSbomPyLinux.groovy`(신규 · Node/pnpm Linux) · jenkinsfile 4종 · config 2종 · Node 샘플 템플릿 2종.
        - 💡 **착수 전 가정 2건이 틀렸다** — ① pnpm 은 기존 `-py`(python) 계열이 **이미 지원**하고 있었다(Groovy Node 템플릿 신설 불요). ② `-py` 가 Windows 였던 건 **EzServer 가 Windows 대상 SW** 라서이고, VT 는 Linux 대상이다.
      - **남은 것 = 없음(완결)**
        - 트리거는 **초기 'QA 태그' 안을 철회하고 일 1회 새벽 스케줄로 확정**(9/10). 기존 잡들과 같은 **pollSCM** 이라 ADO 연동·API 토큰·변수그룹이 필요 없다.
        - 4개 잡을 **KST 새벽 2~5시로 분산**(commit `40986aa` · Verify Upload 통과).
        - **별도 논의 = 커버리지 0%** — 잡에 test+coverage 를 붙일지.
      - ⚠ **부수 발견(별건) — 기존 잡 13개가 업무시간에 돌고 있다**
        - `jenkins-server` 컨테이너에 **TZ 가 설정돼 있지 않아 UTC** 로 동작한다. 크론이 의도와 다르게 해석된다.
        - 예 — SBOM 잡의 `H 3` 이 **KST 정오**다. CI 와 에이전트를 놓고 경합한다(`eslockserver` #18 이 12:19 KST 실행된 것이 증거).
        - **급하지 않아 별건**(`TZ=Asia/Seoul` 은 전체가 9시간 시프트되므로 신중해야 한다) · 회의 안건 아님.
        - VT 4개 잡은 UTC 로 환산해 넣어 실제로 새벽에 돈다.
    - **[DT 취약점 탐지 복구]** ✅ **완료(9/14)**
      - 🔴 **그동안 npm 제품 전체가 취약점 "0" 으로 보고되고 있었다** — VT 만이 아니라 **EzServer 전 계열**이 같은 상태였다.
      - ✅ **13개 프로젝트 탐지 복구** — `EzUpdater` 174 · `AuthProvider` 153 · `REST API v2` 85 · … · `vt-api-gateway` 2 · `console` 6. 취약점 DB **39만 → 63만**.
      - 📌 **한 줄 원인** — npm 취약점 공급원(Sonatype OSS Index)이 **유료화로 끊겨 있었다**. 무료 대체(Google OSV · GitHub Advisories)로 갈아타고 재분석해 정상화했다.
      - ⚠ **이건 끝이 아니다** — 드러난 **1,000건 이상을 누가 심사·조치할지 정해져 있지 않다**. → **논의 [R1]**

      <br/>

      **▼ 상세**
      - **원인 — npm 취약점 공급원이 통째로 끊겼다**
        - **Sonatype OSS Index 가 2026-04-29 부터 402 Payment Required** 반환. 무료 티어 종료 · Sonatype Guide 로 이관 · **레거시 엔드포인트 2026-12-31 완전 종료** 예정.
        - npm 패키지는 **NVD 에 CPE 가 없어** 내장 분석기로 안 잡힌다. OSS Index 가 유일한 공급원이었고, 그것이 끊긴 순간 npm 은 통째로 0 이 된다.
        - **비-npm 제품은 NVD 로 계속 잡히고 있어 문제가 가려져 있었다** — `Ez3D-i`(purl = `generic`·`debian`·`boost`)는 190건 정상.
        - 48시간에 402 에러가 **458건** 쌓여 있었다.
      - **조치**
        - **① Google OSV 활성화** — 생태계 `npm` · `crates.io` · `Pub` · `Packagist`. DT 컴포넌트 purl 을 전수조사해 선정했다(npm 20,366 · cargo 4,929 · pub 398 · composer 66).
        - **② GitHub Advisories 활성화** — **classic PAT(스코프 없음)로 설정 완료 · 정상 동작 중**(9/14 기준 15,265건 수집).
          - **왜 classic 인가** — DT 는 GitHub **GraphQL** 로 전역 보안 권고를 조회한다.
            - 저장소·조직 단위로 권한을 좁히는 신형 **fine-grained PAT 는 이 쿼리에서 401** 이 난다(DT 저장소에 보고된 알려진 제약).
            - 토큰 종류를 고를 때 주의할 점이고 **문제는 아니다**.
          - **보안상 부담도 낮다** — 권고 조회는 공개 데이터라 **스코프를 하나도 주지 않았다**. 유출돼도 공개 데이터 조회 외에는 할 수 있는 게 없다.
          - ⚠ **잔여 리스크** — 조직이 향후 **fine-grained 전용 정책**을 강제하면 이 연동이 끊긴다. 다만 npm 은 OSV 가 이미 커버하므로 그때도 탐지 공백은 생기지 않는다.
        - **③ OSS Index 비활성화** — 402 로 0건만 반환하던 것. **유료화 전환 때문이고, 되살릴 경로가 없다.**
          - **로드맵**
            - 2026-03-31 — 기존 토큰이 Sonatype Guide 로 이관.
            - 2026-04-28 — API 사용이 Guide 요금제·크레딧 체계로 전환(무료 계정 **월 500 크레딧**).
            - 2026-04-29 — `ossindex.sonatype.org` 가 **402 반환 시작**.
            - 🔴 **2026-12-31 — 레거시 엔드포인트 완전 종료.**
          - **우리 상태** — 계정(`gracegyu@gmail.com`)과 토큰이 설정돼 있는데도 402 다. 크레딧 소진인지 이관 누락인지는 Sonatype 계정에서 확인해야 구분된다. 어느 쪽이든 결과는 같다.
          - ⚠ **유료로 전환해도 지금은 못 쓴다** — 엔드포인트 URL 변경 기능이 **DT 4.14.0 부터**인데 우리는 **4.13.3** 이다. 쓰려면 DT 업그레이드가 선행된다.
          - **비용도 맞지 않는다**
            - 크레딧은 **컴포넌트 단위**로 소모되는데, 우리 DT 에만 **약 26,000 컴포넌트**가 있다
              - npm 20,366 · cargo 4,929 · 그 외
            - ⚠ 무료 500 크레딧은 **1회 스캔에도 못 미친다**
            - 매일 도는 잡을 감당하려면 **상당한 유료 플랜**이 필요하다
          - ✅ **결론 = 유료 전환 불필요. 대체가 이미 검증됐다.**
            - `AuthProvider` 가 OSS Index 시절(v6.3.1) **141건** → OSV·GHSA 로 바꾼 v6.5.0-fda **153건**. 같은 제품에서 **동등하거나 더 나은 탐지**다.
            - npm 권고의 원천은 GHSA 이고 OSV 가 그것을 집계하므로 **공급원이 애초에 겹친다**.
            - **DT 가 Sonatype Guide 를 정식 지원하면 그때 재검토**하면 된다.
        - **④ 이미 올라가 있던 프로젝트를 강제로 다시 분석** — 취약점 0 이던 것 전부.
          - **DT 는 BOM 이 올라오는 시점에만 분석한다.** 취약점 소스를 새로 켜도 **기존 프로젝트를 소급해서 다시 보지 않는다.**
          - 그래서 원래대로면 **잡이 다음 새벽에 BOM 을 다시 올릴 때까지 기다리거나**, 사람이 BOM 을 수동으로 재업로드해야 한다.
          - 하루를 기다리지 않으려고 **DT 에 재분석을 직접 지시**했다(`POST /api/v1/finding/project/{uuid}/analyze`). 이미 등록된 컴포넌트를 **새 취약점 DB 와 다시 대조**하는 것이라 SBOM 을 새로 만들 필요가 없고, 몇 분이면 끝난다.
          - **앞으로는 자동이다** — 잡이 매일 새벽 BOM 을 올리고, 그 시점의 최신 DB 로 분석된다.
      - **결과**
        - 취약점 DB **390,692 → 629,114**.
        - **13개 프로젝트에서 탐지 복구**(EzServer 계열 11 + VT 2).
        - 2차로 `crates.io`·`Packagist` 를 추가해 **Rust·PHP 제품까지 커버**했다.
        - VT 수치가 낮은 것은 의존성이 최신이라서다. **0 이 아니라는 점이 핵심**이고, 앞으로 신규 CVE 가 잡힌다.

        | 프로젝트                         | 이전 |    이후 | 비고                              |
        | -------------------------------- | ---: | ------: | --------------------------------- |
        | EzUpdater                        |    0 | **174** |                                   |
        | EzServer AuthProvider            |    0 | **153** | 같은 제품 v6.3.1 = 141 → 정합     |
        | EzUpdater Frontend               |    0 | **109** |                                   |
        | EzServer REST API v2             |    0 |  **85** | `cargo`(Rust) — 2차 미러로 해소   |
        | EzServer WebConsole              |    0 |  **77** |                                   |
        | EzLauncher                       |    0 |  **73** | v6.3.1 = 64                       |
        | EzServer LicenseManager Frontend |    0 |  **70** | v6.3.1 = 44                       |
        | EzServer PMS Integration         |    0 |  **63** | 2차 미러로 해소                   |
        | EzServer LicenseManager          |    0 |  **46** | v6.3.1 = 43                       |
        | EzWebServer                      |    0 |  **35** | `composer`(PHP) — 2차 미러로 해소 |
        | EzServer Messenger               |    0 |  **32** | v6.3.1 = 33                       |
        | **vt-api-gateway-console**       |    0 |   **6** |                                   |
        | **vt-api-gateway**               |    0 |   **2** |                                   |

      - ⚠ **결정 필요(공유가 아니라 안건)**: **드러난 취약점 1,000건 이상의 심사·조치 주체와 정책이 없다.** DT 에 수치만 쌓이고 누가 언제 무엇을 고치는지 정해져 있지 않으면 R1 온보딩의 실효가 없다. 상세 = 아래 논의 사항.
      - ⚠ **부수 발견(별건)**
        - **① GHSA 전량 미러링이 오래 걸린다** — 첫 실행이 `Connection reset` 으로 중단됐다(15분에 400건). **인증 문제는 아니다.**
          - 재시작 후 정상 속도(5~6초에 200건)로 진행 중 — **9/14 기준 15,265건 수집 · 체크포인트 2023-01-24**.
          - **incremental 이라 매일 자동으로 이어받는다**(그대로 두기로 결정).
          - 첫 중단의 원인인 egress 불안정은 **Jenkins install flake** 와 같은 뿌리로 의심된다.
        - **② 빌드 호스트 `/etc/hosts` 오타** — `126.0.0.1 localhost`(127 이어야 함). `localhost` 가 공인 대역을 가리켜 python 등 일부 도구만 간헐 실패했다. **수정 완료(9/14)**.

    - **[최초 admin 부트스트랩 allowlist]** ✅ **구현 완료(9/10 · PR #14212 머지)**
      - 🔴 **해결한 것 — "최초 admin 데드락"**: Console 실 로그인 후 **승인해 줄 admin 이 아무도 없어** 아무도 들어갈 수 없던 상태.
      - **계약** — env `GW_BOOTSTRAP_ADMIN_EMAILS`. 첫 로그인 시 JIT 로 admin 자동 부여(요청→승인 생략) · 매칭=이메일 · 저장=oid · 멱등 · 비회수 · 최소 2명.
        - SRS §7.1.4 · §7.9.2 · env-reference §2.3 에 pin(**spec PR #14204 · `spec-v1.0.85`** · Jack 승인 · main).
      - **tenant 제약 보강**(`spec-v1.0.86`) — allowlist 설정 시 `GW_OPERATOR_OIDC_TENANT` **필수**. 타 테넌트 권한상승을 막는다.
        - 코드 fail-closed = #14212(main) · 문서 머지·태그 완료 = PR #14236(Jack 리뷰어).
      - **코드**(`OperatorBootstrapService` · admin JIT 경로 · PR #14212)
        - unit·e2e green(데드락 해소 · 멱등 · 대소문자 · 비-allowlist 403) · 독립리뷰 🟢.
        - 보안 지적 반영 — M1(테넌트 fail-closed) · M2(감사 loud).
      - ⚠ **부수 — 전 PR 이 막혔던 사건**: 신규 org-wide `multer` HIGH CVE 로 dep-scan 게이트가 **모든 PR 을 차단**. surgical override PR #14220(`multer ^2.3.0`)을 먼저 머지해 언블록했다.
      - **다운스트림** — ③-I(Jack) 이 Parameter Store 에 `GW_BOOTSTRAP_ADMIN_EMAILS` + `GW_OPERATOR_OIDC_TENANT` 주입. 즉시 언블록은 `dev:operator --sub <oid> --role admin`(로컬).
    - **[GW dev 배포·통합]** core·receiver·dispatcher·**admin 전부 dev 기동 확인**(9/10: admin `/v1/admin/me` 401=healthy·8/31 503 해소) · 통합은 Entra admin consent 승인 후 실로그인부터(③-I #3)
    - **[Entra 앱 등록]** ✅ dev 2앱 회신 완료(9/9) · **admin consent 승인 완료(IT · 9/10)**
      - 로컬 실로그인으로 검증됨.
      - **`aud` 형식 확정** — dev SSM 은 `api://<GUID>`, GW admin 은 bare `<GUID>`. **표기가 다르나 둘 다 Entra 표준**(스코프는 `<audience>/.default`).
      - 배포 후 로그인 실패 시 **첫 용의자**로 둔다.
    - **[GW Console 통합]** ⭐ **실 Entra + 제3자 전 경로 검증 통과(9/15)** — 권한 생명주기가 실 환경에서 한 바퀴 돌았다
      - ⭐ **`T-FE-8-1` 로컬 검증 통과(9/10)** — admin consent 승인(IT · 9/10) 후 **실 Entra 로그인 → 토큰 → GW admin 응답**까지 성공.
        - `issuer`·`aud`·`scp` 가 전부 맞다는 것이 **통과 자체로 증명**됐다(이전 401 은 GW `.env` 가 로컬 OIDC 스텁을 보던 것).
        - **최초 admin 도 allowlist 로 자동 부여**되는 것을 확인.
      - ✅ **`ⓒ dev redirect URI` 실측 완료(9/14)** — 배포 후 로그인이 **AADSTS50011 없이 성공**. 등록돼 있었음이 확인됐고 **Entra 미확인 항목은 남아 있지 않다**.
        - `aud` 는 dev SSM `api://<GUID>` · GW admin bare `<GUID>` 로 표기가 다르나 **둘 다 표준**(스코프는 `<audience>/.default`).
      - ✅ **로그인 무한 반복 해소**([PR 14229](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14229) 머지)
        - 고리 = **401 → logout → `/login` → SSO 세션으로 조용한 재로그인 → 같은 토큰 401**.
        - 자동 시도를 **60초 3회에서 끊고 사유를 보여 준다**(수동 재시도는 유지) · 카나리 검증.
      - ⭐ **dev 실 배포 완료(9/14)** — 목 제거 · **실 Entra 로그인 정상** · 프로세스 버전 **4줄 전부 채워짐**(admin·core·receiver·dispatcher = `2deaf14`). `T-FE-8-1` 은 **로컬(9/10)·dev(9/14) 양쪽 통과**
        - ⚠ **9/10~9/14 사이 결함 4건은 전부 "실 환경에서만 드러나는" 종류였다** — 목·로컬·단위테스트 어디에서도 보이지 않는다. dev 실배포를 세우기 전까지 **알 수 없었던 것들**이라는 점이 이번 구간의 교훈이다
        - **① 목 배포 회귀** — `entra` 수동 배포 **12분 뒤** main 머지가 부른 자동 빌드가 기본값 `mock` 으로 돌아 **같은 버킷을 덮었다**.
          - 파라미터는 **수동 실행에만** 실린다. 즉 **기본값이 곧 평상시 dev 의 모습**이다.
          - 기본값을 `entra` 로 바꾸고 실 빌드에 main 조건을 걸어 해소([PR 14299](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14299)).
        - **② `timed_out` 로그인 막힘** — 며칠 만에 들어가면 **로그인이 아예 안 됐다**(브라우저 저장소를 비워야 풀림).
          - `acquireTokenSilent` 의 숨은 iframe 이 Entra 세션 만료로 끊기는데, 그 오류가 `InteractionRequiredAuthError` 가 **아니라서** 그대로 던져졌다.
          - **재로그인하면 그만인데 길이 막힌** 상태다. ⚠ **운영자가 며칠 만에 올 때마다 밟는다**([PR 14303](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14303)).
        - **③ fan-out 포트** — `core`·`receiver`·`dispatcher` 가 `응답 없음`. 프로세스도 version API 도 정상이었다.
          - 원인 = **admin 코드 기본값이 컨테이너 포트(`:3000`)를 k8s Service 주소에 갖다 썼다**(Service 는 `80`).
          - Console 이 `es-gitops` 4앱 values 를 독립 검증했다(`service.port: 80` · ClusterIP · 단일 네임스페이스 · 내부 TLS 없음).
          - → GW 코드 기본값에서 포트 제거([PR 14307](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14307)).
        - **④ 빌드 시각 공백** — 화면의 빌드 시각이 `시각 미상`.
          - **`Build.QueueTime` 이 잡 환경에 실리지 않아** 빈 문자열이 번들에 박혔다(로그 실측 — `command not found` · 값 `[]`).
          - 같은 블록의 `Build.SourceVersion` 은 정상이라 **그 변수 하나만** 없는 것이다.
          - 빌드 직전 직접 스탬프로 교체([PR 14309](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14309)).
      - ⭐ **권한 요청 흐름 완결(9/14)**
        - **제3자 로그인 테스트 1회**에서 결함 4건이 한꺼번에 드러났고 v1.0 범위를 모두 닫았다
        - ⭐ **실사용자를 태워 보기 전에는 어느 테스트도 잡지 못하던 것들**이라는 점이 이번 구간의 수확이다

        - ⚠ **근본은 API 부재였다**
          - 화면이 `/me` 의 `roles` 에서 `requested` 를 찾고 있었다
          - 그런데 계약상 거기 실리는 것은 **실효 역할(active)뿐**이라 그 필터가 **영원히 빈 배열**이었다
          - → 요청을 보내도 흔적이 남지 않았고 **Console 로는 고칠 수 없었다**
          - FR-CON-04[v1.0] "승인 대기" · FR-CON-07[v1.0] "이력 노출" 을 만들 **조각이 빠져 있던 것**
          - → GW 가 **`GET /v1/admin/me/access-requests` 신설**(PL 승인 · `spec-v1.0.88`/`.91` · PR #14320)

        - **결함 4건**
          - **① 승인받고도 콘솔에 못 들어감** — PR #14311
            - 게이트가 `no_access` 를 요청 화면으로 보내는데 **역할이 생겨도 내보내는 쪽이 없었다**
            - ⚠ **주소창을 고칠 줄 아는 사람만** 들어갔다
            - 게이트가 보낸 사람만 표시해 두고 승인 즉시 착지점으로 보낸다
          - **② 요청을 보내도 화면이 그대로** — 보낸 사람이 **보내지지 않은 줄 알고 또 보냈다**
          - **③ 이미 가진 역할이 "요청 중"으로 표시** — 승인을 기다려야 하는 줄 알고 대기 — PR #14315
          - **④ 승인 후 새로고침해야 반영** — PR #14315 → #14318
            - ⚠ **한 번 고쳤다가 실패했다**
              - Refine 의 `invalidate` 는 **resource 기준**이라 `useCustom` 으로 부르는 `/me` 를 **잡지 못한다**
              - 불러도 조용히 아무 일도 안 일어나 **"고친 줄 알았는데 그대로"** 가 됐다
              - 재조회 여부를 **직접 세는 테스트**를 붙여 다시 잡았다

        - ⭐ **목이 서버와 달랐던 것이 뿌리였다**
          - 목은 `/me` 에 `requested` 를 실어 두어 **"목에선 뜨는데 실제론 안 뜨는 화면"** 을 만들어 냈다
          - 계약대로 경계를 갈라 바로잡았다 — `/me` = 실효 역할 · `/me/access-requests` = 요청·이력
          - 시각 회귀용 `pending` 시나리오도 **같은 규칙으로 다시** 만들었다

        - **UI 재구성(PL 결정)**
          - 거부를 상시 경고 카드로 띄우던 것을 **행 인라인 + 접이식 이력**으로 바꿨다
          - ⚠ 거부는 막다른 길이 아니라 **다시 요청할 수 있는 상태**인데 그렇게 보이지 않았다
          - 정작 할 일(역할 고르기)이 카드에 묻혔다
          - `rejected`(승인 전 거부)와 `revoked`(관리자 회수)를 **구분해** 말한다

        - ⚠ **v1.0 interim 안내 유지**
          - 승인 알림이 v1.1(§7.10)이라, 그때까지 *"자동 알림이 없으니 관리자에게 직접 알려 달라"* 를 화면에 남긴다
          - ⚠ **승인권자를 이름으로 열거하지는 않는다**
            - 그 목록을 주는 API(`/me/approvers`)도 v1.1 이다
            - 모르는 것을 아는 척하면 **요청자가 엉뚱한 사람을 찾아간다**

        - **자기 요청 자기 승인 = 허용**(PL 결정)
          - 승인 경로가 admin 전용이고 admin 은 이미 직접 부여가 가능하므로 **새 권한 상승이 아니다**
          - 유일한 제약인 **"admin 최소 1명"** 은 GW 가 409 로 집행하고 Console 도 버튼을 잠근다
          - ⭐ **추가 코드 없음**

        - **시각 회귀로 고정** — PR #14327
          - 이 화면은 **콘솔을 처음 만나는 사람이 보는 유일한 화면**인데 덮여 있지 않았다
            - ⚠ 무너져도 **이미 쓰는 사람은 모른다**
          - 처음 요청 / 대기 중 **두 상태를 따로** 찍는다 — 달라 보여야 하는 것이 요점이라 하나만 찍으면 차이가 사라져도 안 드러난다
          - ⭐ 찍어 보다가 **문구 결함 하나를 더 잡았다** — 역할이 0인 사람에게 "역할 **추가** 요청"

      - ⭐ **제3자 실사용 전 경로 검증 통과(9/15)** — PL 직접 수행
        - **실 Entra + 제3자 계정**으로 권한 생명주기를 **끝에서 끝까지** 돌렸다
          - 제3자 로그인 → 권한 요청
          - admin 승인 → 화면 진입
          - **역할 회수**(revoked)
          - **재신청** → 다시 승인
        - ⭐ **전부 정상 동작**(PL 확인 — *"잘 돼"*)
        - ⭐ **이것이 닫은 것** — v1.0 권한 체계가 **실 환경에서 한 바퀴 돌았다**
          - 그동안은 목·로컬·단위 테스트까지였고, 실 Entra + 타인 계정 조합은 검증된 적이 없었다
          - 9/14 결함 4건이 전부 **이 경로에서만 드러나던 것**이라, 같은 경로로 되짚어 확인한 셈이다
        - ⭐ **회수 후 재신청이 막히지 않는다**는 것도 함께 확인됐다
          - 화면: `revoked` 는 체크박스를 잠그지 않고 *"이전에 회수됨 · 다시 요청할 수 있습니다"* 로 안내
          - 서버: `historical`(rejected·revoked)만 있으면 **재요청 허용**(중복·이미보유만 409)
          - ⚠ 회수는 **막다른 길이 아니다** — 그 말이 화면에 없으면 당사자는 끝난 줄 알고 포기한다


      - ⚠ **v1.1 로 넘긴 것 3건**
        - **승인 알림**(§7.10) — **Email(Amazon SES) 단일**로 확정·머지(spec-v1.0.90)
          - Teams는 채널이 타 법인 인원 멘션 불가라 v1.1 제외 → backlog B-21
        - **승인권자 조회**(`/me/approvers`) — 알림이 생기면 대체로 불요
        - **본인 역할 제거** — 제거는 **승인 없이 즉시**(권한이 내려가는 방향이라 위험이 낮다)
          - "마지막 admin" 보호는 그대로
        - ⚠ **공통 관찰 — "조용한 실패"가 진단 비용의 대부분이었다**
          - SSM 로더는 에러를 stdout 으로 내보내 `$( )` 에 삼켜졌다(어떤 실패든 침묵).
          - `Build.QueueTime` 은 빈 값이 조용히 박혔다.
          - 목 배포는 초록으로 끝나고 덮었다.
          - 💡 **실패가 보이게 만드는 것**이 다음 구간의 개선 항목이다 — ⭐ `es-ci-templates` 는 **이미 반영 완료**(9/14 확인).
    - **[Console dev 실배포 · SSM 3중 결함]** ✅ **9/10 진단·조치 완료**(①③ 해소 · ②는 템플릿 개선으로 이관)
      - 🔴 **증상** — 실 Entra 빌드가 `Load env from SSM` 에서 **에러 한 줄 없이 0.5초 만에** 죽어 두 번 실패.
        - [빌드 55466](https://dev.azure.com/ewoosoft/es-platforms/_build/results?buildId=55466) · [빌드 55475](https://dev.azure.com/ewoosoft/es-platforms/_build/results?buildId=55475).
      - **IAM·KMS·jq 는 전부 무관이었다** — 같은 잡·같은 `dev-ci` 역할에서 `--with-decryption` 조회가 `rc=0`. 파이프라인에 진단 스텝을 넣어 갈라냈다.
      - **① SSM 값이 여러 줄(pretty-print) JSON** — 로더가 `이름<탭>값` **한 줄**을 가정한다. `read` 가 첫 줄에서 끊기고 `jq` 가 `{` 하나를 받아 실패.
        - **③-I 조치** — 한 줄 JSON 으로 재기록 + **넣는 도구가 `jq -c` 를 쓰는지** 확인. 값만 고치면 재발한다.
      - **② 에러가 구조적으로 침묵했다** — 진단이 오래 걸린 진짜 이유.
        - `emit_env` 가 에러를 **stdout** 으로 내보내는데 호출부가 `body="$(emit_env …)"` 라 `$( )` 가 삼킨다. **어떤 실패든 무조건 침묵**하는 구조였다.
        - 최소 수정은 `>&2` 한 줄. 근본은 `--output text` 대신 `--output json`+`jq`(값에 개행이 하나라도 있으면 같은 방식으로 또 깨진다).
        - ⭐ **해소 확인(9/14 · `es-ci-templates`)** — 템플릿이 **모든 실패를 최상위에서 보고**하도록 바뀌었고(명령 치환 안에서 보고하지 않음) 파싱도 `--output json`+`jq` 로 전환됐다.
        - **우리가 제안한 것보다 넓다** — 개행이 든 값은 **키 이름과 함께 미리 실패**시켜, `.env` 한 줄에 담기지 않는 값이 조용히 망가지는 것까지 막는다. 코드 주석에 9/10 사례가 근거로 인용돼 있다.
      - **③ `.env` 출력 경로가 한 겹 중복** — `Build.SourcesDirectory` 가 이미 레포 폴더를 포함하는데 접두를 또 붙였다.
        - ①② 를 고쳐도 다음 게이트(`test -s .env`)에서 막힌다.
        - **Console 조치** — [PR 14233](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14233).
      - ⚠ **별건 · ③-I 조치 대기 — admin 이 영영 못 읽는 값이 있다**
        - `GW_BOOTSTRAP_ADMIN_EMAILS` 가 **`/dev/vt-api-gateway-console/config`(프론트 빌드용)** 에 들어가 있다.
        - **`/dev/vt-api-gateway-admin/config` 로 이동 + admin 파드 재시작** 필요(env 는 부팅 시 1회 로드 · SRS §7.8.4).
        - 미조치 시 **로그인은 되는데 `no_access` 로 떨어진다.**
    - **[운영자 매뉴얼 · 최초 관리자]** ✅ **작성 완료 · 스펙 검토 통과**([PR 14234](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14234))
      - 🔴 **메운 구멍** — _"첫 admin 은 누가 승인하나"_ 에 매뉴얼이 답을 갖고 있지 않았다.
      - **케이스 E 신설** — 승인 없이 부여 · TOFU 아님 · 멱등 · 비회수 · 재로그인 복원 · **2명 이상 권장** · 감사 기록은 `system`.
      - **트러블슈팅 3줄** — 승인할 관리자 없음 / **재시작 누락** / **테넌트 값 누락 시 admin 부팅 거부**(spec-v1.0.86).
      - 배포 주입 절차는 ③-I 소관이라 **일부러 넣지 않았다.**
    - **[스펙 · v1.1 알림/self-service + self-GET 갭 pin]** 이번 주 신규 — **spec PR 3건 전부 머지**(+ 구현 PR #14319 · 리뷰어 Jack)

      - ✅ **v1.0 갭 pin** — [PR 14316](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14316) · `spec-v1.0.88` 태그
        - 운영자 본인 요청 이력 조회 `GET /v1/admin/me/access-requests`(§7.9.2) 신설
        - ⭐ **Console FR-CON-04/07 의 데이터 소스 부재를 해소** — 요청을 보내도 흔적이 남지 않던 것
        - `status` = non-active(active 는 `/me` 가 SSOT)
        - `note` 겸용 · `rejected`/`revoked` semantic 명문화

      - ✅ **self-GET OpenAPI 통제문서** — [PR 14320](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14320) · `spec-v1.0.91` 태그
        - 같은 계약을 계약 정본(`vt-api-gateway.openapi.yaml`)에 `get` 으로 추가
        - ⚠ **#14316 머지 시점엔 통제문서에 `get` 이 없어** 후속 반영이 됐다
          - **프로세스 정정(PL)**: 통제문서 = 계약 SSOT(스펙 선작성) → 구현 gen(`admin.gen.yaml`) 은 compare 로 정합만
        - 태그 번호는 1.0.90(v1.1)이 먼저 머지되며 밀렸다

      - ✅ **GW 구현** — [PR 14319](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14319) · `afff3ce` (9/14 머지)
        - `getAdminMeAccessRequests` — **RBAC 없이 본인 것만**
          - 위조 차단: 대상은 **토큰의 operatorId** · 본문·쿼리로 받지 않는다
        - `status` = requested · rejected · revoked (**active 제외** = `/me` 가 SSOT)
        - `requestedAt` 내림차순 · 결정행은 `decidedByOperator` 를 read-time 조인(N+1 회피)
        - 검증: unit 16 + operators 135 · e2e 4 · `admin.gen.yaml` 재생성
          - 독립 pre-PR 리뷰 🟢(orderBy id 타이브레이크 반영) · CI green(`vt-api-gateway-ci`·`devsecops-admin`)
        - ⭐ **Console FR-CON-04/07 데이터 소스 실연결**

      - ✅ **self-GET 계약 3-PR 클로즈** — main 공식 compare **델타 0** 확정(9/14 · #14320 머지본 `d1e9fc4`)
        - admin `OK GET/POST /v1/admin/me/access-requests`
        - 구성: SRS `1.0.88` · 구현 #14319 · OpenAPI `1.0.91`

      - 📌 **프로세스 못박음(PL 지시)** — OpenAPI **계약 우선(contract-first)·역행 금지**
        - `abc-dev-assistant` 에 명문화: `projects/vt-api-gateway/README.md §2.1` 신설 + `dev-chain-backend` 체크포인트 + `dev-chain-design` Step 3-3
        - 통제문서 = 계약 정본(스펙 선작성) → 구현은 **generate + compare 만**
        - ⚠ **gen 을 계약처럼 커밋하는 역행 금지** · 통제문서에 없는 오퍼레이션은 **멈추고 스펙 선요청**

      - **v1.1 예약** — [PR 14312](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14312) · `spec-v1.0.90` 태그(9/14 머지)
        - **§7.10 운영자·이벤트 알림** 신설
          - 이벤트 2건: 역할 요청 `access.requested` · 결정 `access.decided`
          - **채널 = Email(Amazon SES) 단일**
          - 언어 기본 ko/en 선택 · **비-PHI 불변식** · 비동기·멱등·DLQ
        - **§7.9.2 self-service 2건**
          - 승인권자 가시성 `GET /me/approvers`
          - 역할 self-제거 `DELETE /me/roles/{id}`
        - **Jack 리뷰 반영(9/14)**
          - SES = **중앙 단일 리전** 확정(prod us-east-1 · 비-prod 서울 · §2.1.1 전역 의존 등재)
          - ⚠ **Teams 는 타 법인 멘션 불가**로 backlog **B-21** 로 유예 — 유예된 이벤트·채널도 B-21

      - ⚠ **③-I 준비(알림 착수 전)**
        - Amazon SES 발신 도메인 검증 + production access
        - 중앙 단일 SES(prod us-east-1 · 비-prod 서울) — 가이드는 PR 14312 본문

      - 📌 **버전 — 머지·태그 순서**(전부 완료)
        - `1.0.88`(self-GET SRS) → `1.0.90`(v1.1 알림) → `1.0.91`(self-GET OpenAPI)
        - `1.0.87`·`1.0.89` 는 머지 순서가 밀리며 **결번**
      - ✅ **backlog B-22 완전 클로즈(9/14)** — `openapi:compare` 델타 **15 → 0**(57 op 전부 정합)
        - 스코핑 문제가 아니라 **실제 shape 델타**였다(compare 는 이미 앱별 프리픽스로 스코핑돼 있었다)
        - 세 갈래로 나눠 소거했다 — 아래 (1)·(2)~(5)·code-side

        - ✅ **(1) compare allOf 평탄화** — 구현 PR https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14323 (`7ede092`)
          - 통제문서는 `allOf[base & 확장]`(DRY), gen 은 평탄 object 라 **허위 델타**가 났다(clinics·clinics/{id}·memo·clinics/me 4건)
          - **델타 15 → 11**
          - 안전장치: 충돌 key 를 `conflict[…]` 로 표면화 · 미해석 `$ref` 는 보수적 폴백(독립 리뷰 M1/M2 반영·unit 15)
          - ⭐ **통제문서의 `allOf` 는 그대로 둔다** — DRY 를 포기하는 대신 비교기를 고쳤다

        - ✅ **(2)~(5) 통제문서 편집** — spec PR https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14325 · `spec-v1.0.92` 태그(main `5468ea9`)
          - **(3) targets 분리** — `Target`(응답) / `TargetUpsert`(요청) · 원문 자격은 **요청에만**, 응답은 ref 만(gen 4응답 byte-identical)
          - **(2) nullable 조이기** — connector descriptor · me displayName/email · devices clinicId(clinic-less 의도)
          - **(4) 응답 구체화** — server-configuration · auth/token claims · PATCH clinics/{id} 200 에 Clinic body
          - **(5) getAdminMe 403 제거**
          - 사전확인에서 **델타 11 → 3 → 통제문서 측 0** — audit state free-form 화, heartbeat `configVersion` 제거(gw/1.1 재도입)까지 함께 반영
          - ⚠ `format`(int64·uuid)은 **compare 가 비교하지 않아** 통제문서 그대로 둔다 — 맞추려고 통제문서를 낮추지 않는다

        - ✅ **code-side gen 정밀화** — 구현 PR https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14330 (`21e1d7f`)
          - `TargetUpsert.ports` = 정수 **실범위 1–65535**
            - ⚠ `.int()` 만으로는 JS 안전정수(±9e15)까지 통과해 **포트로서 의미가 없었다**(Raymond 지적 · `MIN_PORT`/`MAX_PORT` 상수)
          - `sourceIpAllowlist` = `string[]`
          - audit `before/afterState` = nullable(any) — #14325 free-form 화 뒤의 잔여
          - 회귀 unit(포트 경계·거부·gen shape·audit nullable) + 독립 리뷰 🟢(High 0·Med 0)

        - 🏁 **최종 상태** — `pnpm openapi:compare` **델타 0**(57 op) · `openapi:check` EXIT 0
          - 통제문서(`spec-v1.0.92`) ↔ gen(admin·core·receiver) **완전 정합**
          - ⭐ compare 가 이제 **실제 드리프트만** 잡는다

    - **[제품 연동 스펙]** EzServer OnePager 수령 확인(잔여)

- 논의 사항 (이번 주 · 신규 · R#)
  - **[R1] 보안·품질 지표를 누가 심사·조치할 것인가** _(9/14 신규 · 판단 = PL · 품질/RA)_
    - 🔴 **측정은 되는데 조치 경로가 없다** — DT 취약점 **1,000건 이상** · SonarQube Quality Gate **25개 중 14개 실패** · security hotspot 검토율 **전 제품 0%**.
    - ❓ **정할 것 5가지** — ① **소유자**(개발팀 / 품질·RA / 보안) ② **주기**(상시 / 릴리스 전 / 월 1회) ③ **범위**(critical·high 만 / 전부) ④ **미조치 처리**(억제·예외 승인 절차) ⑤ **게이트**(릴리스를 막을 것인가)
    - ⚠ **선행 확인** — **품질/RA 가 SBOM 만 요구하는지, 취약점 조치 이력까지 요구하는지**(SRS §6.13). 이 답에 따라 위 5가지의 답과 작업량이 크게 달라진다.
    - 💡 **기술 배선은 이미 끝나 있다.** DT Policy·Notification, SonarQube Gate 조건 모두 관리자 화면에서 조정 가능하다. **지금 필요한 것은 설정이 아니라 정책 결정이다.**

    <br/>

    **▼ 근거·상세**
    - **배경 — 안 보이던 것이 한꺼번에 드러났다**
      - 9/14 DT 취약점 탐지를 복구하자 **1,000건 이상**이 나타났다(위 「이번 주 진행」 표 참조).
      - 같은 제품 v6.3.1 이 141, v6.5.0-fda 가 153 인 데서 보듯 **새로 생긴 것이 아니라 그동안 안 보였던 것**이다.
      - 방치하면 다음 릴리스도 같은 상태로 나간다.
    - **문제 — 수치는 생겼는데 조치 경로가 없다**
      - **누가·언제·무엇을 고치는지가 정해져 있지 않다.**
      - DT 의 조치 장치가 전부 비어 있다.
        - Policy Management(심각도 임계) — **정책 0건**(Policy Violations 전 제품 0)
        - Vulnerability Audit(심사 워크플로) — 미사용
        - Notifications — 미설정
      - 이대로면 DT 는 숫자만 쌓이는 대시보드가 되고, 온보딩이 "가시성 확보"에서 멈춘다.
    - **SonarQube 도 같은 상태다(9/14 실측)**
      - 전체 25개 중 **Quality Gate 실패 14 · 통과 10**.
      - **`new_security_hotspots_reviewed` 가 전 제품 0%** — security hotspot 을 아무도 검토하지 않았다.
      - 실패 원인은 두 갈래로 나뉜다. **둘 다 조치가 필요하고 시급성만 다르다.**
      - **(가) 게이트 실패 조건이 커버리지뿐인 것** — `vt-api-gateway` · `vt-api-gateway-console`
        - 커버리지 리포트를 안 넘겨 0% 로 계산된 결과다.
        - 커버리지는 **ADO CI 가 이미 측정**한다(GW = unit+e2e 합산 + floor 게이트). SonarQube 에서 다시 재는 것은 중복이다.
        - → **조건을 뺄지, Jenkins 잡에 테스트 실행을 붙일지** 결정 필요.
        - ⚠ **단, "코드가 깨끗하다"는 뜻이 아니다**
          - 신규 위반이 0 인 것은 **신규 라인이 210줄·117줄뿐**이기 때문이다(기준선 `PREVIOUS_VERSION` · 분석 2회).
          - 전체로 보면 **VT 도 위반 35건·149건**이 있고 hotspot 검토율은 다른 제품과 같은 **0%** 다.
          - 신규 코드가 쌓이면 (나) 와 같은 상태가 된다.
      - **(나) 신규 코드에서 위반이 나오는 것** — 조건을 조정해도 사라지지 않으므로 **상환 계획**이 필요하다.
      - **아래 14건은 전부 Quality Gate 실패다**(통과 = `eslockserver` 등 10건). `common-rust_es_config` 를 뺀 13건에 **커버리지 0% 조건이 공통**으로 걸려 있어 열에서 생략했다. `—` = 해당 조건 기준 내.

        | 프로젝트                          |  게이트  | 신규 위반 | 신규 중복 | hotspot 미검토 | 전체 위반 |    갈래     |
        | --------------------------------- | :------: | --------: | --------: | :------------: | --------: | :---------: |
        | ezcloud                           |   실패   |   **184** |      5.7% |       O        |         — |     나      |
        | cloudwebviewer                    |   실패   |   **183** |         — |       O        |         — |     나      |
        | ezwebserver                       |   실패   |   **126** | **11.4%** |       O        |         — |     나      |
        | oneid                             |   실패   |    **68** |      3.2% |       O        |         — |     나      |
        | ezserver-license-manager-frontend |   실패   |        59 |         — |       —        |         — |     나      |
        | ezserver-license-manager          |   실패   |        24 |      9.4% |       O        |         — |     나      |
        | frontend                          |   실패   |        19 |         — |       —        |         — |     나      |
        | ezserver-updater                  |   실패   |        16 |         — |       —        |         — |     나      |
        | common-rust_es_config             |   실패   |        12 |         — |       —        |         — |     나      |
        | ezserver-auth-provider            |   실패   |        11 |         — |       O        |         — |     나      |
        | ezserver-messenger                |   실패   |         1 |         — |       —        |         — |     나      |
        | ezserver-updater-frontend         |   실패   |         0 |         — |       O        |         — | 나(hotspot) |
        | **vt-api-gateway**                | **실패** |         0 |         — |       O        |    **35** |   **가**    |
        | **vt-api-gateway-console**        | **실패** |         0 |         — |       O        |   **149** |   **가**    |

        _(전체 위반은 VT 만 채웠다 — (가)/(나) 대비를 보기 위한 것이고, 기존 제품은 미집계.)_

    - **왜 DT 와 묶어서 정하나**
      - 둘 다 **"측정은 되는데 조치 경로가 없다"** 로 구조가 같다.
      - 따로 정하면 소유자·주기·게이트 기준을 두 번 정하게 되고 서로 어긋난다.
      - 아래 5가지는 양쪽에 그대로 적용된다.
    - **정할 것 5가지**
      - **① 소유자** — 제품별 개발팀 / 품질·RA / 보안 담당 중 누구인가
      - **② 주기** — 상시 / 릴리스 전 / 월 1회
      - **③ 범위** — DT = critical·high 만인가 전부인가(DT Policy 로 임계). SQ = 신규 위반 0 을 유지할 것인가, hotspot 검토를 의무화할 것인가
      - **④ 미조치 처리** — 억제(suppress)·예외 승인 절차가 필요한가(누가 승인하나)
      - **⑤ 게이트** — 특정 심각도가 남으면 릴리스를 막을 것인가. **SQ 커버리지 조건 처리(위 (가))도 여기서 함께 정한다** — 빼거나, 잡에 테스트를 붙이거나
    - **규제 연동 — 사실상 선행 조건**
      - 온보딩 착수 때 남긴 **"품질/RA 에 SBOM 요구·범위 확인(SRS §6.13)"** 이 아직 미해결이다.
      - **SBOM 제출만인지, 취약점 조치 이력까지 요구하는지**에 따라 위 5가지의 답과 작업량이 크게 달라진다.
    - **참고(비-블로킹)**
      - 기술 배선은 이미 끝나 있다. DT Policy·Notification, SonarQube Quality Gate 조건 모두 관리자 화면에서 조정 가능하고 정해지면 바로 반영된다.
      - **지금 필요한 것은 설정이 아니라 정책 결정이다.**
      - 별건 — SonarQube 에 **분석 이력이 한 번도 없는 껍데기 프로젝트 8건**이 있다. 정리 대상 여부 확인 필요.
        - `common-rust_*` 3 · `ezserver_installer` · `ezserver_pms_integration` · `ezserver_rest_api_v2` · `ezserver_suite` 등.

- **[③-I Jack 인프라 요청 추적]** — 회의에서 상태·ETA 확인
  - ✅ **9/3 대거 착지(Jack)** — 실 IoT Core · Parameter Store(compat well-known 200) · KMS CMK(payload+target) · 공개 ingress 가 **dev 완료**.
  - admin 부팅(401) · Entra 앱 회신(9/9) 까지 겹쳐 **dev 인프라 핵심이 대부분 해소**됐다.
  - ⚠ **남은 dev 블로커** — Entra admin consent · 자동배포 · 마이그 Job · dispatcher 안정화 · test 환경.
  - 상세 = `docs/handoff/pending-infra-requests.md §9` · [PR 12653](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/12653).

  > **범례**
  >
  > - ✅ 완료 — 괄호는 완료일 · 날짜만 있으면 **이전 주 완료**
  > - 🆕 = **이번 주(9/11 이후) 신규 해결·검증** — *(아직 없음)*
  > - 🟠 부분 · ☐ 미완 · ⚠ 전달 필요
  >
  > *(9/10 주 현실화분 반영: pending-infra §9 Jack 9/3 실측 + dev 엔드포인트 재확인.)*

  | # | 요청 | 수신 | dev | prod |
  | --- | --- | --- | --- | --- |
  | 1 | Region Directory 호스팅 + `consoleHost` 발행 | ③-I | ✅ publish(8/18·`regions.gw.dev.ezcld.net`) · ✅ `consoleHost` 발행(8/31·PR #13355 Jack 머지·`curl regions.json` 확인) | ☐ 도메인 후(prod consoleHost) |
  | 2 | GW Console dev 호스팅([console.gw.dev.ezcld.net](https://console.gw.dev.ezcld.net)) | ③-I | ✅ 개통(8/19·CD 파이프라인·딥링크 rewrite) | ☐ 도메인 후 |
  | 3 | **dev GW 백엔드 배포·env 주입**(`DATABASE_URL`[공용 `common-dev-db`·`gw` DB·apne2]·`REDIS_URL`·`GW_REGION`=apne2·AWS **Pod Identity**·`NODE_ENV` 차트 주입) | ③-I | **core·receiver·dispatcher = ✅ 기동 완료**(8/31 자가검증: core·receiver 404=healthy backend·기동 확인 / dispatcher=HTTP 엔드포인트 없어 배포상 기동) · **admin = ✅ 부팅 확인(9/10: `/v1/admin/me` 401=healthy·8/31 503 해소)** · 단 **Console 실로그인은 admin consent 승인 대기**(consent 미승인→사용자 토큰 취득 불가) | ☐ |
  | 4 | **운영자 Entra 앱 등록**(GW Admin API + Console SPA·2앱·PKCE) | IT·③-I | ✅ **dev 2앱 등록·회신 완료(9/9)·GW 배선 완료** · 남은 것 = **admin consent 승인 1건**([IT-9442](https://vts.vatech.com/projects/IT/issues/IT-9442)·IT팀 승인 대기·조직 1회) → **승인 전까지 Console 실로그인 불가**(admin API 자체는 9/10 부팅 확인·401) | ☐ prod 등록 시 동일(도메인 후) |
  | 5 | **env-reference 환경별 값 채움**(test·sandbox·prod endpoint·호스트·리전) | ③-I | ✅ dev · ☐ test/sandbox/prod | ☐ |
  | 6 | **dev-seed grant**(`DATABASE_URL` 변수그룹·Environment 승인게이트) — 전용 수동 파이프라인 `gw-dev-seed.yml`(멱등·`dev:showcase`)용 | ③-I | 🟠 **미완 확정(9/10 ADO 실측: `gw-dev-seed`/`DATABASE_URL` 변수그룹 부재)** · 파이프라인(id 335)·Environment 승인게이트(id 9)·AWS 서비스커넥션 `gw-dev-seed` 등록됨 ✅ · **남은 것 = `DATABASE_URL`(dev RDS) 변수그룹 미생성** → **Jack: 변수그룹 `gw-dev-seed`+`DATABASE_URL`(시크릿)+파이프라인 링크** + **SC 롤 KMS grant**(Encrypt/GenerateDataKey). AWS 5변수는 **GW가 서비스커넥션 전환**(PR 13358)→Jack 불요. ⚠ **혼동 주의**: Jack이 9/3 한 것은 **KMS CMK(#8)**(별개 항목)이며 dev-seed 변수그룹/grant는 미완. + alias명 정합(#8 실물 `alias/gw-payload-apne2` ↔ 시드 기대 `alias/gw-webhook-payload`) 확인 필요. 요청 8/20. | — |
  | 7 | **`pg_trgm` CREATE EXTENSION 권한**(clinic 검색 선결 · env-reference §2.1) | ③-I | ✅ 문제 없음(Jack 확인 8/20 — `gw_app`=`gw` DB OWNER·trusted extension) | ☐ prod 동일 확인 |
  | 8 | **KMS CMK provisioning**(webhook payload·target 자격 alias·리전별 · 8/4 키 토폴로지 · env-reference §2.4) | ③-I | ✅ **완료(9/3 Jack·AB#5650)**: ① `alias/gw-payload-apne2`(PR 12413) · ② `alias/gw-target-cred-apne2`(PR 13573 apply·SSM alias 4앱 주입) · 기능검증=admin 파드 복구 후 | ☐ 리전별(prod) |
  | 9 | **admin API dev ingress 노출**(`admin.apne2.gw.dev.ezcld.net`·Entra-gated 공개 ingress) — Console이 실 dev DB 데이터를 조회하려면 admin 부팅에 더해 이 ingress가 있어야 함(없으면 admin이 떠도 Console이 못 부름) | ③-I | ✅ **ingress 구축 확인**(8/25 curl: 443 OPEN·ALB 응답) — 단 전 경로 **503(ALB에 healthy target 0·즉시응답)** = **admin 미기동**이 원인(ingress 문제 아님)·**9/10 재확인: `/v1/admin/me` = 401**(admin 부팅·healthy·8/31 503 해소·ingress serving 확인) · 남은 건 Console 로그인용 **admin consent** | ☐ 도메인 후 |

- **[GW 구현 선결 추적 · 외부 인프라·자격]** — E2E·배포가 외부 선결로 막힌 항목. 소유별 상태·ETA 확인.

  | # | 선결 항목 | 소유 | dev | prod |
  | --- | --- | --- | --- | --- |
  | 1 | 공개 ingress(AXS→GW webhook 수신) | ③-I | ✅ **완료**(9/3 Jack 확정·es-infra PR 12931·8/20 · `curl axs.webhook.apne2.gw.dev.ezcld.net`→404 healthy) | ☐ prod |
  | 2 | 실 IoT Core(MQTT 다운링크·Thing/policy·IRSA·`MQTT_URL`) | ③-I | ✅ **완료(dev·9/3 Jack)**(es-infra PR 12190 · 공유 policy `dev-ezserver-edge` · `MQTT_URL`=Secrets Manager `dev/…dispatcher` · dispatcher `iot:Publish gw/clinic/*`) · ⚠ **E2E 미실행**(dispatcher exit137 반복·enroll Thing 0=별건) | ☐ |
  | 3 | 자동배포 파이프라인(main→DEV·tag→TEST/PROD) | ③-I | 🟠 **① main→DEV = 됨**: `devsecops-{core·receiver·dispatcher·admin·migrate}.yml` **main 트리거** → ECR push → es-gitops `imageTag` 스탬프 → ArgoCD sync(dev 4앱 배포·migrate id 340). **9/10 ADO 실측: 5개 파이프라인 등록·최근 실행 `main`/`individualCI`/`succeeded`(9/3)** → **main 머지 시 dev 자동 배포 실동작 확인**. · **② tag→TEST/PROD = 안 됨**: 릴리스 태그 기반 상위환경 승격 경로 **미구축** — 원인은 파이프라인이 아니라 **test 환경 미프로비저닝(선결 #5)·prod 미설정**. 환경 생기면 같은 템플릿에 태그 트리거만 추가 | ☐ prod |
  | 4 | Parameter Store write IAM + ESO + AWS 커넥션(compat publish 포함) | ③-I | ✅ **완료(dev·9/3 Jack·AB#5650)**: write IAM·SC(PR 12694) · 발행 파이프라인(354 run 53818) · ESO 마운트(es-gitops PR 13571) · `GW_COMPAT_MATRIX_DIR` 주입 · `/.well-known/production/server-configuration.json` **200** | ☐ test/prod |
  | 5 | **test 환경 프로비저닝**(별도 인프라·GW=infra 분류·상시 최소 baseline+임시 확장·부하/HA 사이즈업 포함) | ③-I | ☐ **요청 완료·마감 8/26** | ☐ |
  | 6 | AXS 자격 | Straumann·영업 | ✅ sandbox(8/11) | ☐ prod(NDA후) |
  | 7 | 파일 붙은 lab order 시드 | Straumann·④ | ☐ (sandbox) | — |
  | 8 | **마이그레이션 배포 Job 배선**(migrate 이미지 ECR push[앱과 같은 SHA] · 매 배포 前 1회 `migrate deploy`·성공 gating·fail-closed) | ③-I | ✅ **완료(dev)**: ③-I 회신 3건 해소(§확정)·**PreSync→sync-wave Job 확정**(AB#5206·wave0 SA/ESO→wave1 migrate→wave2 Deploy)·ECR `vt-api-gateway-migrate`(es-infra PR 13034)·`devsecops-migrate.yml` 완성·**ADO 파이프라인 등록(id 340)** · GW 몫(#12926·#13173·#13184) | ☐ test/prod OWNER 확인 |

  _(`—`=해당 없음.)_

  > **[③-I 요청 전달 감사 — 2026-08-26]**
  >
  > ⭐ **"문서에 선결로 적혀 있다 ≠ Jack 에게 전달됨."**
  >
  > - 두 추적 표를 훑어 GW handoff **7종 전부 결과 Form·전달 흔적 0** 확인 — **작성 ≠ 전달**
  > - 전달 흔적이 없던 항목
  >   - ③-I #8 · GW 선결 #1 · #2 · #4
  >   - Console CloudFront 헤더 4-tier · 사내 접근제한(8/19 회신서 누락 변종)
  > - **조치** — handoff + 결과 Form 을 **단일 전달 패킷**으로 묶음
  >   - [pending-infra-requests.md](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/handoff/pending-infra-requests.md&version=GBmain)(GW repo · 초안)
  >   - **전달 주체 = Raymond**(PL 지시)
  > - ⚠ **재발 방지** — 이후 모든 ③-I 요청은 handoff + Form 으로 전달하고, 회신을 이 표에 **일자·산출물로 기록**
  > - 모범 사례 = 마이그레이션 인계(#13020)

- 공유 사항 (결정 아님 · 논의사항인지 애매한 것을 임의 결정해 공유 · 매주 상시)
  - **S1. 프로젝트 일정(Gantt) — 9/10 스냅샷(현실화)**
    - **진행률(구현)**
      - **GW ≈ 93%** — v1.0 계획 기능 코드 완결(8/24 feature-complete) · 잔여=dev 통합(Entra·③-I 인프라)
        - 잔여 = ③-I 실 인프라 게이트 · 개발 통합검증 · 계약 경화(OpenAPI 코드-first 일원화)
      - **GW Console ≈ 92%** (8/26 재평가) — Task **61/67 완료** · 부분 4 · 미착수 2
        - 잔여 **6건이 전부 외부 선결** — Console 코드로 앞당길 잔여 **0**
        - 성격이 셋으로 갈린다:
          - **통합 검증 3**
            - ✅ `T-FE-8-1`(실 Entra 로그인 왕복) — **완료**(로컬 9/10 · dev 9/14 · 제3자 전 경로 9/15)
            - ⏳ `T-FE-8-2`(실 GW 여정 e2e) · `T-FE-9-17`(목↔실 GW 응답 대조)
          - **남의 작업 2** — `T-FE-7-6` CloudFront 헤더 **배선**(③-I) · `T-FE-8-4` prod **배포**(PL 실행)
          - **내부 조사 1** — `T-FE-9-13` 플레이크(가설 확보·**다음 발생 대기**)
        - ⚠ **"검증이니 곧 끝난다" 로 읽으면 안 된다**
          - 검증의 목적은 어긋난 것을 찾는 것이고, **찾으면 그게 Console 작업이 된다.**
          - `T-FE-9-17` 은 **1단계(목↔계약)만으로 갭 2건**이 나왔다(`FleetState.clinicId` 누락 · `Device.createdAt/updatedAt` 부재).
          - 2단계는 **실 GW 응답**과 맞추는 것이라 더 나올 수 있다.
          - 🔴 **화면은 목만 보고 개발됐고 목은 실물보다 관대했다** — 지금까지 난 결함의 절반이 그 구멍에서 나왔다.
          - Entra 도 claim→역할 매핑 · 딥링크 왕복(`?to=` 쿼리 보존)을 **소스로만 확인했고 한 번도 밟아 본 적이 없다.**
        - 즉 **남은 8% 는 "8% 만큼의 일" 이 아니라 "폭을 아직 모르는 일"** 이다 — 아무것도 안 나오면 며칠, 목↔실 GW 가 여러 곳 어긋나 있으면 그보다 늘어난다.
    - **목표 = 10월 출시**(역산·잠정 — 잔여 변수 = prod 자격[NDA후]·부하/HA 환경)
    - **범례** — 막대: 작성=기본·PR=강조·◆=baseline/마일스톤·**빨강=외부/미정 선결** / 선결(빨강): AXS **prod** 자격(NDA 후·Straumann)

    ```mermaid
    gantt
        title v1.0 = Straumann(AXS) 첫 외부연동 · 10월 출시 목표 (9/10 현재)
        dateFormat YYYY-MM-DD
        axisFormat %m/%d
        todayMarker stroke-width:3px,stroke:#d33,opacity:0.6

        section ③ GW SRS + API/DBML (계약 SSOT · baseline v1.0 동결)
        작성·PR·baseline v1.0 (완료 7/20) :done, srs, 2026-06-15, 2026-07-20

        section GW 구현 → dev 통합 → 출시 (코드 feature-complete · dev 통합=Entra·③-I 게이트)
        1단계 GW 독립 코어 (P0~P6·P10·완료) :done, implindep, 2026-07-21, 31d
        2단계 AXS 연동 (P7~P12·코드 완료) :done, implaxs, 2026-07-28, 2026-08-24
        GW 코드 feature-complete       :milestone, done, impldone, 2026-08-24, 0d
        운영자 Entra dev consent (IT-9442·승인 대기·블로커) :crit, active, entra, 2026-09-09, 2026-09-19
        Entra dev 준비 완료 (admin consent·Console 로그인 게이트) :milestone, crit, entram, after entra, 0d
        dev 통합·E2E (인프라 완료 9/3·Entra consent·E2E 실행 대기) :crit, active, e2e, 2026-09-03, 2026-09-30
        개발환경 연동 완료(목표·9월)   :milestone, crit, dev9, 2026-09-30, 0d
        v1.0 production 연동 완료(목표·10월·재검토) :milestone, rel, 2026-10-31, 0d

        section ③-I 인프라 IaC (dev 핵심 완료 9/3 · 자동배포·마이그Job 잔여 · test/prod 미착수)
        계획서 ①초안→②Jack 상세→③병합 (완료 7/27·PR #11973) :done, infplan, 2026-07-20, 2026-07-27
        dev 배포·인프라 핵심 (앱 3기동·ingress·IoT·Param Store·KMS 완료 9/3) :done, infcore, 2026-08-19, 2026-09-03
        잔여 dev (자동배포 tag→TEST/PROD·마이그Job 배선·dispatcher 안정화) :active, infrem, 2026-09-03, 2026-09-30
        test 환경 프로비저닝 (요청 8/26·미착수)  :crit, inftest, 2026-09-01, 2026-10-15

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

        section ④ AXS 연동 (코드·sandbox e2e=완료 · 실 dev 통합=③-I 대기 · prod=NDA 후)
        AXS PPR sandbox 자격 확보(8/11) :done, cred, 2026-08-11, 1d
        AXS 연동 구현·sandbox e2e green(P7·하네스) :done, axsimpl, 2026-08-11, 2026-08-24
        AXS 코드·sandbox e2e green     :milestone, done, axsdone, 2026-08-24, 0d
        ④ Sub-SRS 경량 문서(완료 8/27·spec-v1.0.69) :done, axssub, 2026-08-27, 1d
        AXS 실 dev 통합 (IoT Core 완료·E2E 실행 대기·dispatcher) :crit, active, axsint, 2026-09-03, 2026-09-30
        AXS prod 자격(NDA 후·선결·미확보) :crit, active, credp, 2026-08-18, 2026-10-15

        section ③-C GW Console — v1.0 (별도 repo · 코드=완료 · dev 통합=Entra 대기)
        SRS 작성 (8/5)                 :done, consrsw, 2026-08-05, 6d
        v1.0 구현 (mock-first)         :done, conv1, 2026-08-12, 2026-08-24
        v1.0 코드 구현 완료            :milestone, done, conv1m, 2026-08-24, 0d
        GW·Entra 통합테스트 (Entra 승인 대기·미완) :crit, active, contest, 2026-08-24, 2026-09-30
        통합테스트 완료(목표)          :milestone, crit, contestm, 2026-09-30, 0d

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
      | **CleverLab** | — | — | — | — | ⬜ AXS 오더·확정(갈래B) | ④ Sub-SRS(갈래B·보류) |
      | **VatechAPIGateway** | 🟢 호환 게이트(§7.7) | 🟢 presigned 중계(§4.1.4) | 🟢 본체·라우팅·인증·호환 | 🟢 리전 라벨·Region Directory·HA | ⬜ AXS OAuth·Org-ID·온보딩·고정IP | ③ SRS ✅ baseline · **현행 `spec-v1.0.84`** |
      | **GW Console**(③-C) | — | — | — | 🟢 Admin Web Console(Entra 앱계층) | ⬜ 온보딩·Org-ID 후속(gw/1.1·1.2) | ✅ ③-C Sub-SRS baseline(`spec-v1.0`) → S4 |
      | **인프라** | — | — | 🟢 **dev·test·sandbox·prod(4종)** | 🟢 Route53·K8s | 🟢 AXS 고정IP·샌드박스 | 🟢 ③-I IaC 계획서(PR #11973·living doc) + KMS 키 토폴로지 |
      | **외부(Straumann AXS)** | — | — | — | — | 🟡 PPR sandbox=확보(8/11) · ⬜ prod=NDA 후 | ④ 입력(외부 제공) |

    - **스펙 문서 등록처·baseline (SSOT)**

      | 단위 | 스펙 문서 | Repo · 경로 | baseline tag |
      | --- | --- | --- | --- |
      | **③ GW** | SRS(+OpenAPI·DBML·UnitTCL) | `vt-api-gateway` · `docs/specs/` | **`spec-v1.0.84`**(현행 · v1.0 baseline 동결) |
      | **③-C GW Console** | Sub-SRS | `vt-api-gateway-console` · [docs/specs/SRS.md](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/specs/SRS.md&version=GBmain) | ✅ `spec-v1.0`(8/11) |
      | **④ AXS** | 경량 연동 프로파일 | `vt-api-gateway` · `docs/specs/04-subsrs-straumann-axs/` | 경량(PPR 자격 확보·착수 가능) |
      | **③-I 인프라** | IaC 구축계획서 | `vt-api-gateway-infra` · `docs/IaC-구축계획서.md` | PR #11973(living doc) |
      | **③-P-EZ EzServer** | GW적응 OnePager | `ezserver_suite`(`v6.5.x`) · `doc/onepager/gw_adaptation/` | 미부여(팀 baseline 예정) |
      | **③-P-CS CleverSpace** | GW적응 OnePager | `ezicloud/ezcloud` · `docs/onepager/gw_adaptation/` | PR #12239(팀 baseline 예정) |
      | **③-P-CO CleverOne** | GW적응 OnePager | SharePoint `gw_adaptation` | — (팀 baseline) |

  - **S3. GW 백엔드(③) 현황 — Phase 요약 (9/1)** _(NestJS 코어·부모 SRS · Console은 S4)_

    | Phase | 범위 | 상태 |
    | --- | --- | --- |
    | **P0~P6·P10** 1단계 코어 | 스캐폴드·데이터모델·인증(JWKS)·enrollment·region·호환게이트·프록시·fleet/config | ✅ 완료 |
    | **P7** External Connector·AXS | 아웃바운드 OAuth2·egress fail-closed·AXS 실연동·커넥터 전략·presigned 중계 | ✅ 완료 |
    | **P8~P11** 2단계 | webhook 수신·Dispatcher/분배·Admin CRUD(RBAC·break-glass·audit) | ✅ 완료 |
    | **P12** E2E·하드닝 | 12-1 아웃바운드·12-2 compat·12-5 presign·12-7 업로드위임·12-8 다운로드·12-9 webhook라우팅 | ✅ 완료분 · ◑ 진행 |
    | **P12** 잔여 | 12-6 인바운드+MQTT(ingress·IoT Core=완료 9/3·**E2E 실행 대기**) · 12-3 부하 실측(하네스 완료·③-I test) · 12-4 HA(③-I Multi-AZ) | 🟠 IoT/ingress 해소 · 부하/HA=test 대기 |
    | **P9-5** 실 IoT 프로비저닝 | (a) 코드 완료(어댑터·mock) · (b) 실 IoT Core mTLS 실증 | 🟠 (a)완료·(b) **IoT Core 완료(9/3)**·실증 대기(dispatcher·enroll) |
    | **P0-5** 자동배포(CD) | ECR/ArgoCD·main→DEV·tag→TEST/PROD | 🟠 **main→DEV 자동=됨**(파이프라인 main 트리거·ArgoCD) · tag→TEST/PROD=상위환경(선결#5·prod) 대기 |
    | **v1.0 정합·하드닝**(지난 주·9/10) | connector_type 어댑터 프로파일 레지스트리(파생 폐기·특정 target 하드코딩 금지·#13357) · target_id DNS 라벨 전 소비자 일괄+seed 하이픈(#13363) · dev-seed AWS 서비스커넥션(#13358) · CleverSpace `internal_bypass` 단정 제거(#13404) · 데모 steps 정직성(#13314) · unknown connector_type fail-closed 3계층 회귀 확인 | ✅ 머지 완료 |
    - 커버리지(merged·8/20): 전역 96.7 / 91.9 / 93.9 / 96.5 · 보안 도메인 98.5 / 96.0 / 100 / 98.4 · 핵심 보안파일 16개 각 100% — **CI floor 게이트 통과**.

    - **남은 작업 — 전부 외부 선결(GW 코드는 feature-complete·코드로 앞당길 잔여 = 0)**

      | Task | 남은 작업 | GW 상태 | 막는 것(루트 블로커) | 소유 |
      | --- | --- | --- | --- | --- |
      | **T-PLAT-0-7** | 마이그레이션 배포 Job | ✅ 이미지·인계 명세·GW몫 | ✅ **배선 완료**(sync-wave Job·ECR PR 13034·pipeline id 340·회신 3건 해소) — dev 완료·test/prod=OWNER 확인만 | ③-I |
      | **T-DISP-9-5** | 실 IoT Core 프로비저닝 실증 | ✅ 어댑터·최소권한 policy·cert·enroll | **IoT Core infra=완료(dev·9/3)** · 남은=E2E 실증(dispatcher exit137 안정화·Thing enroll) | ③-I(infra)·GW(실증) |
      | **T-E2E-12-6** | E2E webhook→IoT 다운링크 | ✅ 수신·dispatcher drain·멱등·주권 | **공개 ingress·실 IoT Core 둘 다 완료(9/3)** · 남은=E2E 실행(dispatcher 안정화·enroll) | ③-I·GW |
      | **T-E2E-12-3** | 부하 실측 | ✅ 하네스·스크립트·파이프라인 초안(#13048) | test staging(실 SQS/EKS)·부하 EC2 | ③-I |
      | **T-E2E-12-4** | HA/카오스 실측 | ✅ drain·RTO probe·loss-verify·파이프라인(#13022·#13048) | test staging·Multi-AZ·FIS **+ RTO/RPO 목표** | ③-I **+ PL** |
      | **T-E2E-12-5** | 환자문서 order-file presign | ✅ create/download 실측 | 파일 붙은 lab order 시드 | Straumann |
      - 🔴 **최우선 블로커(회의에서 밀 것)**
        - **① Entra admin consent 승인** — dev 2앱 회신 9/9 · IT-9442. **admin API 는 부팅됨**(9/10 401)이나 **consent 미승인**이라 Console 실로그인이 안 된다 → **dev 통합검증 정체**.
        - **② test 환경 프로비저닝** — 선결 #5 · 마감 8/26. 풀리면 **부하·HA 2건이 동시에 해제**된다.
        - ❓ **PL 결정 대기 = RTO/RPO 목표**(HA 합격기준).
        - ✅ **GW 코드/설정 잔여 = 0** — 마이그레이션·ECR·파이프라인까지 완료.
      - 🟢 **지금 착수 가능 — IoT 다운링크 E2E**(T-DISP-9-5 · T-E2E-12-6) · **③-I 대기 아님 · GW 몫**
        - 경로는 스펙 정의 — 토픽 `gw/clinic/{clinicId}/#` · `MQTT_URL`/`IOT_ENDPOINT` · ShareName `ezserver`.
        - 순서 — ① **dispatcher exit137 원인규명·해소** → ② **device Thing enroll 1건** → ③ **webhook→IoT Core→EzServer 다운링크 E2E 1회**.
        - **9/10 직접 실측(read-only)**: `aws iot list-things`=**0**(enroll된 Thing 없음 실증) · dev IoT 엔드포인트 `a2ig1yuqacb8gl` 일치.
        - ⚠ **접근 경계** — dispatcher 파드(exit137) 진단에 **dev EKS 접근**이 필요한데 현재 자격 계정에는 안 보인다(IoT 는 보이나 **EKS 클러스터 0**).
          - → **Jack 에게 dev EKS 접근 개방 요청**, 또는 **dev 접근을 가진 쪽**이 `kubectl describe/logs` 로 원인 특정(OOM=리소스→③-I / 코드→GW).
        - 그 외(부하·HA=test 환경 · presign=Straumann 시드)는 여전히 막힘.

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
    | **P7** 공통 UX·i18n·동시성·보안 | 세션만료·403·오류분류·stale-write·i18n·보안/a11y 게이트 | 🟡 **6/7**(T-FE-7-6 보안 리뷰 — **배포 헤더만 잔여**·③-I) |
    | **P8** 실 e2e·배포 | Entra dev 전환·staging 실연동·baseline 승인·prod 배포 | 🔴 외부 선결(Entra·staging GW·CORS·도메인) |
    - 커버리지(unit+component·8/26): 전역 **91.2 / 86.0 / 85.5 / 92.2** — **CI floor 통과**(85/85/82/86). 테스트 **unit·component 1,164 · e2e 172 · a11y 27 · 시각회귀 17**(전부 차단 게이트).

    - **남은 작업 — 전부 외부 선결(Console 코드로 앞당길 잔여 = 0)**

      | Task | 남은 작업 | Console 상태 | 막는 것(루트 블로커) | 소유 |
      | --- | --- | --- | --- | --- |
      | **T-FE-8-1** | dev Entra 실 OIDC 전환·claim→역할 검증 | ✅ MSAL 실배선·env 스위치·`verify:entra` · 9/9 회신값으로 로컬 실로그인 실측(scope 노출 확인) | **Entra admin consent 승인**(앱 회신 9/9·IT-9442) · admin API dev 기동 = ✅ 9/10 확인(401) | IT/③-I |
      | **T-FE-8-2** | test 환경 실 GW 핵심 여정 e2e | ✅ MSW 대체 커버 + 대체 스펙 문서화 | **test 환경**(선결#5) · CORS(C-3) · T-FE-8-1 | ③-I |
      | **T-FE-9-17** | 목↔**실 GW** 응답 대조(2단계) | ✅ 목↔**계약** 대조 회귀 검사·갭 2건 수정(#13057) | **dev 재배포·재시드 + admin consent**(admin dev 9/10 = 401 부팅·8/31 503 해소) | ③-I |
      | **T-FE-8-4** | prod 배포 | ✅ 프리뷰 배포 파이프라인(S3+CloudFront) | **prod 도메인**(C-10) · ⚠ **무인 대상 제외**(사람이 실행) | PL/③-I |
      | **T-FE-7-6** | 배포 헤더(CSP·nosniff·Referrer-Policy·HSTS) | ✅ **8/26 실측 — 전부 부재**(`curl` 로 판정·사람 불요) | **CloudFront response headers policy 미배선** | ③-I |
      - 🔴 **최우선 블로커**
        - **① Entra admin consent 승인** — 9/9 앱 회신 · IT-9442 · consent 미승인. admin API 는 9/10 부팅 확인(401). **Console 실로그인이 막혀 dev 실검증이 통째로 정체.**
        - **② dev 재배포·재시드** — 계약(운영자 요약 · clinic 임베드 · config device-facing)은 **양쪽 다 머지됐는데 dev 에 안 떠 있어** 실화면 확인이 불가.

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
  | 16 | **`GW_BOOTSTRAP_ADMIN_EMAILS` 경로 정정 + admin 재시작** — 값이 `/dev/vt-api-gateway-console/config`(프론트 빌드용)에 들어가 **admin 이 못 읽는 상태**(9/10 실측). `/dev/vt-api-gateway-admin/config` 로 이동 후 **파드 재시작** 필요(env=부팅 시 1회 로드·SRS §7.8.4) · 미조치 시 로그인 후 `no_access` | ③-I | ✅ **완료(9/10·Jack)** | ☐ |
  | 17 | **SSM `config` 값을 한 줄 JSON 으로 재기록** — 여러 줄(pretty-print)이라 CI 로더가 첫 줄에서 끊겨 **에러 없이 exit 1**(9/10 진단). 값만 고치면 재발하므로 **넣는 도구가 `jq -c` 를 쓰는지** 확인 필요 · 겸하여 `es-ci-templates/load-envs-step.yml` 의 **에러 출력 `>&2`**(현재 `$( )` 가 삼켜 **어떤 실패든 침묵**) 및 `--output json`+`jq` 파싱 전환 | ③-I | ✅ **완료(9/10·Jack)** · **템플릿 보강도 반영 확인(9/14)** | ☐ |
