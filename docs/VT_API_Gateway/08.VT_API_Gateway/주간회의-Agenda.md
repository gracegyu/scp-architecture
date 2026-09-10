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
    - **[R1 실행 — GW·Console × DT·SonarQube 온보딩] ✅ 완료(9/10)** ⭐ _(회의 결정 직후 당일 완료·Jenkins 세션)_ — **4 커버리지(GW·Console × DT·SonarQube) 전부 실데이터 확인·Quality Gate 둘 다 Pass**.
      - **결과**: DT SBOM components GW **424**·Console **260**(CycloneDX 1.6) · SonarQube GW **17.5k LoC·버그5·취약점0·hotspot21**·Console **24.2k·버그5·취약점0·hotspot15**. ⚠ **커버리지 0%**(파이프라인이 테스트 미실행) → 잡에 test+coverage 추가할지 **별도 논의**.
      - **부수 성과(전 제품 해당)**: `python/sbom_extractor.py`의 **잠복 버그 5건 발견·수정**(DT/ABS 업로드·trivy 실패의 **종료코드 삼킴**→빌드 SUCCESS인데 DT 비어 있던 것·불완전 SBOM 업로드·POSIX rmtree) — Windows 에이전트에선 안 드러나다 Linux 이관서 노출. **종료코드 불신·DT 직접 조회 Verify Upload 스테이지 추가**. + trivy 0.71+가 CycloneDX 1.7 산출→DT 4.13.3(1.6까지)이 400 거절 → **trivy 0.70.0 고정**(DT 업그레이드 불요). 상세=`sbom/jenkins` repo.
      - **만든 것**(`sbom/jenkins`·main): `vars/sharedPipelineSbomPyLinux.groovy`(신규·Node/pnpm Linux) · jenkinsfile 4종 · config 2종 · Node 샘플 템플릿 2종. (pnpm은 기존 `-py`(python) 계열이 이미 지원 — Groovy Node 템플릿 신설 불요로 판명. `-py`가 Windows였던 건 EzServer가 Windows 대상 SW라서·VT는 Linux 대상.)
      - **남은 것 = 없음(완결).** 트리거는 **초기 'QA 태그' 안 철회 → 일 1회 새벽 스케줄로 확정**(Raymond·9/10) — 기존 잡들과 동일 **pollSCM**이라 ADO 연동·API 토큰·변수그룹 불요. 4잡 KST 새벽 2~5시 분산(commit `40986aa`·Verify Upload 통과). **별도 논의 = 커버리지 0%**(잡에 test+coverage 붙일지·Raymond "필요성 추가 논의").
      - ⚠ **부수 발견(별건·Jenkins 세션 처리)**: `jenkins-server` 컨테이너 **TZ 미설정(UTC)** → 기존 잡 13개 크론이 의도와 달리 **업무시간에 돔**(예 SBOM `H 3`=KST 정오·CI와 에이전트 경합·eslockserver #18이 12:19 KST 실행이 증거). 급하지 않아 별건(TZ=Asia/Seoul은 전체 9h 시프트라 신중)·회의 안건 아님. VT 4잡은 UTC 환산해 실제 새벽 실행.
    - **[최초 admin 부트스트랩 allowlist]** ✅ **구현 완료(9/10·PR #14212 머지)** — Console 실 로그인(9/10) 후 PL이 부딪힌 **"최초 admin 데드락"**(승인할 admin이 없음) 해소. env `GW_BOOTSTRAP_ADMIN_EMAILS`(첫 로그인 JIT admin 자동 부여·요청→승인 생략·매칭=이메일·저장=oid·멱등·비회수·≥2명) 계약을 SRS §7.1.4·§7.9.2·env-reference §2.3에 pin(**spec PR #14204·`spec-v1.0.85`**·Jack 승인·main) + **tenant 제약 보강**(`spec-v1.0.86`: allowlist 설정 시 `GW_OPERATOR_OIDC_TENANT` 필수·타 테넌트 권한상승 차단 — 코드 fail-closed는 #14212로 main·**문서 v1.0.86은 Raymond 리뷰 대기·pending**). **코드**(`OperatorBootstrapService`·admin JIT 경로·PR #14212): unit·e2e(데드락 해소·멱등·대소문자·비-allowlist 403) green·독립리뷰 🟢·보안 M1(테넌트 fail-closed)/M2(감사 loud) 반영. **부수**: 신규 org-wide `multer` HIGH CVE로 dep-scan 게이트가 전 PR 차단 → surgical override PR #14220(`multer ^2.3.0`) 먼저 머지해 언블록. 다운스트림 = **③-I(Jack) Parameter Store 에 `GW_BOOTSTRAP_ADMIN_EMAILS`+`GW_OPERATOR_OIDC_TENANT` 주입**. 즉시 언블록은 `dev:operator --sub <oid> --role admin`(로컬).
    - **[GW dev 배포·통합]** core·receiver·dispatcher·**admin 전부 dev 기동 확인**(9/10: admin `/v1/admin/me` 401=healthy·8/31 503 해소) · 통합은 Entra admin consent 승인 후 실로그인부터(③-I #3)
    - **[GW Console 통합]** 실 dev GW + Entra 접목 · 완료 화면 포함 정합성 확인 마무리
      - ⭐ **`T-FE-8-1` 로컬 검증 통과(9/10)** — admin consent 승인(IT·9/10) 후 **실 Entra 로그인 → 토큰 → GW admin 응답**까지 성공. `issuer`·`aud`·`scp` 가 전부 맞다는 것이 통과 자체로 증명됨(이전 401 은 GW `.env` 가 로컬 OIDC 스텁을 보던 것) · **최초 admin 도 allowlist 로 자동 부여 확인**
      - ⚠ **dev 배포는 아직 목(mock)** — 실 Entra 빌드가 **SSM 로드에서 3중 결함**으로 막힘(아래 별도 항목) · **`ⓒ dev redirect URI` 등록 여부는 배포해야 실측**(미등록이면 AADSTS50011)
      - ✅ **로그인 무한 반복 해소**(PR https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14229 머지) — **401 → logout → `/login` → SSO 세션으로 조용한 재로그인 → 같은 토큰 401** 의 고리. 자동 시도를 60초 3회에서 끊고 사유를 보여 준다(수동 재시도는 유지) · 카나리 검증
    - **[Entra 앱 등록]** dev 2앱 회신 완료(9/9) · **admin consent 승인 완료(IT·9/10)** ✅ — 로컬 실로그인으로 검증됨. **`aud` 형식 확정**: dev SSM 은 `api://<GUID>`, GW admin 은 bare `<GUID>` 로 **표기가 다르나 둘 다 Entra 표준**(스코프는 `<audience>/.default`) · 배포 후 로그인 실패 시 첫 용의자로 둔다
    - **[Console dev 실배포 blocked · SSM 3중 결함]** ⚠ **9/10 진단 완료 · 조치 대기** — 실 Entra 빌드가 `Load env from SSM` 에서 **에러 한 줄 없이 0.5초 만에** 죽어 두 번 실패(https://dev.azure.com/ewoosoft/es-platforms/_build/results?buildId=55466 · https://dev.azure.com/ewoosoft/es-platforms/_build/results?buildId=55475). 파이프라인에 진단 스텝을 넣어 원인을 갈라냄 — **IAM·KMS·jq 는 전부 무관**(같은 잡·같은 `dev-ci` 역할에서 `--with-decryption` 조회가 `rc=0`)
      - **① SSM 값이 여러 줄(pretty-print) JSON** — 로더가 `이름<탭>값` **한 줄**을 가정해 `read` 가 첫 줄에서 끊기고 `jq` 가 `{` 하나를 받아 실패. **③-I 조치**(한 줄 JSON 재기록 + **넣는 도구가 `jq -c` 를 쓰는지** 확인 — 값만 고치면 재발)
      - **② 에러가 구조적으로 침묵** — `emit_env` 가 에러를 **stdout** 으로 내보내는데 호출부가 `body="$(emit_env …)"` 라 `$( )` 가 삼켜 로그에 안 찍힘. **어떤 실패든 무조건 침묵**하는 구조 · `>&2` 한 줄이면 해소 · 근본은 `--output text` 대신 `--output json`+`jq`(값에 개행이 하나라도 있으면 같은 방식으로 또 깨짐) — **`es-ci-templates` 조치**
      - **③ `.env` 출력 경로가 한 겹 중복** — `Build.SourcesDirectory` 가 이미 레포 폴더를 포함하는데 접두를 붙여 둠 · ①②를 고쳐도 다음 게이트(`test -s .env`)가 실패 · **Console 조치**(PR https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14233)
      - ⚠ **별건 · ③-I 조치 대기**: `GW_BOOTSTRAP_ADMIN_EMAILS` 가 **`/dev/vt-api-gateway-console/config`(프론트 빌드용)에 들어가 admin 이 영영 못 읽는 상태** → `/dev/vt-api-gateway-admin/config` 로 이동 **+ admin 파드 재시작**(env 는 부팅 시 1회 로드 · SRS §7.8.4). 미조치 시 로그인은 되고 `no_access` 로 떨어진다
    - **[운영자 매뉴얼 · 최초 관리자]** ✅ **작성 완료 · 스펙 검토 통과**(PR https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14234) — *"첫 admin 은 누가 승인하나"* 에 매뉴얼이 답이 없던 구멍. 케이스 E 신설(승인 없이 부여·TOFU 아님·멱등·비회수·재로그인 복원·**2명 이상 권장**·감사에 `system`) · 트러블슈팅 3줄(승인할 관리자 없음 / **재시작 누락** / **테넌트 값 누락 시 admin 부팅 거부**·spec-v1.0.86) · 배포 주입 절차는 ③-I 소관이라 **일부러 미기재**
    - **[제품 연동 스펙]** EzServer OnePager 수령 확인(잔여)

  - **이번 주 결정사항 (9/10 회의)**
    - **R1 (SBOM/보안 파이프라인)**: ③ **GW+Console 둘 다** 온보딩 · **DT/SBOM + SonarQube 둘 다**(SQ를 후속→**병행 상향**) · 트리거 = **일 1회 새벽 스케줄**(초기 'QA tagging' 안은 ADO/토큰 비용 커 **철회**·pollSCM). **당일 완료(9/10·Jenkins 세션)** → 위 「이번 주 진행」 참조. 실행=Raymond 지시.
    - **Entra**: prod 등 **전 환경 앱을 미리 요청**(임건혁/Jack) — 단 **domain 확정 선행**(김성훈/Scott).
    - **DT·SonarQube의 cloud 이전**(비용·방안) 추가 검토 — 급하지 않음(임건혁/Jack).

- 논의 사항 (이번 주 · 신규 · R#)
  - _(9/10 신규 안건 없음 — R1 결정 완료→「이번 주 진행」으로 이동. 신규 발생 시 R2·R3…)_

- **[③-I Jack 인프라 요청 추적]** — 회의에서 상태·ETA 확인. **✅ 9/3 대거 착지(Jack): 실 IoT Core·Parameter Store(compat well-known 200)·KMS CMK(payload+target)·공개 ingress = dev 완료** · admin 부팅(401)·Entra 앱 회신(9/9)까지 겹쳐 **dev 인프라 핵심이 대부분 해소**됨(남은 dev 블로커 = Entra admin consent·자동배포·마이그Job·dispatcher 안정화·test 환경). 상세=`docs/handoff/pending-infra-requests.md §9`. (PR: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/12653)

  > 범례: ✅ 완료(괄호=완료일·날짜만이면 **이전 주 완료**) · **🆕 = 이번 주(9/11 이후) 신규 해결·검증 — (아직 없음)** · 🟠 부분 · ☐ 미완 · ⚠ 전달 필요. _(9/10 주 현실화분 반영: pending-infra §9 Jack 9/3 실측 + dev 엔드포인트 재확인.)_

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

  > **[③-I 요청 전달 감사 — 2026-08-26]** "문서에 선결로 적혀 있다 ≠ Jack에게 전달됨." 두 추적 표를 훑어 GW handoff 7종 전부 **결과 Form·전달 흔적 0** 확인(작성 ≠ 전달). 전달 흔적 없는 항목(③-I #8·GW선결 #1·#2·#4 + Console CloudFront 헤더 4-tier·사내 접근제한[8/19 회신서 누락 변종])을 **handoff + 결과 Form 단일 전달 패킷**([pending-infra-requests.md](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/handoff/pending-infra-requests.md&version=GBmain)·GW repo·초안)으로 묶음. **전달 주체 = Raymond**(PL 지시). 이후 모든 ③-I 요청은 handoff+Form으로 전달하고 회신을 이 표에 일자·산출물로 기록(재발 방지). 모범 = 마이그레이션 인계(#13020).

- 공유 사항 (결정 아님 · 논의사항인지 애매한 것을 임의 결정해 공유 · 매주 상시)
  - **S1. 프로젝트 일정(Gantt) — 9/10 스냅샷(현실화)**
    - **진행률(구현)**
      - **GW ≈ 93%** — v1.0 계획 기능 코드 완결(8/24 feature-complete) · 잔여=dev 통합(Entra·③-I 인프라)
        - 잔여 = ③-I 실 인프라 게이트 · 개발 통합검증 · 계약 경화(OpenAPI 코드-first 일원화)
      - **GW Console ≈ 92%** (8/26 재평가) — Task **61/67 완료** · 부분 4 · 미착수 2
        - 잔여 **6건이 전부 외부 선결** — Console 코드로 앞당길 잔여 **0**
        - 성격이 셋으로 갈린다:
          - **통합 검증 3** — `T-FE-8-1`(실 Entra 로그인 왕복) · `T-FE-8-2`(실 GW 여정 e2e) · `T-FE-9-17`(목↔실 GW 응답 대조)
          - **남의 작업 2** — `T-FE-7-6` CloudFront 헤더 **배선**(③-I) · `T-FE-8-4` prod **배포**(PL 실행)
          - **내부 조사 1** — `T-FE-9-13` 플레이크(가설 확보·**다음 발생 대기**)
        - ⚠ **"검증이니 곧 끝난다" 로 읽으면 안 된다.** 검증의 목적은 어긋난 것을 찾는 것이고, **찾으면 그게 Console 작업이 된다.** `T-FE-9-17` 은 **1단계(목↔계약)만으로 갭 2건**이 나왔다(`FleetState.clinicId` 누락 · `Device.createdAt/updatedAt` 부재). 2단계는 **실 GW 응답**과 맞추는 것이라 더 나올 수 있다 — 화면은 목만 보고 개발됐고 **목은 실물보다 관대했다**(지금까지 난 결함의 절반이 그 구멍에서 나왔다). Entra 도 claim→역할 매핑·딥링크 왕복(`?to=` 쿼리 보존)을 **소스로만 확인했고 한 번도 밟아 본 적이 없다.**
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
      - **최우선 블로커(회의에서 밀 것)**: ① **Entra admin consent 승인**(dev 2앱 회신 9/9·IT-9442·**admin API는 부팅됨**[9/10 401]·**consent 미승인**이라 Console 실로그인 불가) → **dev 통합검증 정체** · ② **test 환경 프로비저닝**(선결#5·마감 8/26) — 부하·HA 2건 동시 해제. **PL 결정 대기 = RTO/RPO 목표**(HA 합격기준). **GW 코드/설정 잔여 = 0**(마이그레이션·ECR·파이프라인까지 완료).
      - 🟢 **지금 착수 가능(9/3 ③-I 인프라 풀림) — IoT 다운링크 E2E**(T-DISP-9-5·T-E2E-12-6): **③-I 대기 아님·GW 몫**. 경로는 스펙 정의(토픽 `gw/clinic/{clinicId}/#`·`MQTT_URL`/`IOT_ENDPOINT`·ShareName `ezserver`). 순서 = ① **dispatcher exit137 원인규명·해소** → ② **device Thing enroll 1건** → ③ **webhook→IoT Core→EzServer 다운링크 E2E 1회**. 실행 주체=**구현 세션**.
        - **9/10 직접 실측(스펙 세션·read-only)**: `aws iot list-things`=**0**(enroll된 Thing 없음 실증) · dev IoT 엔드포인트 `a2ig1yuqacb8gl` 일치.
        - ⚠ **접근 경계**: dispatcher 파드(exit137) 진단은 **dev EKS 접근** 필요인데, 내 자격 계정(IoT는 보이나 **EKS 클러스터 0**)에 안 보임 → **Jack에 dev EKS 접근 개방 요청** 또는 **dev 접근 보유 구현 세션**이 `kubectl describe/logs`로 원인(OOM=리소스→③-I / 코드→GW) 특정.
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
      - **최우선 블로커**: ① **Entra admin consent 승인**(9/9 앱 회신·IT-9442·consent 미승인·admin API는 9/10 부팅 확인 401) — Console 실로그인이 막혀 dev 실검증이 통째로 정체 ② **dev 재배포·재시드** — 계약(운영자 요약·clinic 임베드·config device-facing)은 **양쪽 다 머지됐는데 dev 에 안 떠 있어** 실화면 확인이 불가.

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
  | 16 | **`GW_BOOTSTRAP_ADMIN_EMAILS` 경로 정정 + admin 재시작** — 값이 `/dev/vt-api-gateway-console/config`(프론트 빌드용)에 들어가 **admin 이 못 읽는 상태**(9/10 실측). `/dev/vt-api-gateway-admin/config` 로 이동 후 **파드 재시작** 필요(env=부팅 시 1회 로드·SRS §7.8.4) · 미조치 시 로그인 후 `no_access` | ③-I | ☐ **요청(9/10)** | ☐ |
  | 17 | **SSM `config` 값을 한 줄 JSON 으로 재기록** — 여러 줄(pretty-print)이라 CI 로더가 첫 줄에서 끊겨 **에러 없이 exit 1**(9/10 진단). 값만 고치면 재발하므로 **넣는 도구가 `jq -c` 를 쓰는지** 확인 필요 · 겸하여 `es-ci-templates/load-envs-step.yml` 의 **에러 출력 `>&2`**(현재 `$( )` 가 삼켜 **어떤 실패든 침묵**) 및 `--output json`+`jq` 파싱 전환 | ③-I | ☐ **요청(9/10)** | ☐ |
