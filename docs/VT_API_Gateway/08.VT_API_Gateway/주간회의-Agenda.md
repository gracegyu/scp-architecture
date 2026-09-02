# VT API Gateway — 9/3 주간회의 Agenda

> **과거 주차(~8/27)는 [`주간회의-Agenda-Archive.md`](주간회의-Agenda-Archive.md)로 이관·보존**(조회용). 본 문서는 **9/3 현행 주차만** 유지한다. 틀(논의/공유/이월)·Gantt(S1)·스펙표(S2)는 매주 상시 포함.

- **이번 주 진행 (~9/3 회의) — 이번 주 완료·진행한 실제 작업**

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
    - **[8/31 Straumann 데모]** dev console에서 **VT 이미지가 GW를 거쳐 실 AXS sandbox에 저장되고 되가져와 표시**되는 것을 시연 — 누구나 dev console 링크에서 클릭
      - **로컬 검증 성공** — 실제로 이미지를 선택→전송하니 **실 AXS sandbox로 올라갔다 되돌아온 것을 화면에서 확인**(왕복 관통). 흐름은 이미 되고, 남은 건 dev에 올리는 것뿐.
      - **구현·머지 완료**: GW core 전송 엔드포인트 · Console Demo 화면 · 데모 OnePager(실행계획·API 계약). 추가로 **전송 단계 로그**(GW가 device 자격 대행·정책/egress 검사·조직 해석·AXS 토큰/생성/업로드/조회)를 화면에 표시해 "GW가 무엇을 했는지"까지 보이게 함 — **구현 완료·후속 PR 준비**(실 AXS e2e 8단계 green).
      - **실제성(중요)**: **전송은 실 GW·실 AXS·실 데이터**(mock 아님). 화면의 부가 브라우징(clinic 목록 등)만 배포 console 특성상 mock이라 **데모에서 제외**하고 전송+되가져오기에 집중.
      - **데모 당일 남은 것 = ③-I 실 인프라뿐**: DB 마이그레이션(테이블 생성·**최대 병목**)·dev→AXS egress·KMS·core 데모 경로 ingress·데모 활성 env·dev 재배포 → 이후 배포 링크 리허설.

    - **[target_id 규칙 확정]** `target_id` 형식을 **DNS 라벨(RFC 1123)** 로 못 박고 스펙·코드를 함께 맞춤 — 부모 `spec-v1.0.71` · Console SRS FR-CON-18(`spec-v1.0.9`).
      - ⚠ **화면이 서버보다 느슨했다** — Console 검증이 `^[a-z0-9_]+$` 라 **밑줄을 통과시켰는데** 서버는 거절한다. 게다가 **안내 예시가 `clever_space`**(밑줄)여서 **예시를 그대로 따라 하면 저장 시 400** 이었다. 화면이 사용자를 틀린 길로 안내한 셈.
      - **수정**: 패턴을 DNS 라벨(+최대 63자)로 교체 · 예시를 하이픈으로 · **무엇이 걸렸는지 짚는 오류 문구**(대문자/밑줄/공백/시작·끝 하이픈/길이) · **치는 동안 인라인 검증**(저장까지 기다리지 않음) · 규칙과 이유(`axs.webhook.apne2.gw…` 서브도메인 첫 라벨이 됨)를 화면이 스스로 설명.
      - 부수 소득: **기존 테스트가 옛 규칙을 고정**하고 있어(밑줄 통과가 통과 조건) 느슨한 상태가 보호되고 있었음 — 함께 뒤집음. 시각 회귀 게이트가 **i18n 누락·문구 치환 오류 2건**을 추가로 잡아냄.
      - **정리(8/31)**: 당초 SRS+구현을 #13309 한 PR로 냈으나 connector_type 작업과 겹쳐 → 스펙은 **#13351에 흡수**·코드는 **#13359로 이동**·**#13309 close**. 추가로 **admin DTO 패턴이 아직 옛 `^[a-z0-9_]+$`** 였음을 발견 → **GW #13363**: target·정책·org-mapping·컨트롤러 @ApiParam **전 소비자 RFC 1123 일괄** + seed 하이픈(커플링). 스펙 OpenAPI도 OrgMapping·Policy targetId 패턴 정합(#13349). **✅ 데모 후 머지 완료**.
    - **[Target 범용화 — connector_type 도입]** ⭐ 아웃바운드 커넥터가 AXS 관례(Organization-ID·`storageUrl`·org 1:1)를 **코드 상수로 하드코딩**해 **제2 external target이 record만으로 조용히 오동작**하는 사각지대를 3면 감사(GW·Console·스펙)로 발견 → **`connector_type`(어댑터 프로파일)을 v1.0에 정식 도입**(파생 판별 폐기).
      - **★범용 불변식(NORMATIVE)**: 런타임 소스에 `if targetId==='axs'` 류 특정 target 하드코딩 금지 — 동작차는 오직 `connector_type`→프로파일 레지스트리로만. 새 파트너=프로파일 추가(코드 1곳), 특정 target 하드코딩 X.
      - **⚠ 제약(현실)**: "신규 target = 코드 0(record만 추가)"은 **관례가 기존 프로파일과 일치할 때만** 성립
        - **target마다 인증 방법·clinic(org) 식별 방법이 다름**(헤더명/토큰 클레임/경로·서명 체계·업로드 위임 유무 등) → **초기 몇 개 target은 새 프로파일/전략(코드) 추가가 불가피**.
        - 범용 불변식(하드코딩 금지)은 항상 준수하되, "코드 0"은 **성숙기 목표** → **초기 확장기엔 target별 추가 개발을 전제로 일정·범위**를 잡음(SRS §7.5.1 명문화·백로그 B-19).
        - 프레임워크 가치 = 추가가 **한 곳(프로파일/전략)에 국소화**·코어 무파급.
      - **v1.0 커넥터 타입 2개**
        - **`internal_bypass`**: 내부 신뢰망 · **v1.0 확정 사용처 없음**(CleverSpace는 ③b P0로 v1.1).
        - **`oauth2_org_header`**: OAuth2 client_credentials 인증(tenant 단일) + Organization-ID 헤더로 org 구분(예 AXS).
        - 명명 이력: 구 `oauth2_cc` → `oauth2_org_scoped` → **`oauth2_org_header`**("org_scoped"가 "토큰이 org별 스코프"로 오독돼 개명·스펙 #13417).
      - **descriptor 스키마-구동**: GW `GET /v1/admin/connector-types`가 type별 필드 서술 반환 → Console이 폼을 **동적 렌더**(정적 per-type 분기 금지) → 새 프로파일 시 **Console 코드 0**(범용성이 프론트에도 관철).
      - **스펙**: GW **#13349**(spec-v1.0.73·§7.5.1 재작성·카탈로그·descriptor·Q2/Q3·targetId 정합) · Console **#13351**(FR-CON-16 스키마-구동 폼·#13309 흡수) · 부수 **#13338**(KMS-envelope 설명 정정).
      - **구현**(✅ 머지 완료): GW **#13357**(파생→레지스트리 dispatch·`oauth2_cc`→`oauth2_org_scoped`·profile↔type 400·변경 409·cross-field 400·unit 1994) · Console **#13359**(type-first·descriptor 동적 폼·profile 읽기전용·TARGET_ID_PATTERN) · GW **#13363**(target_id 전 소비자) · GW **#13358**(dev-seed AWS 서비스커넥션).
      - **데모 무영향**(당시): 전부 feature 브랜치·기존 AXS=`oauth2_org_scoped` byte-identical. **✅ 데모 후 전부 머지 완료**(스펙→코드 순·IP 태그 핀 spec-v1.0.73).
    - **[CleverSpace 연동 → v1.0에서 v1.1로 변경]** ⭐ connector_type 후속 — Console 화면 검증에서 카탈로그가 `internal_bypass` 예시를 'CleverSpace'로 **단정**한 것이 발단. 조사 결과 **CleverSpace ③b(GW→CleverSpace) 신원 전달이 미정(P0)**이고(review-log-12239 C-02 — CleverSpace는 JWT 필수라 '내부 신뢰'가 아님), **v1.0은 이미 종료됐고 CleverSpace는 실연동된 적이 없음** → **CleverSpace 실연동을 v1.0 → v1.1로 변경**(추후 CleverSpace 연동 요구가 있을 때).
      - **v1.0 = AXS만 실연동** · CleverSpace는 presigned 중계 capability(구조적 지원)만. **실연동(target 등록·connector·③b 신원 전달)=v1.1**. SRS 전수 조사로 v1.0으로 적힌 곳(§41·§887·§1160·§2376·§2.6·§2.7·③b 헤더 등)을 모두 v1.1로 정정.
      - **CleverSpace 커넥터 타입 = `oauth2_jwt_assertion`**(GW 서명 upstream JWT 어서션·RFC 7523 · CleverSpace GW Guard가 JWKS로 검증) — v1.0 카탈로그엔 `availability:planned`·`plannedIn:v1.1`로 **자리만** 둔다(구현은 v1.1).
      - **안전(fail-closed)**: planned 타입은 dispatch 레지스트리 밖 별도 목록 → 모르는 타입은 **거절(throw)**·인증 없이 통과 없음. GW 3계층 회귀 테스트로 잠금 확인(73/73 green).
      - **JWKS 엔드포인트만 v1.0 선공개 유지**(공개키 노출 무해·재도입 churn 회피·실제 소비자 CleverSpace GW Guard는 v1.1).
      - **스펙**: **#13406**(spec-v1.0.74·CleverSpace 단정 제거) merged·태그 완료 · **#13413**(spec-v1.0.75·전수 v1.1 정합+planned 카탈로그+descriptor availability 필드) **✅ merged·태그 완료**. 선행 GW **#13404**(description 정정·merged)·Console **#13408**(폼 planned 안내). 백로그 B-20 결정 반영.
    - **[Console 운영 매뉴얼 작성]** 운영자가 GW Console을 보고 **따라할 수 있는 운영 매뉴얼** 착수 — 가장 어렵고 중요한 **연동 대상(target) 등록·관리**부터
      - 한국어·task(작업)별 다중 문서 + 인덱스 구조 · 스크린샷도 한국어 화면(대표 데이터·PHI 없음)
      - target 문서 = **사례 주도**(AXS·CleverSpace로 따라하기)·필드 설명·연동 켜기(org 매핑)·트러블슈팅
      - 진행: **target 등록·관리 + 인덱스(README) 문서 ✅ 머지 완료**(#13507 · `docs/manual/`). 현행 결정(oauth2_org_header·CleverSpace v1.1 oauth2_jwt_assertion·target_id DNS 라벨·sandbox/prod 2 target·prod 수동 등록) 반영.
      - 잔여: Console 세션이 **실제 화면 스텝·한국어 스크린샷 보완**(문서 내 `[Console 확인 필요]` 표시) · **나머지 메뉴 문서**(device-onboarding·org-mapping·webhook-events·operators-rbac·clinic·config·audit — README에 *(작성 예정)*).
    - **[프로세스 버전·빌드 정보 API — 배포 검증]** ⭐ 각 프로세스가 자기 버전/빌드정보를 서빙해 **새 이미지가 실제 붙었는지(배포 landed)를 화면에서 즉시 확인**. **계기**: dev 데모 500 진단 때 "무엇이 배포됐는지 화면서 알 수 없다"가 지연 원인이었음(개명 후 dev `axs` 행 미이관·배포본 확인난).
      - **설계**
        - per-process **`GET /version`**(core·admin·receiver·dispatcher): version·gitCommit·buildTime·startedAt·region · `/health`와 분리·무인증 인프라.
        - **dispatcher도 이미 Nest HTTP 앱(HealthModule)** → 다른 3앱처럼 `/version` 컨트롤러만 추가(별도 리스너 불요·as-built).
        - **admin 취합 `GET /v1/admin/system/versions`**(operatorAuth·4개 fan-out·status ok/unreachable·부분 결과) → **Console 1콜 표**.
      - **배포 검증 UX**: gitCommit **불일치(롤아웃 미완)**·**unreachable**·재기동(startedAt)을 화면이 플래그.
      - **빌드 주입**: version=package.json · gitCommit/buildTime=Docker build ARG→env(Jack Dockerfile 조율·미주입 시 unknown).
      - **버전 규약 = SemVer (BE·FE 모두)**: 버전 관리·서빙을 **[SemVer](https://semver.org) 규약**으로 통일 — 정식 `1.0.0` 출시 전까지 `1.0.0-alpha.N`(PR마다 N↑) → `beta.N`/`rc.N` → `1.0.0`. **SemVer 표준 준수라 프로젝트별로 규약을 구구절절 설명할 필요 없음.** version API가 이 값을 그대로 서빙(version이 곧 라벨·별도 releaseVersion 없음). *(FE self-version 화면=Console 백로그 CB-8 → ✅ 완료·#13441.)*
      - **스펙**: GW **#13435**(spec-v1.0.79·§7.8.6 FR-SYS-01·OpenAPI `ServiceVersion`) merged·태그 · Console **#13436**(spec-v1.0.12·FR-CON-39 version 표) merged·태그.
      - **구현 분담**: GW(4 `/version`+dispatcher HTTP+admin 취합) · Console(version 표·계약 확정이라 목 우선 착수) · Jack(Dockerfile build ARG·마이그레이션 Job 배선).

    - **[CI 셀프호스티드(Self-hosted1) 전환 — 공유 풀 적체 해소]** ⭐
      - **계기**: 공유 Agent pool 대기열이 심하게 적체돼 GW·Console CI가 몇 시간씩 큐에 묶임 → 사내 자체 구축 풀 **Self-hosted1**(사내 서버·docker 컨테이너 에이전트)로 빌드를 되살림. **지난번 실패 원인 = 에이전트에 Docker 미설치**(이미지 buildx 불가)로 확인·해소.
      - **1) 에이전트 재구축** (`references/Self-hosted1`)
        - 에이전트 이미지(`azp-agent:linux`)에 추가: **docker-ce-cli + buildx**(이미지 빌드) · **AWS CLI v2**(ECR push·S3 sync) · **Playwright chromium 시스템 라이브러리**(Console e2e). 기존 Node/pnpm/git/jq/Rust 유지.
        - 재설치 스크립트에 **`-v /var/run/docker.sock` 소켓 마운트** → buildx가 호스트 도커 데몬 사용.
        - Linux 에이전트 **4대**(`demands: agent.os -equals Linux`).
        - **보안**: 재설치 스크립트에 실 PAT 포함 → **git 추적 제거 + `.gitignore`**. 신규 PAT는 **Agent Pools(Read & manage) 스코프만**.
      - **2) 스모크 검증** (진짜 파이프라인 전 에이전트 능력만 확인)
        - `trigger:none/pr:none` 스크래치 파이프라인으로 **적체 큐를 안 타고** 검증.
        - 8단계: 도구 존재 · **docker 데몬+buildx build**(지난번 실패 지점) · Node 20.19 · pnpm 9.15.9 · **playwright chromium launch** · 리소스.
        - **8/8 green**(소켓 미마운트·playwright 모듈 미설치 이슈 잡아 수정 후 통과) → 지난번 실패(docker buildx) 해소를 실측 확인.
      - **3) 중앙 템플릿 pool 파라미터화** (Jack 소유 `es-ci-templates` · **PR #13482 머지**)
        - 공용 `devsecops.yml`에 **`pool` 파라미터(기본값 `{vmImage: ubuntu-latest}`)** 추가 + 3개 job 배선.
        - **가법적·기본값 보존** → **GW만 오버라이드로 opt-in**, 다른 Product 무영향.
        - **Cache@2 미도입**: self-hosted에선 매 실행 ~1GB 캐시 tarball 업로드가 순손실(로컬 디스크 캐시가 지속되므로 불요).
      - **4) 적용**
        - **범위 기준** = **GW/Console PR·머지 회전에 직접 영향(적체가 PR/배포를 막는)** 것만 우선. 드물고 늦어도 되는 compat·docs-wiki·seed·부하/HA·promote는 **확대 후보로 제외**(트리거/전제조건은 `references/Self-hosted1/README.md` backlog).
        - **GW root CI**(GW 세션): **#13480** — root `azure-pipelines.yml` 풀→Self-hosted1+demands Linux · pnpm Cache@2 제거. 머지 전 대기 · 블로커=`vt-api-gateway-ci` **풀 인가**(Raymond).
        - **GW devsecops-\* 5종**(core/admin/receiver/dispatcher/migrate·GW 세션): **#13498** — `extends.parameters`에 `pool: {name: Self-hosted1, demands: [agent.os -equals Linux]}` 오버라이드. #13482 선병합 확인 → 머지 가능.
        - **Console**(Console 세션): CI 풀 Self-hosted1 전환(watched PR).
        - ⚠ **선결(Raymond 포털)**: 각 파이프라인을 `Agent pools → Self-hosted1 → Security → Pipeline permissions`에 **파이프라인별 등록**해야 실행됨(**Open access 금지** — chromium 경합 플레이크). 스모크 파이프라인은 등록 완료.
      - **5) OOM 먹통 사고·대책 (9/2)** — 상세=`references/Self-hosted1/README.md`
        - **현상**: 전환 직후 GW·Console 잡 동시 실행 → 메모리 고갈 → swap 스래싱 → **GUI·SSH 먹통**(15분 load average **249**).
        - **진단**: 빌드 호스트(BuildMachine2·**32 vCPU / 62GB**)가 **CI 전용이 아닌 공용 서버**였음 — dependency-track 7.4GB·sonarqube·jenkins·abc-wbs 앱·win10 VM 7.7GB 상주 → **CI 실여유 ~30GB뿐**. 근본 원인 = **테스트 러너가 코어 수로 워커 자동 증식**(Jest 기본 **31/job**) × **에이전트 4대** 중첩.
        - **대책** (전부 리부팅 후 유지):
          - ① **워커 공통 상한 2**: GW Jest `--maxWorkers=2 --workerIdleMemoryLimit=1GB`(#13480) · Console vitest2/playwright2(#13441).
          - ② **에이전트 컨테이너별 `--memory=6g --memory-swap=6g`**: blast-radius 차단(폭주해도 호스트·상주서비스 못 죽임). `docker update` 즉시 적용 + `reinstall_agent.sh` 반영.
          - ③ **win10 KVM 종료**(`virsh destroy`+autostart off): **7.7GB 회수**·리부팅해도 안 올라옴. 방치된 Windows 에이전트(2024-11 이후 미사용) 호스트였음.
          - 서비스화(자동복구)는 **이미 충족**: 에이전트 `restart=unless-stopped` + docker 데몬 부팅 enabled.
        - **✅ 해결 확인 (9/2·실부하 상태)**: 사용 **24GB / 여유 38GB**(62GB 중) · load **249→13** · 에이전트 실작업 중(playwright 도는데도 안정) · 상한 유지.
          - **구조적 보장**: 최악 = 4대 × 6GB = **24GB** + 상주 ~22GB = **46GB < 62GB** → 호스트 OOM이 **수학적으로 불가**. (부하가 몰려도 상한 때문에 CI 총량이 24GB를 못 넘음.)
        - **보류(관측 후 판단)**: 에이전트 4→2 축소(위 여유상 불필요할 듯)·job 동시성 제한.
      - **6) 효과 실측 (9/2·전후 평균·성공 빌드 기준·타임라인 workerName으로 실행 풀 판별)**

        | 파이프라인 | 구분 | 표본 | 실행 | 큐 대기 | 총 회전 |
        | --- | --- | --- | --- | --- | --- |
        | **GW CI** | Microsoft-hosted(전) | 13 | 6.9m | 16.9m | 23.8m |
        | | **Self-hosted1(후)** | 8 | **3.2m** | **0.1m** | **3.3m (~86%↓)** |
        | **Console CI** | Microsoft-hosted(전) | 2 | 36.8m | 30.9m | 67.7m |
        | | **Self-hosted1(후)** | 11 | **6.4m** | **1.3m** | **7.8m** |

        - **최대 효과 = 큐 대기 소멸**(공유 풀 적체 해소=원래 목적) · 실행시간도 단축(i9-14900 32코어 + **영속 pnpm/docker 캐시**·워커 상한으로 느려질 법한데도 상쇄).
        - ⚠ **표본 신선**: 9/2 전환이라 after는 하루치 · **Console before n=2**(참고치) · Console self 실행 편차 큼(0.9~24.3m·path 필터 부분런 섞임). GW는 일관적(2.5~4.5m)이라 신뢰도 높음 → 며칠 후 재산출 시 정밀화.

  - **진행 중 · 선결 대기**
    - **[GW dev 배포·통합]** core·receiver·dispatcher dev 기동 확인 · admin=Entra 등록 후 통합 착수(③-I #3)
    - **[GW Console 통합]** 실 dev GW + Entra 접목 · 완료 화면 포함 정합성 확인 마무리
    - **[Entra 앱 등록]** dev admin+Console 2앱 — **[IT-9442](https://vts.vatech.com/projects/IT/issues/IT-9442)**(Jack 입력·절차/회신 양식 제공 완료) · **admin 부팅 선결**(③-I #3·#4)
    - **[제품 연동 스펙]** EzServer OnePager 수령 확인(잔여)

  - _(이번 주 결정사항 = 회의 시 추가)_

- 논의 사항 (이번 주 · 신규 · R#)
  - _(회의 중 신규 논의/결정 안건 발생 시 **R1·R2…** 로 추가 · 선결·보류는 아래 「이월 논의 사항」 표.)_

- **[③-I Jack 인프라 요청 추적]** — 회의에서 상태·ETA 확인. (PR: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/12653)

  > 범례: ✅ 완료(괄호=완료일·날짜만이면 **이전 주 완료**) · **🆕 = 이번 주 신규 구축·자가검증 완료(2026-08-31)** · 🟠 부분 · ☐ 미완 · ⚠ 전달 필요. *(2026-08-31 curl·AWS read-only 자가검증 반영.)*

  | # | 요청 | 수신 | dev | prod |
  | --- | --- | --- | --- | --- |
  | 1 | Region Directory 호스팅 + `consoleHost` 발행 | ③-I | ✅ publish(8/18·`regions.gw.dev.ezcld.net`) · **🆕 `consoleHost` 발행(8/31·PR #13355 Jack 머지→파이프라인·`curl regions.json` 자가검증: `console.gw.dev.ezcld.net` 노출 확인)** | ☐ 도메인 후(prod consoleHost) |
  | 2 | GW Console dev 호스팅([console.gw.dev.ezcld.net](https://console.gw.dev.ezcld.net)) | ③-I | ✅ 개통(8/19·CD 파이프라인·딥링크 rewrite) | ☐ 도메인 후 |
  | 3 | **dev GW 백엔드 배포·env 주입**(`DATABASE_URL`[공용 `common-dev-db`·`gw` DB·apne2]·`REDIS_URL`·`GW_REGION`=apne2·AWS **Pod Identity**·`NODE_ENV` 차트 주입) | ③-I | **core·receiver·dispatcher = ✅ 기동 완료**(8/31 자가검증: core·receiver 404=healthy backend·기동 확인 / dispatcher=HTTP 엔드포인트 없어 배포상 기동) · **admin = 🟠 Entra 구성만 대기**(앱은 배포/기동됨 · 현재 외부 503은 Entra 미구성으로 readiness/인증 미통과 · 구성되면 serving) | ☐ |
  | 4 | **운영자 Entra 앱 등록**(GW Admin API + Console SPA·2앱·PKCE) | IT·③-I | 🟠 **진행중 · [IT-9442](https://vts.vatech.com/projects/IT/issues/IT-9442)**(Jack 입력·절차·회신 양식 제공 완료)·마감 8/21 경과·**admin 부팅 선결** | ☐ 도메인 후 |
  | 5 | **env-reference 환경별 값 채움**(test·sandbox·prod endpoint·호스트·리전) | ③-I | ✅ dev · ☐ test/sandbox/prod | ☐ |
  | 6 | **dev-seed grant**(`DATABASE_URL` 변수그룹·Environment 승인게이트) — 전용 수동 파이프라인 `gw-dev-seed.yml`(멱등·`dev:showcase`)용 | ③-I | 🟠 **8/31 자가검증**: 파이프라인(id 335)·Environment 승인게이트(id 9)·AWS 서비스커넥션 `gw-dev-seed` 등록됨 ✅ · `- group:` 로드실패는 PR 12806서 수정(8/19 에러=stale) · **남은 것=`DATABASE_URL`(dev RDS) 변수그룹 미생성** → **Jack: 변수그룹 `gw-dev-seed`+`DATABASE_URL`(시크릿)+파이프라인 링크**(+서비스커넥션 롤 KMS 권한 확인). AWS 5개 변수는 **GW가 YAML을 서비스커넥션(`AWSShellScript@1`)으로 전환**(VT-GW-구현·데모 후)→Jack 불요. 요청 8/20. *(seed 변경=스크립트 수정+재실행·멱등·재요청 불필요)* | — |
  | 7 | **`pg_trgm` CREATE EXTENSION 권한**(clinic 검색 선결 · env-reference §2.1) | ③-I | ✅ 문제 없음(Jack 확인 8/20 — `gw_app`=`gw` DB OWNER·trusted extension) | ☐ prod 동일 확인 |
  | 8 | **KMS CMK provisioning**(webhook payload·target 자격 alias·리전별 · 8/4 키 토폴로지 · env-reference §2.4) | ③-I | ☐ (webhook/target 실사용 시) · **8/31 자가검증: `gw` KMS alias 없음=미프로비저닝 확인(트리거 前이라 정상)** · ⚠**전달 흔적 없음**→전달패킷 §4(handoff+Form·트리거 명시) | ☐ 리전별 |
  | 9 | **admin API dev ingress 노출**(`admin.apne2.gw.dev.ezcld.net`·Entra-gated 공개 ingress) — Console이 실 dev DB 데이터를 조회하려면 admin 부팅에 더해 이 ingress가 있어야 함(없으면 admin이 떠도 Console이 못 부름) | ③-I | ✅ **ingress 구축 확인**(8/25 curl: 443 OPEN·ALB 응답) — 단 전 경로 **503(ALB에 healthy target 0·즉시응답)** = **admin 미기동**이 원인(ingress 문제 아님)·**#4 Entra 구성 시 serving**(8/31 재확인: `/`·`/v1/admin/me` 여전히 **503**·Entra 구성 전이라 미serving 지속·앱 배포는 됨) | ☐ 도메인 후 |

- **[GW 구현 선결 추적 · 외부 인프라·자격]** — E2E·배포가 외부 선결로 막힌 항목. 소유별 상태·ETA 확인.

  | # | 선결 항목 | 소유 | dev | prod |
  | --- | --- | --- | --- | --- |
  | 1 | 공개 ingress(AXS→GW webhook 수신) | ③-I | **🆕 사실상 구축 확인(8/31 자가검증**: `axs.webhook.apne2.gw.dev.ezcld.net` → 404·연결성립·admin과 달리 503 아님=healthy backend 응답) — Jack에 "이미 됨" 1줄 확인 후 ✅ 확정. (기존 전달패킷 §1) | ☐ |
  | 2 | 실 IoT Core(MQTT 다운링크·Thing/policy·IRSA·`MQTT_URL`) | ③-I | ☐ · **8/31 자가검증: endpoint 존재(`a2ig1yuqacb8gl-ats…`)이나 공유 policy 0개=미구성** · ⚠**전달 흔적 없음**→전달패킷 §2(handoff=[docs/handoff/iot-authz-infra.md](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/handoff/iot-authz-infra.md&version=GBmain)·Form) | ☐ |
  | 3 | 자동배포 파이프라인(main→DEV·tag→TEST/PROD) | ③-I | 🟠 dev 배포 됨(3앱) · 자동화·tag→TEST/PROD 잔여(Jack Azure Flow 템플릿→ECR/ArgoCD) | ☐ |
  | 4 | Parameter Store write IAM + ESO + AWS 커넥션(compat publish 포함) | ③-I | ☐ · **8/31 자가검증: `/dev` 하위 `server-configuration`/`.files` 경로 없음=미구성** · ⚠**전달 흔적 없음**→전달패킷 §3(handoff=[docs/handoff/compat-matrix-infra.md](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/handoff/compat-matrix-infra.md&version=GBmain)·Form) | ☐ |
  | 5 | **test 환경 프로비저닝**(별도 인프라·GW=infra 분류·상시 최소 baseline+임시 확장·부하/HA 사이즈업 포함) | ③-I | ☐ **요청 완료·마감 8/26** | ☐ |
  | 6 | AXS 자격 | Straumann·영업 | ✅ sandbox(8/11) | ☐ prod(NDA후) |
  | 7 | 파일 붙은 lab order 시드 | Straumann·④ | ☐ (sandbox) | — |
  | 8 | **마이그레이션 배포 Job 배선**(K8s Job + ArgoCD PreSync hook · migrate 이미지 ECR push[앱과 같은 SHA] · 매 배포 前 1회 `migrate deploy`·성공 gating·fail-closed) | ③-I | 🟠 **GW 몫 완료**(#12926 · migrate 이미지 타겟·실행명령·env·local `make dev-up` 자동) · **인계 명세 전달**(#13020·[docs/handoff/migration-deploy-infra.md](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/handoff/migration-deploy-infra.md&version=GBmain) + 초안 `devsecops-migrate.yml`) · ③-I 회신 3건(org 템플릿 `--target` 지원·migrate 배포스테이지 처리·SHA 태그 경로) + K8s Job+PreSync 배선 대기 | ☐ |

  _(`—`=해당 없음.)_

  > **[③-I 요청 전달 감사 — 2026-08-26]** "문서에 선결로 적혀 있다 ≠ Jack에게 전달됨." 두 추적 표를 훑어 GW handoff 7종 전부 **결과 Form·전달 흔적 0** 확인(작성 ≠ 전달). 전달 흔적 없는 항목(③-I #8·GW선결 #1·#2·#4 + Console CloudFront 헤더 4-tier·사내 접근제한[8/19 회신서 누락 변종])을 **handoff + 결과 Form 단일 전달 패킷**([pending-infra-requests.md](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/handoff/pending-infra-requests.md&version=GBmain)·GW repo·초안)으로 묶음. **전달 주체 = Raymond**(PL 지시). 이후 모든 ③-I 요청은 handoff+Form으로 전달하고 회신을 이 표에 일자·산출물로 기록(재발 방지). 모범 = 마이그레이션 인계(#13020).

- 공유 사항 (결정 아님 · 논의사항인지 애매한 것을 임의 결정해 공유 · 매주 상시)
  - **webhook payload 보존·아카이브 방식(gw/1.1)** — 무한 누적되는 webhook payload(PHI·KMS 암호문) 관리 방식을 임의로 결정해 공유: **리전 로컬 S3 아카이브 후 삭제**(파티셔닝 미채택)·무인 K8s CronJob(시간 기준)·export→검증→배치삭제·잡 단위 감사·tombstone 없음. SRS §7.6.9에 설계 골격+다이어그램 반영(gw/1.1·v1.0=저볼륨 미구현·알람만). 확정 필요 값(리전별 ① DB 잔존 기간 ② S3 보관 기간·+가동 임계값)은 법무 의존이라 **이월 논의 #15**에서 추적(Appendix B #5·#36).

  - **S1. 프로젝트 일정(Gantt) — 8/27 스냅샷**
    - **진행률(구현)**
      - **GW ≈ 90%** — v1.0 계획 기능 구현 완결(8/24 feature-complete)
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

        section ④ AXS 연동 (실연동=GW P7 완료 · ④ Sub-SRS=경량 후속 문서)
        AXS PPR sandbox 자격 확보(8/11) :done, cred, 2026-08-11, 1d
        AXS 실연동 구현·sandbox e2e green(P7) :done, axsimpl, 2026-08-11, 2026-08-24
        실연동 완료(sandbox 커버)      :milestone, done, axsdone, 2026-08-24, 0d
        ④ Sub-SRS 경량 문서(완료 8/27·spec-v1.0.69) :done, axssub, 2026-08-27, 1d
        AXS prod 자격(NDA 후·선결)     :crit, credp, 2026-08-18, 21d

        section ③-C GW Console — v1.0 (frontend·별도 repo·P0~P6 완료·P7 6/7·P8=외부 선결)
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
      | **CleverOne** | 🟡 Vatech-\* 헤더·fallback | 🟡 presigned 이용 | 🟡 Direct→GW 경유 | ⬜ Region 선택·ClinicID | — | 🟢 ③-P-CO OnePager 인계(SharePoint·Nick 검토) |
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
    | **P12** 잔여 | 12-6 인바운드+MQTT(③-I ingress+실 IoT) · 12-3 부하 실측(하네스 완료·③-I test) · 12-4 HA(③-I Multi-AZ) | 🔴 외부 선결 |
    | **P9-5** 실 IoT 프로비저닝 | (a) 코드 완료(어댑터·mock) · (b) 실 IoT Core mTLS 실증 | ◑ (a)완료·(b)③-I |
    | **P0-5** 자동배포(CD) | ECR/ArgoCD·main→DEV·tag→TEST/PROD | 🔴 ③-I |
    | **v1.0 정합·하드닝**(이번 주) | connector_type 어댑터 프로파일 레지스트리(파생 폐기·특정 target 하드코딩 금지·#13357) · target_id DNS 라벨 전 소비자 일괄+seed 하이픈(#13363) · dev-seed AWS 서비스커넥션(#13358) · CleverSpace `internal_bypass` 단정 제거(#13404) · 데모 steps 정직성(#13314) · unknown connector_type fail-closed 3계층 회귀 확인 | ✅ 머지 완료 |
    - 커버리지(merged·8/20): 전역 96.7 / 91.9 / 93.9 / 96.5 · 보안 도메인 98.5 / 96.0 / 100 / 98.4 · 핵심 보안파일 16개 각 100% — **CI floor 게이트 통과**.

    - **남은 작업 — 전부 외부 선결(GW 코드는 feature-complete·코드로 앞당길 잔여 = 0)**

      | Task | 남은 작업 | GW 상태 | 막는 것(루트 블로커) | 소유 |
      | --- | --- | --- | --- | --- |
      | **T-PLAT-0-7** | 마이그레이션 배포 Job | ✅ 이미지·인계 명세(#13020) | K8s Job+ArgoCD PreSync 배선 + **회신 3건**(org 템플릿 `--target`·배포스테이지·SHA 태그) | Jack/③-I |
      | **T-DISP-9-5** | 실 IoT Core 프로비저닝 실증 | ✅ 어댑터·최소권한 policy·cert·enroll | 실 AWS IoT Core(Thing/policy·IRSA·endpoint) | ③-I |
      | **T-E2E-12-6** | E2E webhook→IoT 다운링크 | ✅ 수신·dispatcher drain·멱등·주권 | 공개 ingress **+** 실 IoT Core | ③-I |
      | **T-E2E-12-3** | 부하 실측 | ✅ 하네스·스크립트·파이프라인 초안(#13048) | test staging(실 SQS/EKS)·부하 EC2 | ③-I |
      | **T-E2E-12-4** | HA/카오스 실측 | ✅ drain·RTO probe·loss-verify·파이프라인(#13022·#13048) | test staging·Multi-AZ·FIS **+ RTO/RPO 목표** | ③-I **+ PL** |
      | **T-E2E-12-5** | 환자문서 order-file presign | ✅ create/download 실측 | 파일 붙은 lab order 시드 | Straumann |
      - **최우선 블로커(회의에서 밀 것)**: ① **Entra 앱 등록**(IT-9442·마감 8/21 경과) — admin 미기동 → **dev 통합검증 전체 정체** · ② **test 환경 프로비저닝**(선결#5·마감 8/26) — 부하·HA 2건 동시 해제. **PL 결정 대기 = RTO/RPO 목표**(HA 합격기준). GW 즉시 처리 가능 잔여 = Jack 회신 3건 오면 마이그레이션 파이프라인 확정뿐.

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
      | **T-FE-8-1** | dev Entra 실 OIDC 전환·claim→역할 검증 | ✅ MSAL 실배선·env 스위치·`verify:entra` | **Entra 앱 등록 회신**(IT-9442) **+** admin API dev 기동 | IT/③-I |
      | **T-FE-8-2** | test 환경 실 GW 핵심 여정 e2e | ✅ MSW 대체 커버 + 대체 스펙 문서화 | **test 환경**(선결#5) · CORS(C-3) · T-FE-8-1 | ③-I |
      | **T-FE-9-17** | 목↔**실 GW** 응답 대조(2단계) | ✅ 목↔**계약** 대조 회귀 검사·갭 2건 수정(#13057) | **dev 재배포·재시드**(admin dev = 503 실측) | ③-I |
      | **T-FE-8-4** | prod 배포 | ✅ 프리뷰 배포 파이프라인(S3+CloudFront) | **prod 도메인**(C-10) · ⚠ **무인 대상 제외**(사람이 실행) | PL/③-I |
      | **T-FE-7-6** | 배포 헤더(CSP·nosniff·Referrer-Policy·HSTS) | ✅ **8/26 실측 — 전부 부재**(`curl` 로 판정·사람 불요) | **CloudFront response headers policy 미배선** | ③-I |
      - **최우선 블로커**: ① **Entra 앱 등록**(IT-9442·마감 8/21 경과) — GW admin 미기동과 **같은 뿌리**라 Console 도 dev 실검증이 통째로 정체 ② **dev 재배포·재시드** — 계약(운영자 요약·clinic 임베드·config device-facing)은 **양쪽 다 머지됐는데 dev 에 안 떠 있어** 실화면 확인이 불가.

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
