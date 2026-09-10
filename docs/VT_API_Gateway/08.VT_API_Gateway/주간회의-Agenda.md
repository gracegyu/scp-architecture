# VT API Gateway — 9/10 주간회의 Agenda

> **과거 주차(~8/27)는 [`주간회의-Agenda-Archive.md`](주간회의-Agenda-Archive.md)로 이관·보존**(조회용). 본 문서는 **9/10 현행 주차만** 유지한다. 틀(논의/공유/이월)·Gantt(S1)·스펙표(S2)는 매주 상시 포함.

- **이번 주 진행 (~9/10 회의) — 이번 주 완료·진행한 실제 작업**
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

  - **완료 · 주요 작업**
    - **[Console 운영 매뉴얼 8종 작성 완료]** ⭐ _(지난 회의 종료 후 마무리)_ 운영자용 **한국어 운영 매뉴얼 8종 작성 완료** — 운영자가 GW Console을 보고 따라할 수 있는 사례 주도·따라하기·트러블슈팅 문서.
      - 연동 대상(target) 등록·관리 · org 매핑 관리 · 디바이스 온보딩·관리 · webhook 이벤트 조회·장애 대응 · 운영자·권한(RBAC) · 클리닉 조회·식별 메모 · 중앙 설정(config) · 감사(audit) (+ 매뉴얼 인덱스)
    - **[운영 매뉴얼 Project wiki 발행 완료]** ✅ GW·Console 운영 매뉴얼(`docs/manual`)을 스펙(`docs/specs`)과 함께 es-platforms **project wiki로 자동 미러**하도록 발행 파이프라인(`docs-wiki.yml`) 확장(PR #14130·#14132 머지·발행 완료) — **Git 접근·라이선스 없는 기획·PM·품질팀도 위키에서 바로 열람** 가능.
      - **위키 링크**: [Console 매뉴얼 폴더](https://dev.azure.com/ewoosoft/es-platforms/_wiki/wikis/es-platforms.wiki?pagePath=/vt%20api%20gateway/03c%20subsrs%20gw%20console/manual) · [GW 매뉴얼 폴더](https://dev.azure.com/ewoosoft/es-platforms/_wiki/wikis/es-platforms.wiki?pagePath=/vt%20api%20gateway/manual)
      - GW 매뉴얼 → `vt api gateway/manual/`(최상위) · Console 매뉴얼 → `03c subsrs gw console/manual/`(Sub-SRS와 나란히·SSOT=console repo에서 pull). 매뉴얼은 스펙과 달리 **이미지도 함께 게시** · 정본 변경 시 **자동 재발행**(교차 트리거).
      - **상호 크로스링크**: GW `target-onboarding`(API·인프라 크로스팀 runbook) ↔ Console `target-management`(UI 운영자 가이드). 검토 결과 **독자·계층이 달라 통합하지 않고 둘 다 발행**, 대신 서로 참조 링크를 걸어 계층 구분.
    - **[CI 셀프호스티드(Self-hosted1) 전환 — 공유 풀 적체 해소]** ⭐ 공유 CI 풀 대기 적체로 GW·Console CI가 정체 → **사내 self-hosted 빌드로 전환**.
      - **전환·적용**: 에이전트 재구축(docker buildx·AWS CLI·Playwright·trivy·gitleaks 내장) · 스모크 검증 · 중앙 CI 템플릿에 pool 파라미터 추가(Jack repo·머지). GW root CI·Console CI·devsecops에 적용(범위 = PR·머지 회전에 직접 영향 있는 것 위주).
      - **효과**: CI 회전 대폭 단축 — **GW CI 총 23.8분 → 3.3분**(큐 대기 소멸 + 실행시간 단축).
      - **OOM 사고·대책**: 전환 직후 공용 빌드 서버가 메모리 고갈로 먹통 → 원인 = 테스트 러너 워커 자동 증식 × 에이전트 4대. 대책(테스트 워커 상한 · 컨테이너 메모리 상한 · 불용 VM 종료)으로 **해결·구조적 재발 방지**(리부팅 후 유지).
      - **공용 빌드 서버 Jenkins 복구 · Java 21 이관 · 정리**: OOM 대책 때 종료한 win10 VM이 **Jenkins Windows 노드(Windows 제품 SonarQube 스캔)** 도 겸하던 것을 확인해 VM을 재기동하는 과정에서, **Jenkins 마스터의 잠복 문제**(플러그인은 최신인데 마스터가 오래 재시작된 적 없어 옛 버전으로 구동 중이던 상태)가 드러나 재시작 시 부팅 실패 → 복구 + 밀린 유지보수(Java 21)·정리까지 완결.
        - **복구**: 최신 플러그인이 요구하는 코어로 올리면 에이전트(Java 17)가 못 붙고, 옛 코어로 두면 플러그인이 안 뜨는 딜레마 → 우선 **Java 17 마지막 LTS(2.541.3)** 로 코어를 맞추고 일관된 플러그인 세트로 재구성해 복구.
        - **메모리 캡 정비(재발 방지)**: 그간 캡이 CI 에이전트에만 걸려 있고 Jenkins·SonarQube·Dependency-Track은 무제한이던 것을 확인 → **전 서비스에 메모리 상한 적용**(한 서비스 폭주가 서버 전체를 죽이지 못하도록).
        - **Java 21 이관(EOL 스택 해소)**: Java 17이 Jenkins 기준 **이미 EOL(2026-03-31)**이라 임시 고정점(2.541.3)에 머물지 않고 이관 — **에이전트(Linux 4대 재빌드·Windows는 JDK 23) 먼저 → 마스터 최신 LTS 2.568.3(Java 21) 상향**(순서 지켜 무탈 정렬). 마스터·에이전트 전부 Java 21.
        - **플러그인·보안 정리**: 2.568.3용 최신 세트 재해석(0 실패)·**보안 패치 `pipeline-groovy-lib`(CSRF·SECURITY-3815) 적용** · deprecated **Blue Ocean 계열 20개 제거**(개발 중단·UI 레이어라 빌드 무관·디자인 라이브러리 포함·137→117) · **위험 스크립트 승인 제거**(`GroovyObject.invokeMethod`=샌드박스 우회).
        - **결과**: 마스터·에이전트 전부 **Java 21**·**빌드 노드 6개(Linux 4 + Windows 2) online**·플러그인 **0 실패·deprecated 0·보안 갱신**·SonarQube/Dependency-Track 정상·메모리 안정. 상세 = `references/Self-hosted1/99.2`.
        - **후속(내년) — Java 25 이관 필요**: Jenkins "2+2+2" 정책상 Java 21도 최소 요구로 **약 18개월**(~**2027년 하반기** Java 25로 전환·Java 21 지원 종료 전망). **내년에 Java 25로 올려야 함** — 이번과 동일 절차(에이전트 먼저 → 마스터)라 수월, EOL 전 제때 계획(이번처럼 밀리지 않게).
      - **보안 스캔 구조 개선 ✅ 완료**: devsecops가 앱 4개에서 같은 스캔을 4번 중복 + 취약점 DB를 매번 외부(gcr.io)서 받다 실패하던 문제 →
        - **소스·시크릿 스캔을 CI verify로 일원화**(trivy fs · gitleaks · SBOM · PR당 1회) → devsecops 5종은 스캔 OFF(빌드/배포만) = **4중복 제거**.
        - **스캐너 자동 관리(핵심)**: trivy·gitleaks를 에이전트 이미지가 아니라 **사내 공유 볼륨(`/opt/trivy-cache/bin`)에 별도 설치** —
          - **버전 자동 업데이트**: 새벽 cron이 **하루 1회 최신 버전으로 자동 갱신**(smoke-test·실패 시 옛 버전 유지) → 버전업에 이미지 재빌드·에이전트 재설치 불요.
          - **취약점 DB도 하루 1회 갱신**(gcr.io 접속은 그때만) → CI는 `--skip-db-update`로 **완전 오프라인**(매 실행 gcr.io 다운로드 실패[flaky] 원천 제거).
        - **SBOM 생성**(CycloneDX/SPDX·아티팩트) — DT 업로드는 후속(DT 사내망이라 CI서 직접 불가 · Jack의 pipeline→S3→BM2 폴링→DT 방안 확정 후 배선).
        - 중앙 CI 템플릿 스캔 토글 = Jack 머지. 상세 = `CI-DevSecOps-SelfHosted/`.
        - **후속/미결**: ① DT SBOM 업로드 배선(Jack S3 계획 후) · ② install 네트워크 flake(호스트 egress 불안정·prisma/cpu-features/gcr.io/git·재실행 우회·호스트 안정화는 별도) · ③ enforce(hard gate) 전환은 별도 결정.
    - **[Jenkins 파이프라인 무한 hang 진단·차단(timeout 전면 도입)]** ⭐ `dart-Linux-SonarQube` 빌드 2건이 "Setup Flutter"에서 **30시간·6시간째 안 끝나고** executor를 점유(빌드 노드 4대 중 2대)하던 것을 발견·분석.
      - **원인 2겹**: ① **Jenkins 기본 빌드 타임아웃이 없음** + 이 파이프라인들에 `timeout`이 전무 → 멈춰도 무한 대기. ② `flutter pub get`이 **비공개 Azure DevOps git 의존성**(`common-dart/ezwebserver-client`)을 clone하는데 **자격(PAT) 미주입**으로 auth 실패 → dart pub이 이를 일시장애로 오인해 **무한 재시도**(retry 1611회·64초 간격 ≈ 28h, 경과와 일치).
      - **조치**: **공유 파이프라인 라이브러리(`vars/` 9종)에 스테이지 timeout 일괄 도입**(기본 60분·`STAGE_TIMEOUT`로 오버라이드) → samples 6 + jenkinsfiles 11(oneid·ezcloud·eslockserver·EzServer 등) + 미래 잡까지 **한 곳 수정으로 전부 hang 방지**. Dart Linux `setupFlutter`에 **`azure-devops-pat`를 GIT_ASKPASS로 주입**(근본 수정·전역 git에 시크릿 미잔류). hung 빌드 2건은 콘솔에서 abort.
      - **비고**: PAT는 유효(메인 체크아웃엔 이미 사용)라 **재발급 불요** — pub get에 안 실리던 것만 수정. 남은 것 = Dart 잡 1회 실행 green 검증 · DartWin(Windows·bat) 동형 수정. jenkins repo(`sbom/jenkins`) 소유=Raymond.
    - **[dispatcher dev 부팅 장애 해소 + IoT Core 발행 인증 확정]** ⭐ dev dispatcher가 부팅을 못 하고 5분마다 죽던 문제를 해소하고, IoT Core로의 이벤트 발행 인증 방식을 확정.
      - **원인**: dev의 MQTT 엔드포인트가 IoT Core(WSS)인데 dispatcher가 무인증 로컬 MQTT로 붙어 IoT Core가 접속을 끊음 → 무한 재접속으로 부팅이 멈춤(KEDA 최소 replica를 0→1로 올리며 드러남).
      - **해결**: dispatcher가 IoT Core에 **SigV4 서명 WSS·IAM(Pod Identity)** 로 접속·발행하는 어댑터 추가 + 최초 접속 타임아웃(fail-fast). Jack 제안 PR 머지로 dev 언블록.
      - **인증 방식 정리**: **발행자(GW)=IAM/SigV4** vs **구독자(EzServer)=디바이스별 인증서** 로 역할 구분. 어댑터 선택은 env `MQTT_AUTH`(auto·sigv4·none·기본 auto)로 확정 — dev/prod는 자동 SigV4라 추가 설정 불요.
      - **스펙 정합**: SRS §7.6.6·env-reference 반영(spec-v1.0.84 머지). 명시 MQTT_AUTH 전환 PR **머지 완료(#13585·9/3)**.
      - ⚠ **남은 dev 이슈(부팅과 별건)**: dispatcher 파드 **exit137 반복**(9/3 pending-infra 관찰·OOM/kill 추정) + **enroll된 Thing 0건** → **IoT 다운링크 E2E 미실행**(T-DISP-9-5·T-E2E-12-6). SigV4 부팅 수정과 별개 문제라 **9/10 재확인·안정화 필요**(IoT 인프라는 9/3 완료).
    - **[Entra dev 회신값 접목 착수 — IT-9442]** ⭐ IT팀이 dev 앱 2개(API 리소스·Console SPA)를 등록·회신(9/9). Jack이 값을 문서에 반영(PR #14162 머지)하고 **dev 실 로그인 배포 경로**를 파이프라인에 추가(#14167·기본은 목 유지·`devAuthMode=entra` 수동 실행). Console은 회신값으로 **로컬 실 로그인을 시도해 남은 항목을 실측 판정**했다.
      - **판정된 것** — 테넌트·issuer·JWKS가 discovery 문서와 **일치** · SPA client ID·`localhost:3100` redirect **등록됨** · scope `access_as_operator` **노출됨**(동의 화면 도달이 그 증거)
      - ⚠ **남은 잠금 = admin consent 1건** — 미승인이라 사용자마다 승인 요청 화면이 뜬다. **조직 단위 1회**면 되고 이후 사용자는 동의 화면을 보지 않는다(Console 역할 부여와는 **다른 계층**). IT팀(이희선)에 요청 전송
      - ⚠ **환경별 등록마다 consent 1회 필요** — prod 등록 시 같은 작업이 반복된다(사전 공유)
      - **`aud` 형식 미확정** — v2 토큰이면 GUID 단독, v1이면 `api://<GUID>`. 검사기는 `api://` 만, GW dev 주입값은 GUID로 **서로 반대를 가정**하고 있었다 → 검사기가 **둘 다 통과**시키되 *두 등록 혼동*은 계속 잡도록 수정(#14168 머지). **실토큰 한 장으로 확정**할 판독 도구도 함께 넣었다
      - **Console 버그 1건 발견·수정(#14169 머지)** — 로그인 리다이렉트가 한 번 끊기면 `interaction_in_progress` 로 **이후 로그인이 영영 막혔다**(탭을 닫기 전엔 회복 불가). `handleRedirectPromise()` 를 콜백 화면에서만 불러 생긴 문제로, 초기화 시 한 번 정리하도록 고침. **실 로그인을 시도하지 않았으면 안 드러났을 결함**
      - **#14167 리뷰** — 설계는 타당(실 빌드에도 `verify:bundle` 적용·`.env` 사전 정리·같은 버킷 상호배제). ⚠ **차단 1건**: 정적 export 플래그 누락으로 `out/` 이 안 만들어져 **빌드는 초록·배포에서 실패**한다(로컬 재현 완료). 리뷰 문서 `03c-subsrs-gw-console/_review-console-ci-14167.md` 로 남기고 PR 코멘트 게시

  - **진행 중 · 선결 대기**
    - **[GW dev 배포·통합]** core·receiver·dispatcher·**admin 전부 dev 기동 확인**(9/10: admin `/v1/admin/me` 401=healthy·8/31 503 해소) · 통합은 Entra admin consent 승인 후 실로그인부터(③-I #3)
    - **[GW Console 통합]** 실 dev GW + Entra 접목 · 완료 화면 포함 정합성 확인 마무리
      - ⚠ **`T-FE-8-1`·`T-FE-9-17`의 한 뿌리 = admin consent** — **admin API는 부팅됨**(9/10 `/v1/admin/me` **401**=healthy·OIDC 설정 주입으로 이전 503 해소) · 남은 건 **admin consent 미승인**이라 Console 실로그인(토큰 취득)이 막혀 두 검증이 정체 · consent 풀리면 **함께** 풀린다
    - **[Entra 앱 등록]** dev 2앱 **회신 완료**(9/9) — 남은 것은 **admin consent 1건**(IT팀 승인 대기). 승인 즉시 `T-FE-8-1` 로컬 검증 착수 · `aud` 형식도 그때 확정
    - **[제품 연동 스펙]** EzServer OnePager 수령 확인(잔여)

  - _(이번 주 결정사항 = 회의 시 추가)_

- 논의 사항 (이번 주 · 신규 · R#)
  - **R1. GW·GW Console을 Jenkins 보안 파이프라인에 온보딩할지 결정** — 다른 사내 제품(eslockserver·ezcloud·oneid 등)은 Jenkins에서 **① SBOM 생성→Dependency-Track 업로드**, **② SonarQube 정적분석**을 돌리는데 GW·GW Console은 미연동. Jenkins가 복구·최신화됐고 **DT와 같은 내부망**이라 지금 붙이기 좋음.
    - **① SBOM→DT**: 기존 템플릿(`sharedPipelineSbomGitNodeLinux`) 재사용 — DT 프로젝트 생성 + jenkinsfile/잡 추가로 GW·Console 의존성 취약점을 DT에서 상시 추적. **Azure CI가 못 하던 내부 DT 업로드를 Jenkins가 직접 수행** → 기존 "Azure CI→S3→폴링→DT" 후속안을 대체·단순화.
    - **② SonarQube 정적분석**: 기존 SonarQube 템플릿 재사용(코드 품질·SAST). GW는 현재 Azure CI에 SonarQube 미연동.
    - **결정 (두 축 · ✅ = 추천)**:
      - **(A) 제품 범위**
        - ① 안 함
        - ② GW만
        - **③ GW + Console ✅**
      - **(B) 도구**
        - **DT / SBOM ✅ — 먼저(필수급)**
        - SonarQube / 정적분석 — 후속·선택
        - (지향점 = 둘 다)
    - **추천 근거**:
      - **SBOM은 사실상 필수** — FDA 시판전 사이버보안(cyber device·FD&C §524B) 제출 의무 + IEC 62304 SOUP(외부 구성요소) 관리 근거. GW는 이미 Azure CI가 CycloneDX SBOM 생성 中이라, Jenkins/DT 추가분은 **취약점 상시 추적·시판후 모니터링**.
      - **GW+Console 둘 다** — 둘 다 IEC 62304/ISO 13485 통제 대상(Console은 PHI 취급)이라 규제 범위에 함께 들어갈 공산이 큼. **누락 리스크 > 추가 비용**이고 템플릿 재사용이라 저비용 → 안전하게 둘 다.
      - **SonarQube는 후순위** — secure SDLC 근거로 유용하나 SBOM 같은 명시 의무 산출물은 아님 → DT 먼저, 여력 시 추가.
      - **①·② 비추천** — 안 하면 인증 요구 시 급히 붙여야 하고, GW만 하면 Console이 제출 범위일 때 재작업.
    - **⚠ 최종 확정은 규제 확인 후**: SRS §6.13이 "인증 준비물은 마케팅·품질팀이 확정"(Appendix B #11)이라 명시 → **품질/RA팀에 ①SBOM/정적분석 요구 여부 ②범위(GW/Console) 확인이 선행**. 확인되면 추천안대로, 요구 아니면 축소·보류. 기술 준비(pnpm 대응·jenkinsfile·잡)는 결정 후 착수(저비용).
  - _(회의 중 신규 논의/결정 안건 발생 시 **R1·R2…** 로 추가 · 선결·보류는 아래 「이월 논의 사항」 표.)_

- **[③-I Jack 인프라 요청 추적]** — 회의에서 상태·ETA 확인. **🆕 9/3 대거 착지(Jack): 실 IoT Core·Parameter Store(compat well-known 200)·KMS CMK(payload+target)·공개 ingress = dev 완료** · admin 부팅(401)·Entra 앱 회신(9/9)까지 겹쳐 **dev 인프라 핵심이 대부분 해소**됨(남은 dev 블로커 = Entra admin consent·자동배포·마이그Job·dispatcher 안정화·test 환경). 상세=`docs/handoff/pending-infra-requests.md §9`. (PR: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/12653)

  > 범례: ✅ 완료(괄호=완료일·날짜만이면 **이전 주 완료**) · **🆕 = 이번 주(8/31 이후) 신규 해결·검증(주로 2026-09-03 Jack ③-I 인프라 배치·9/9 Entra·admin 부팅)** · 🟠 부분 · ☐ 미완 · ⚠ 전달 필요. _(9/10 현실화: pending-infra §9 Jack 9/3 실측 + dev 엔드포인트 재확인 반영.)_

  | # | 요청 | 수신 | dev | prod |
  | --- | --- | --- | --- | --- |
  | 1 | Region Directory 호스팅 + `consoleHost` 발행 | ③-I | ✅ publish(8/18·`regions.gw.dev.ezcld.net`) · ✅ `consoleHost` 발행(8/31·PR #13355 Jack 머지·`curl regions.json` 확인) | ☐ 도메인 후(prod consoleHost) |
  | 2 | GW Console dev 호스팅([console.gw.dev.ezcld.net](https://console.gw.dev.ezcld.net)) | ③-I | ✅ 개통(8/19·CD 파이프라인·딥링크 rewrite) | ☐ 도메인 후 |
  | 3 | **dev GW 백엔드 배포·env 주입**(`DATABASE_URL`[공용 `common-dev-db`·`gw` DB·apne2]·`REDIS_URL`·`GW_REGION`=apne2·AWS **Pod Identity**·`NODE_ENV` 차트 주입) | ③-I | **core·receiver·dispatcher = ✅ 기동 완료**(8/31 자가검증: core·receiver 404=healthy backend·기동 확인 / dispatcher=HTTP 엔드포인트 없어 배포상 기동) · **admin = 🆕 부팅 확인(9/10: `/v1/admin/me` 401=healthy·8/31 503 해소)** · 단 **Console 실로그인은 admin consent 승인 대기**(consent 미승인→사용자 토큰 취득 불가) | ☐ |
  | 4 | **운영자 Entra 앱 등록**(GW Admin API + Console SPA·2앱·PKCE) | IT·③-I | 🆕 **dev 2앱 등록·회신 완료(9/9)·GW 배선 완료** · 남은 것 = **admin consent 승인 1건**([IT-9442](https://vts.vatech.com/projects/IT/issues/IT-9442)·IT팀 승인 대기·조직 1회) → **승인 전까지 Console 실로그인 불가**(admin API 자체는 9/10 부팅 확인·401) | ☐ prod 등록 시 동일(도메인 후) |
  | 5 | **env-reference 환경별 값 채움**(test·sandbox·prod endpoint·호스트·리전) | ③-I | ✅ dev · ☐ test/sandbox/prod | ☐ |
  | 6 | **dev-seed grant**(`DATABASE_URL` 변수그룹·Environment 승인게이트) — 전용 수동 파이프라인 `gw-dev-seed.yml`(멱등·`dev:showcase`)용 | ③-I | 🟠 **미완 확정(9/10 ADO 실측: `gw-dev-seed`/`DATABASE_URL` 변수그룹 부재)** · 파이프라인(id 335)·Environment 승인게이트(id 9)·AWS 서비스커넥션 `gw-dev-seed` 등록됨 ✅ · **남은 것 = `DATABASE_URL`(dev RDS) 변수그룹 미생성** → **Jack: 변수그룹 `gw-dev-seed`+`DATABASE_URL`(시크릿)+파이프라인 링크** + **SC 롤 KMS grant**(Encrypt/GenerateDataKey). AWS 5변수는 **GW가 서비스커넥션 전환**(PR 13358)→Jack 불요. ⚠ **혼동 주의**: Jack이 9/3 한 것은 **KMS CMK(#8)**(별개 항목)이며 dev-seed 변수그룹/grant는 미완. + alias명 정합(#8 실물 `alias/gw-payload-apne2` ↔ 시드 기대 `alias/gw-webhook-payload`) 확인 필요. 요청 8/20. | — |
  | 7 | **`pg_trgm` CREATE EXTENSION 권한**(clinic 검색 선결 · env-reference §2.1) | ③-I | ✅ 문제 없음(Jack 확인 8/20 — `gw_app`=`gw` DB OWNER·trusted extension) | ☐ prod 동일 확인 |
  | 8 | **KMS CMK provisioning**(webhook payload·target 자격 alias·리전별 · 8/4 키 토폴로지 · env-reference §2.4) | ③-I | 🆕 **완료(9/3 Jack·AB#5650)**: ① `alias/gw-payload-apne2`(PR 12413) · ② `alias/gw-target-cred-apne2`(PR 13573 apply·SSM alias 4앱 주입) · 기능검증=admin 파드 복구 후 | ☐ 리전별(prod) |
  | 9 | **admin API dev ingress 노출**(`admin.apne2.gw.dev.ezcld.net`·Entra-gated 공개 ingress) — Console이 실 dev DB 데이터를 조회하려면 admin 부팅에 더해 이 ingress가 있어야 함(없으면 admin이 떠도 Console이 못 부름) | ③-I | ✅ **ingress 구축 확인**(8/25 curl: 443 OPEN·ALB 응답) — 단 전 경로 **503(ALB에 healthy target 0·즉시응답)** = **admin 미기동**이 원인(ingress 문제 아님)·**9/10 재확인: `/v1/admin/me` = 401**(admin 부팅·healthy·8/31 503 해소·ingress serving 확인) · 남은 건 Console 로그인용 **admin consent** | ☐ 도메인 후 |

- **[GW 구현 선결 추적 · 외부 인프라·자격]** — E2E·배포가 외부 선결로 막힌 항목. 소유별 상태·ETA 확인.

  | # | 선결 항목 | 소유 | dev | prod |
  | --- | --- | --- | --- | --- |
  | 1 | 공개 ingress(AXS→GW webhook 수신) | ③-I | ✅ **완료**(9/3 Jack 확정·es-infra PR 12931·8/20 · `curl axs.webhook.apne2.gw.dev.ezcld.net`→404 healthy) | ☐ prod |
  | 2 | 실 IoT Core(MQTT 다운링크·Thing/policy·IRSA·`MQTT_URL`) | ③-I | 🆕 **완료(dev·9/3 Jack)**(es-infra PR 12190 · 공유 policy `dev-ezserver-edge` · `MQTT_URL`=Secrets Manager `dev/…dispatcher` · dispatcher `iot:Publish gw/clinic/*`) · ⚠ **E2E 미실행**(dispatcher exit137 반복·enroll Thing 0=별건) | ☐ |
  | 3 | 자동배포 파이프라인(main→DEV·tag→TEST/PROD) | ③-I | 🟠 **① main→DEV = 됨**: `devsecops-{core·receiver·dispatcher·admin·migrate}.yml` **main 트리거** → ECR push → es-gitops `imageTag` 스탬프 → ArgoCD sync(dev 4앱 배포·migrate id 340). **9/10 ADO 실측: 5개 파이프라인 등록·최근 실행 `main`/`individualCI`/`succeeded`(9/3)** → **main 머지 시 dev 자동 배포 실동작 확인**. · **② tag→TEST/PROD = 안 됨**: 릴리스 태그 기반 상위환경 승격 경로 **미구축** — 원인은 파이프라인이 아니라 **test 환경 미프로비저닝(선결 #5)·prod 미설정**. 환경 생기면 같은 템플릿에 태그 트리거만 추가 | ☐ prod |
  | 4 | Parameter Store write IAM + ESO + AWS 커넥션(compat publish 포함) | ③-I | 🆕 **완료(dev·9/3 Jack·AB#5650)**: write IAM·SC(PR 12694) · 발행 파이프라인(354 run 53818) · ESO 마운트(es-gitops PR 13571) · `GW_COMPAT_MATRIX_DIR` 주입 · `/.well-known/production/server-configuration.json` **200** | ☐ test/prod |
  | 5 | **test 환경 프로비저닝**(별도 인프라·GW=infra 분류·상시 최소 baseline+임시 확장·부하/HA 사이즈업 포함) | ③-I | ☐ **요청 완료·마감 8/26** | ☐ |
  | 6 | AXS 자격 | Straumann·영업 | ✅ sandbox(8/11) | ☐ prod(NDA후) |
  | 7 | 파일 붙은 lab order 시드 | Straumann·④ | ☐ (sandbox) | — |
  | 8 | **마이그레이션 배포 Job 배선**(migrate 이미지 ECR push[앱과 같은 SHA] · 매 배포 前 1회 `migrate deploy`·성공 gating·fail-closed) | ③-I | ✅ **완료(dev)**: ③-I 회신 3건 해소(§확정)·**PreSync→sync-wave Job 확정**(AB#5206·wave0 SA/ESO→wave1 migrate→wave2 Deploy)·ECR `vt-api-gateway-migrate`(es-infra PR 13034)·`devsecops-migrate.yml` 완성·**ADO 파이프라인 등록(id 340)** · GW 몫(#12926·#13173·#13184) | ☐ test/prod OWNER 확인 |

  _(`—`=해당 없음.)_

  > **[③-I 요청 전달 감사 — 2026-08-26]** "문서에 선결로 적혀 있다 ≠ Jack에게 전달됨." 두 추적 표를 훑어 GW handoff 7종 전부 **결과 Form·전달 흔적 0** 확인(작성 ≠ 전달). 전달 흔적 없는 항목(③-I #8·GW선결 #1·#2·#4 + Console CloudFront 헤더 4-tier·사내 접근제한[8/19 회신서 누락 변종])을 **handoff + 결과 Form 단일 전달 패킷**([pending-infra-requests.md](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/handoff/pending-infra-requests.md&version=GBmain)·GW repo·초안)으로 묶음. **전달 주체 = Raymond**(PL 지시). 이후 모든 ③-I 요청은 handoff+Form으로 전달하고 회신을 이 표에 일자·산출물로 기록(재발 방지). 모범 = 마이그레이션 인계(#13020).

- 공유 사항 (결정 아님 · 논의사항인지 애매한 것을 임의 결정해 공유 · 매주 상시)
  - **공용 빌드 서버 Jenkins Java 21 이관(밀린 유지보수 · 기한 이미 경과)** — 이번 복구로 Jenkins 코어를 **Java 17로 도는 마지막 LTS(2.541.3)** 에 맞췄으나, 이는 임시 고정점이다(GW 서비스와 무관 — GW CI는 Jenkins를 쓰지 않는다). **기한을 정하는 것은 Jenkins의 Java 17 지원 종료 일정**인데, 이는 **이미 지났다** — Java 17은 Jenkins 기준 **2026-03-31 EOL**, LTS는 **2026-05-13(2.555.1)부터 Java 21 전용**으로 전환돼 Java 17 지원을 제거했다. 즉 2.541.3은 직전 세대라 **보안 백포트가 이미 끊긴 상태**다(미패치 노출 누적). 리스크는 격리돼 있으나(사내 abc-wbs 제품 스캔용·외부 노출 아님) **미룰 수 없는 밀린 유지보수**다. **권장 = 향후 2~4주 내 한가한 창에 계획 이관**(당장 오늘은 에이전트 준비 선행 필요, 무기한 유지는 불가). 순서 = **에이전트 먼저(LinuxNode 4대 Java 21 재빌드 — Windows 노드는 이미 JDK 23이라 불요) → 마스터 최신 LTS 나중**(반대로 하면 에이전트가 못 붙어 전 노드 탈락). 상세 = `references/Self-hosted1/99.2. Jenkins 복구 기록`.

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
    | **v1.0 정합·하드닝**(이번 주) | connector_type 어댑터 프로파일 레지스트리(파생 폐기·특정 target 하드코딩 금지·#13357) · target_id DNS 라벨 전 소비자 일괄+seed 하이픈(#13363) · dev-seed AWS 서비스커넥션(#13358) · CleverSpace `internal_bypass` 단정 제거(#13404) · 데모 steps 정직성(#13314) · unknown connector_type fail-closed 3계층 회귀 확인 | ✅ 머지 완료 |
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
      - 🟢 **지금 착수 가능(9/3 ③-I 인프라 풀림) — IoT 다운링크 E2E**(T-DISP-9-5·T-E2E-12-6): **③-I 대기 아님·GW 몫**. ① **dispatcher exit137 원인규명·해소**(OOM=리소스→③-I / 코드→GW·dev EKS `kubectl` 필요) → ② **device Thing enroll 1건** → ③ **webhook→IoT Core→EzServer 다운링크 E2E 1회**. 실행 주체=**구현 세션**. · 그 외(부하·HA=test 환경 · presign=Straumann 시드)는 여전히 막힘.

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
