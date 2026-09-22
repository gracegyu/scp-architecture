# VT API Gateway — 10/1 주간회의 Agenda

- **이번 주(10/1) 착수·진행 · 선결 대기**
  - **[R1 실행] 보안·품질 지표 심사·조치 = 개발자가 AI로 직접** (9/17 회의 결정)
    - **도구 = 사내 표준 CLI `es-toolkit`** — Jira·Confluence 래퍼가 있던 그 `es` CLI에 DT·SonarQube를 `es sec` 서브커맨드로 붙였다. 개발자는 별도 서버 접속 없이 **자기 노트북·프로젝트 폴더에서** Claude Code `/es-sec` 스킬로 쓴다.
    - 흐름 — 취약점·이슈를 직접 조회·수정, 안 고칠 건은 근거 남겨 심사(triage). 모든 쓰기에 `--confirm`

    - ⭐ **핵심은 도구가 아니라 흐름이다 — 취약점 조치가 프로젝트 폴더 안에서 끝난다**
      - 지금까지는 DT·SonarQube 화면을 열고, 무엇이 왜 걸렸는지 따로 파악하고, 코드로 돌아와 고치고, 다시 화면에서 확인했다. **도구와 사람 사이를 네 번 오간다.**
      - 이제 개발자가 **자기 프로젝트 폴더에서 `/es-sec` 한 번**으로 끝낸다.

      | | 단계 | 누가 |
      |---|---|---|
      | ① | 현재 DT·SonarQube 문제를 조회해 **원인과 조치 계획**을 낸다 | AI |
      | ② | **계획을 사람이 검토하고 승인한다** | **사람** |
      | ③ | 고칠 것은 고치고, 안 고칠 것은 **근거를 남겨 심사(suppress)** 한다 | AI |
      | ④ | 재검사 — 다음 새벽 자동 스캔, 급하면 Jenkins 에서 즉시 실행 | 자동 |
      | ⑤ | DT·SonarQube 콘솔에서 결과 확인 | 자동 반영 |

      - ⭐ **사람이 판단하는 자리는 ② 하나다.** 조회·수정·심사 기록·재검사는 전부 자동이다.
      - ⚠ **②를 없애지 않는다** — 억제는 되돌리기 어렵고 서버에 기록이 남는다. 승인 없이 AI 가 "안 고쳐도 된다"고 결정하게 두지 않는다. 모든 쓰기에 `--confirm` 이 걸려 있는 이유다.
      - ⭐ **아래 GW·Console 조치가 이 흐름을 그대로 탄 첫 사례다** — DT 8건(GW 2 + Console 6) → **0건**. 사람이 개입한 지점은 계획 승인과 PR 리뷰뿐이다.

    - ⭐ **적용 결과 — Before / After** — **각 구현 담당이 작업 완료 후 직접 채운다**

      | 대상 | Before | 심각도 | After | 처리 방식 | 상태 |
      |---|---|---|---|---|---|
      | **Console · DT** | 6건 | CRITICAL 2 · HIGH 2 · MEDIUM 2 | **0건** | `next` 16.3.5 패치 · `qs` override `^6.16.0` · `js-yaml` 1건은 `Not Affected`+`Code Not Reachable` 로 심사 억제 | ✅ **완료** — PR [#14569](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14569) 머지 · 9/21 재스캔 0 확인 |
      | **Console · SQ — Security** | **A 0** · ⚠ 핫스팟 **8건 미검토**(검토율 **0%** · 등급 E) | MEDIUM 7(ReDoS 정규식) · LOW 1(하드코딩 IP) | **A 0** · 검토율 **100%** | **판정 8건** — ReDoS 7 은 `SAFE`: **입력 길이를 공격자가 정하지 못한다**(빌드 타임 환경변수·우리가 배포하는 리전 디렉터리·계약에서 생성한 경로 템플릿). ⭐ 결정적 근거는 **정적 export 라 서버가 없다**는 것 — ReDoS 의 목적인 자원 고갈이 성립하지 않는다 · 1건은 **오탐**(`6.3.1.3` 은 IP 가 아니라 목 픽스처의 **앱 버전 문자열**) | ✅ **완료** — 9/21 심사, 전건 근거 기록 |
      | **Console · SQ — Reliability** | **D 7** | HIGH 1(`sort()` 비교 함수 누락) · MEDIUM 6(정규식 우선순위 2 · Tailwind v4 CSS 2 · `alt` 문구 2) | **A 0** | **고침 5** — `sort()` 비교 함수 1 · 정규식 2(⭐ IPv6 대괄호는 **동작 결함도 함께**: `[::1` 를 조용히 정상처럼 만들던 것) · `alt` 문구 2(**한국어 번역 포함** — 영어만 고치면 정작 우리 화면에서 두 번 들린다) · **판정 2** — CSS `False Positive`(⚠ `@theme`·`@custom-variant` 는 **Tailwind v4 의 정식 문법** — 스캐너가 틀린 경우. DT `js-yaml` 을 `Not Affected` 로 둔 것과 **정반대**) | ✅ **완료** — PR [#14580](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14580)·[#14594](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14594) 머지 · 9/22 스캔에서 **A 0** 확인 |
      | **Console · SQ — Maintainability** | **A 146** | 중첩 삼항 · `role=` 대신 태그 · 중첩 템플릿 리터럴 · 인지 복잡도 등 | **A 78** (−47%) | **고침** — 중첩 삼항 1(신규 코드) · `kill-dialog` 불리언 분기 1 · **판정** — `void` 2 `Won't Fix`(일부러 안 기다린다는 표시라 빼면 실수와 구분이 안 된다) · shadcn CLI 산출물 4 = **분석 제외**(`src/generated` 와 같은 이유 — 우리가 쓴 코드가 아니다) · ⏳ **남은 78건** — 중첩 삼항 24 · `role="status"` → `<output>` 20 · 중첩 템플릿 리터럴 9 · 인지 복잡도 7 · 불필요한 타입 단언 7 · 기타 11. ⚠ **등급은 A 라 급하지 않다** — 손댈 순서는 별도 판단 | ✅ PR [#14580](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14580)·[#14590](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14590) 머지 · 등급은 계속 A |
      | **Console · SQ — Coverage** | **0.0%** — 미커버 **6337줄**(전 줄) | Gate `new_coverage ≥ 80` 실패의 유일한 원인 | **91.6%** | ⭐ **코드 문제가 아니었다** — 실제로는 처음부터 91%대였는데 **잡이 테스트를 안 돌려** lcov 가 없었고, 스캐너는 그것을 *"측정 안 함"* 이 아니라 ***"한 줄도 커버 안 됨"*** 으로 기록했다. `sonar-project.properties` 신설(lcov 경로·`sonar.tests` 분류)+Jenkins 잡에 커버리지 단계 추가로 해결 | ✅ PR [#14577](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14577)·[#14581](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14581) 머지 · Jenkins 잡 `0301f11` · ⚠ **같은 파이프라인 9개 잡 전부 0 이던 문제**였다 |
      | **GW · DT** | 2건 | MEDIUM 2(GHSA-4mjr CVSS 5.3 DoS · GHSA-x5fp 3.7 array-limit) | **0건** | `qs` override `^6.16.0` — `express` 전이 의존(쿼리 파서)이라 surgical(우리 코드 아님·patched `>=6.16.0`) | ✅ **완료** — PR [#14568](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14568) 머지 · 9/21 DT 재스캔 0 확인 |
      | **GW · SQ · Security** | A · vuln 0 · 핫스팟 검토율 **0%** | 핫스팟 21(HIGH 10·MED 5·LOW 6) TO_REVIEW | A · vuln 0 · 검토율 **100%** | 핫스팟 21 `SAFE`+근거(es-base nonroot·in-cluster 평문·anchored 정규식·redaction·docker bridge IP) — 실코드 수정 0 | ✅ SonarQube 심사 |
      | **GW · SQ · Reliability** | **D** · bugs 5 | CRITICAL 4(sort 비교함수 누락)·MAJOR 1(정규식 우선순위) | **A** · 0 | BUG 5 수정(동작 보존·configVersion 해시 code-unit 순서 유지) | ✅ PR [#14585](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14585) |
      | **GW · SQ · Maintainability** | A · code smells **≈195 추정**(전체 스캔 pre-fix·미측정) — 부분스캔 30은 오설정 아티팩트(테스트 blanket 제외·전체 미분석) | CRITICAL 다수 포함 | A · code smells **171** (전체 스캔 첫 측정·이미 아래 소거 반영·등급 A) | CODE_SMELL 20 정리 · new_violations 4 소거(optional chain 3·무단언 e2e 1) · `void` Won't Fix · **open**: S3776 복잡도 7(게이트 무관·backlog) | ✅ PR [#14588](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14588)·[#14598](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14598) · Gate PASS(new_violations 0) |
      | **GW · SQ · Coverage** | `new_coverage` **0.0** (미커버 4380줄·Gate 실패) | 배선 문제(코드 아님) | **96.5** (전체 coverage 96.3) | ADO 스캔 배선(3a) — merged lcov(unit+e2e)·main-only daily schedule·java 이미지·`sonar-project.properties` | ✅ PR [#14585](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14585)·[#14592](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14592) · Gate PASS |

      - ⭐ **"고친 것"과 "안 고치기로 한 것"이 표에 같이 있다** — 억제도 조치다. 근거를 남겨 다음 사람이 같은 것을 다시 파지 않게 하는 것이 목적이다.
      - ⚠ **억제는 오탐 처리가 아니다** — 취약점은 실재하고 스캐너가 옳다. 우리가 그 코드 경로를 타지 않을 뿐이다. `False Positive` 로 적으면 기록이 사실과 달라진다.
    - **PR [#14475](https://dev.azure.com/ewoosoft/platforms/_git/es-toolkit/pullrequest/14475) 머지**(es-toolkit) — 구현·실서버 검증 완료(심사 쓰기 왕복·데이터 원상복구)
    - ✅ **서버 설정 = DT·SonarQube 양쪽 완료** · SonarQube 개발자 온보딩 부트스트랩(`sbom/jenkins` `admin/sq_bootstrap.py`) main 머지
    - ✅ **머지 완료(9/22)** — Scott Kim 승인 · Thomas Windows 실기 검증 완료. 개발자 배포 시작 가능.
    - ✅ **첫 적용(9/17) — GW 백엔드 DT 2건 조치** (`es sec` 조회 → AI 직접 수정)
      - `qs` MEDIUM 2건 — 우리 코드가 아니라 `express` 전이 의존(쿼리 파서)이라 외부 요청에서 도달 가능
      - surgical override `qs ^6.16.0` 로 소거 — broad 범프가 아니다. [PR #14568](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14568) 머지
      - **DT 재스캔 0건 확인(9/21)** — 로컬 audit 이 아니라 **서버 보안대장 기준**
    - ✅ **Console DT 6건 조치(9/17)** — [PR #14569](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14569)
      - ⭐ **배포 형태로 갈렸다** — Console 은 **정적 export** 라 **Next.js 서버가 배포에 없다**
        - CRITICAL 2건(next RCE) = **배포본에 닿지 않음** · HIGH 2건은 빌드 타임/서버 전용
        - ⚠ **MEDIUM 2건(`qs`)만 실제 위험** — `@refinedev/core` 경유로 **브라우저 번들에 들어간다**
      - ⭐ **번들에서 실측했다** — 배포본 청크에 `qs` 고유 옵션이 있고 나머지 넷은 없다. 추정이 아니다.
      - ⚠ **next 는 배포본에 안 닿아도 올렸다** — 개발 서버는 영향받고, **DT 에 CRITICAL 이 남으면 판단이 흐려진다**
      - **결과 6건 → 0건(9/21)** — ⭐ HIGH `sharp` 도 함께 빠졌다(next 패치에 peer 가 따라 올라감)
        - 남은 **HIGH `js-yaml` 1건은 심사 억제** — `Not Affected`+`Code Not Reachable`+`Will Not Fix`
        - ⚠ **`False Positive` 가 아니다** — 취약점은 실재하고 DT 가 옳다. 우리가 그 코드 경로를 타지 않을 뿐이다.
        - ⭐ **"왜 안 고치는가"를 남기는 것이 요점** — 다음 사람이 HIGH 를 보고 다시 파지 않는다
    - ✅ **GW 백엔드 SonarQube — Quality Gate PASS(9/21)** — new_coverage 96.5 · new_violations 0 · 핫스팟 100%
      - **Gate 실패 조건은 둘 다 배선이었다** — `new_coverage 0.0` · 핫스팟 검토율 0%. 코드 품질 문제가 아니다.
      - 핫스팟 21건 심사(SAFE+근거) — **실코드 수정 0** · BUG 5건 수정([PR #14585](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14585)·동작 보존) · CODE_SMELL 20건 정리([PR #14588](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14588))
      - **`new_coverage` 0.0 → 96.5** (PL 결정 3a · [PR #14592](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14592))
        - ⚠ **Jenkins 에이전트엔 Docker 소켓이 없어 e2e 를 못 돌린다** → 커버리지가 이미 도는 **ADO 로 옮겼다**
        - ⚠ 소켓을 붙이면 잡이 **호스트 Docker 를 제어**하게 된다 — 같은 호스트에 DT·Jenkins 가 있다
        - Jenkins 기존 잡은 **트리거만 제거**(`f48341a`) — ⚠ 같은 projectKey 에 두 스캐너가 쓰면 **나중 것이 이긴다**
      - 📌 S3776 복잡도 7건 open 유지 — 판단성 리팩터·게이트 무관
    - ✅ **Console SonarQube — Quality Gate PASS(9/21~9/22)** — 커버리지 91.6 · Reliability A · Maintainability A
      - **Gate 실패 조건 둘** — `new_coverage 0.0` · `new_violations 3`
      - **`new_violations` 3 → 0** ([PR #14580](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14580))
        - 중첩 삼항 1건 = 코드 수정 · **`void` 2건 = 코드 그대로**, 근거 달아 `Won't Fix`
        - ⚠ 일부러 안 기다린다는 표시라 빼면 **"실수로 `await` 을 놓친 것"과 구분이 안 된다**
      - **`new_coverage` 0.0 → 91.6** — ⭐ **코드 문제가 아니었다.** 실제로는 처음부터 91%대였는데 **잡이 테스트를 안 돌려** lcov 가 없었고, 스캐너는 그것을 *"측정 안 함"* 이 아니라 ***"한 줄도 커버 안 됨"*** 으로 기록했다.
      - ⚠ **커버리지를 붙이자 `new_violations` 가 0 → 5 로 늘었다** ([PR #14590](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14590))
        - ⭐ **새로 생긴 문제가 아니라 안 보이던 것이 보이게 된 것이다** — 그동안 분석에서 빠져 있던 파일에 규칙이 처음 돌았다
        - **shadcn CLI 산출물 4건 = 분석 제외** — `src/generated` 와 같은 이유. ⚠ 손으로 고치면 **다음 `shadcn add` 마다 되풀이된다**
      - **핫스팟 8건 심사 — 검토율 0% → 100%**
        - ReDoS 정규식 7건 `SAFE` — **입력 길이를 공격자가 정하지 못한다** · ⭐ 결정적 근거는 **정적 export 라 서버가 없다**는 것
        - ⭐ **1건은 오탐** — `6.3.1.3` 을 IP 로 읽었는데 실제로는 목 픽스처의 **앱 버전 문자열**
      - **Reliability D → A** ([PR #14594](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14594))
        - ⚠ **등급은 개수가 아니라 가장 나쁜 항목으로 정해진다** — HIGH 1건(`sort()` 비교 함수)을 고치자 D 가 C 로 내려갔다
        - ⭐ 그래서 **"몇 건 남았나" 보다 "가장 나쁜 게 무엇인가"** 를 먼저 본다
        - **CSS 2건 = `False Positive`** — `@theme`·`@custom-variant` 는 **Tailwind v4 정식 문법**, 스캐너가 틀렸다
          - ⚠ **DT 의 `js-yaml` 과 정반대다** — 거기선 스캐너가 옳고 우리가 안 닿을 뿐이었다
        - 정규식 2건 — ⭐ **IPv6 쪽은 동작 결함도 함께** 고쳤다(`[::1` 을 조용히 정상처럼 만들던 것)
        - `alt` 문구 2건 — ⚠ **한국어 번역도 같이** 고쳤다. 영어만 고치면 정작 우리 화면에서 두 번 들린다.
      - ⭐ **덤으로 CI 결함을 하나 잡았다 — 가드가 있는데 걸린 적이 없었다** ([PR #14581](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14581))
        - `vitest.config.mts` 의 워커 상한이 `CI` 환경변수에 걸려 있는데 **CI 에서 한 번도 참이 된 적이 없었다**
        - ⭐ 그 가드는 **9/2 메모리 고갈 사고(에이전트 offline)를 막으려고** 넣은 것이다
        - ⭐ **같은 일이 반복되지 않게 설정을 검사하는 테스트를 넣었다**
      - **Jenkins 빌드 인프라 정비 — 5단계 완료(9/21 · PL 승인 후)**
        - ⭐ **근본 원인** — 공용 파이프라인이 `checkout → sonar-scanner` 뿐이라 **테스트를 돌리지 않았다**
        - ⭐ **Console 만의 문제가 아니었다** — 같은 파이프라인 **9개 잡 전부** 커버리지 0

        | | 단계 | 결과 |
        |---|---|---|
        | ① | SBOM 파이프라인의 **Node 18 강제 설치 제거** | ✅ `c60a92a` |
        | ② | 에이전트 이미지 **Node 18 → 24** + corepack | ✅ `7a3e114` |
        | ③ | **에이전트 4대 재생성** | ✅ 전부 `Connected` |
        | ④ | Console 잡에 **커버리지 단계** | ✅ `0301f11` |
        | ⑤ | `SQUBE_EXCLUSIONS` → **레포 정본 이관** | ✅ 양쪽 |

        - **Node 24 인 이유** — GW 상한 `<25`, Console 하한 `>=20.19.0`. 둘을 다 태우는 **유일한 값**
        - ⚠ 작업 중 **"켜는 순간 터졌을" 함정 3건**이 더 드러났다 — pnpm 버전 불일치 · `CI` 미설정 · 재생성 스크립트 `sudo`

        | 커버리지 | Before | After |
        |---|---|---|
        | **vt-api-gateway** | 0.0 · 미커버 **4380줄** | **96.3** · 미커버 128줄 |
        | **vt-api-gateway-console** | 0.0 · 미커버 **6337줄** | **91.6** · Gate Passed |

        - ⭐ **미커버 줄 수가 답이다** — 4380/6337 이 "전부 미커버" 로 잡히던 것이 정상 수치로 돌아왔다
      - ⚠ **Community 에디션 제약이 여기서 다 나왔다** — 브랜치 분석 없음 · PR decoration 없음
        - 그래서 **`main` 빌드에서만 스캔**한다(PR 빌드에서 스캔하면 그 PR 수치가 프로젝트 수치가 된다)
        - ⭐ **PR 단계에서 품질 피드백을 받으려면 Developer Edition 이 필요하다** — 당장은 불필요
      - **이슈 151건 분류** — BUG 5 · CODE_SMELL 146
        - ⚠ **CODE_SMELL 77건이 우리 관례와 충돌** — `void` 57 · `role="status"` 20
        - ⭐ **고칠 대상이 아니라 규칙을 조정할 대상**이다

  - ✅ **[audit 계약 정정] B-23 클로즈(9/21)** — codegen `Record<string, never>`(빈 객체) 오생성 → `Record<string, unknown>` 정정
    - 통제문서 `type: object`+`additionalProperties:true`+`nullable` (spec PR #14575·`spec-v1.0.94`)
    - 구현 gen 동조 `z.record(z.string(), z.unknown()).nullable()` ([PR #14578](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14578)·main `4190f53`)
    - 결과: `openapi:compare` **델타 0**(57 op) · Console 목 단언 우회 제거 예정 (B-22 후속)
  - **[GW·Console dev 통합 마무리]** — 남은 건 전부 외부 선결
    - ③-I: test 환경 프로비저닝(마감 8/26·미착수) · 자동배포 tag→TEST/PROD · dispatcher 안정화(exit137)
    - GW 몫(③-I 대기 아님): IoT 다운링크 E2E(dispatcher 진단→Thing enroll→webhook→IoT 1회)
    - PL 결정 대기: RTO/RPO 목표(HA 합격기준)
    - Straumann: 파일 붙은 lab order 시드(presign E2E)
  - **[제품 연동 스펙]** EzServer OnePager 수령 확인(잔여)

  - ✅ **[인프라] SonarQube 업그레이드 25.4 → 26.7 (9/22 완료)**
    - 발단 = Thomas 질의 "Rust·Dart 가 지원되지 않는다". **회귀가 아니라 처음부터 없었다.**
    - ⭐ **Rust 는 라이선스가 아니라 버전 문제였다** — Community Build **25.5** 부터 무료로 지원되는데 우리는 **25.4** 였다.
      - 그동안 Rust 프로젝트는 clippy 결과를 **외부 이슈로 밀어넣는 우회**를 썼다. 이슈는 보이지만 **라인 수·커버리지·품질 게이트가 전부 없다** — 1년 넘게 사실상 게이트가 없었다.
    - **최신(26.9) 이 아니라 26.7 로 올렸다** — 26.8 부터 PostgreSQL 15+ 를 요구하는데 우리 DB 는 **14 이고 Dependency-Track 과 공용**이다. 26.7 이면 DB 를 건드리지 않고 Rust 를 다 받는다.
    - **결과** — 프로젝트 31개 **측정값 손실 0**(업그레이드 전/후 전수 대조) · Rust 규칙 85개 활성 · 실기 스캔으로 정식 규칙 적용 확인
    - ⚠ **검증 중 더 큰 것이 나왔다 — 31개 중 9개가 「0파일 분석 + 게이트 통과」**
      - 지원되지 않는 언어이거나 분석 경로가 빗나가면 **스캔은 성공하고 화면은 초록인데 아무것도 검사되지 않는다.**
      - ⭐ **「지원 안 됨」보다 나쁘다** — 지원이 없으면 없는 줄 알지만, **초록은 검증됐다는 뜻으로 읽힌다.**
      - 대부분 Rust · Dart 2건. **업그레이드만으로는 안 풀린다** — 파이프라인 전환과 「0파일이면 실패」 가드가 필요하다.
    - ❌ **Dart 는 해결되지 않는다** — Community Build 에 **아예 없다**(Cloud·Server 상용 전용). 서드파티 플러그인은 현재 버전에서 로드되지 않는다.
      - 당분간 CI 에서 `flutter analyze` 로 직접 게이트를 건다. 정식 지원이 필요하면 **Developer Edition 결정 사안**이다.
    - 📄 매뉴얼 갱신 — `6.3 SonarQube에 테스트 커버리지 연동하기` ([VKS](https://vks.vatech.com/x/7qj9Ew)) · 언어별 속성표를 실서버 기준으로 정정(동작하지 않는 속성 2개 제거)
    - ⏳ **잔여** — Rust 파이프라인 네이티브 전환 · 0파일 가드

- 논의 사항 (이번 주 · 신규 · R#)
  - (이번 주 신규 안건 없음 — 지난주 R1은 결정되어 위 '이번 주 진행'에 반영)

- **[③-I Jack 인프라 요청 추적]** — 회의에서 상태·ETA 확인
  - ✅ **9/3 대거 착지(Jack)** — 실 IoT Core · Parameter Store(compat well-known 200) · KMS CMK(payload+target) · 공개 ingress 가 **dev 완료**.
  - admin 부팅(401) · Entra 앱 회신(9/9) 까지 겹쳐 **dev 인프라 핵심이 대부분 해소**됐다.
  - ⚠ **남은 dev 블로커** — Entra admin consent · 자동배포 · 마이그 Job · dispatcher 안정화 · test 환경.
  - 상세 = `docs/handoff/pending-infra-requests.md §9` · [PR 12653](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/12653).

  > **범례**
  >
  > - ✅ 완료 — 괄호는 완료일 · 날짜만 있으면 **이전 주 완료**
  > - 🆕 = **이번 주(9/11 이후) 신규 해결·검증** — _(아직 없음)_
  > - 🟠 부분 · ☐ 미완 · ⚠ 전달 필요
  >
  > _(9/10 주 현실화분 반영: pending-infra §9 Jack 9/3 실측 + dev 엔드포인트 재확인.)_

  | # | 요청 | 수신 | dev | prod |
  | --- | --- | --- | --- | --- |
  | 1 | Region Directory 호스팅 + `consoleHost` 발행 | ③-I | ✅ publish(8/18·`regions.gw.dev.ezcld.net`) · ✅ `consoleHost` 발행(8/31·PR #13355 Jack 머지·`curl regions.json` 확인) | ☐ 도메인 후(prod consoleHost) |
  | 2 | GW Console dev 호스팅([console.gw.dev.ezcld.net](https://console.gw.dev.ezcld.net)) | ③-I | ✅ 개통(8/19·CD 파이프라인·딥링크 rewrite) | ☐ 도메인 후 |
  | 3 | **dev GW 백엔드 배포·env 주입**(`DATABASE_URL`[공용 `common-dev-db`·`gw` DB·apne2]·`REDIS_URL`·`GW_REGION`=apne2·AWS **Pod Identity**·`NODE_ENV` 차트 주입) | ③-I | **core·receiver·dispatcher = ✅ 기동 완료**(8/31 자가검증: core·receiver 404=healthy backend·기동 확인 / dispatcher=HTTP 엔드포인트 없어 배포상 기동) · **admin = ✅ 부팅 확인(9/10: `/v1/admin/me` 401=healthy·8/31 503 해소)** · 단 **Console 실로그인은 admin consent 승인 대기**(consent 미승인→사용자 토큰 취득 불가) | ☐ |
  | 4 | **운영자 Entra 앱 등록**(GW Admin API + Console SPA·2앱·PKCE) | IT·③-I | ✅ **dev 2앱 등록·회신 완료(9/9)·GW 배선 완료** · 남은 것 = **admin consent 승인 1건**([IT-9442](https://vts.vatech.com/projects/IT/issues/IT-9442)·IT팀 승인 대기·조직 1회) → **승인 전까지 Console 실로그인 불가**(admin API 자체는 9/10 부팅 확인·401) | ☐ prod 등록 시 동일(도메인 후) |
  | 5 | **env-reference 환경별 값 채움**(test·sandbox·prod endpoint·호스트·리전) | ③-I | ✅ dev · ☐ test/sandbox/prod | ☐ |
  | 6 | **dev-seed grant** — 전용 수동 파이프라인 `gw-dev-seed.yml`(멱등·`dev:showcase`) | ③-I | 🟠 **요청 개정(PR #14269·active·9/11)** — 초안(변수그룹 `gw-dev-seed`+`DATABASE_URL` 시크릿+KMS grant)은 폐기. dev RDS가 프라이빗 서브넷이라 MS-hosted agent 로 못 닿아 **pool 을 mgmt-eks self-hosted 로 전환**하고 `DATABASE_URL` 은 **Secrets Manager `dev/vt-api-gateway-core` 에서 실행 시 조회**(변수그룹 없음). **남은 Jack 몫 = ① SC 롤에 `secretsmanager:GetSecretValue`/`DescribeSecret`(+기존 KMS) ② dev RDS SG 가 mgmt-eks 노드 대역 인바운드 허용**. 파이프라인 id 335·Environment id 9·SC `gw-dev-seed` 등록됨 ✅. ⚠ 시드가 앱 롤 `DATABASE_URL` 사용(showcase 전용 분리 롤 아님) = dev 수용 여부 PL 판단. 요청 8/20·개정 9/11. | — |
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
        - ✅ **실환경 검증으로 갭을 걷어냈다(9/15)** — 검증의 목적은 어긋난 것을 찾는 것이고, 찾은 만큼 Console 작업이 됐다
          - 🔴 **교훈** — 화면이 목만 보고 개발됐고 목이 실물보다 관대해, 지금까지 결함의 절반이 그 구멍에서 나왔다
          - `T-FE-9-17` — 1단계(목↔계약) 갭 2건 수정 → **2단계(목↔실 dev GW 16 EP) 완료(9/15)** · audit 필드 결함 수정(#14375) · targets/operators 대조는 후속
          - Entra claim→역할 매핑 · 딥링크 왕복(`?to=` 보존)도 **실 Entra + 제3자 전 경로로 검증(9/15)** — 더는 미검증 아님
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
      | **VatechAPIGateway** | 🟢 호환 게이트(§7.7) | 🟢 presigned 중계(§4.1.4) | 🟢 본체·라우팅·인증·호환 | 🟢 리전 라벨·Region Directory·HA | ⬜ AXS OAuth·Org-ID·온보딩·고정IP | ③ SRS ✅ baseline · **현행 `spec-v1.0.92`** |
      | **GW Console**(③-C) | — | — | — | 🟢 Admin Web Console(Entra 앱계층) | ⬜ 온보딩·Org-ID 후속(gw/1.1·1.2) | ✅ ③-C Sub-SRS baseline(`spec-v1.0`) → S4 |
      | **인프라** | — | — | 🟢 **dev·test·sandbox·prod(4종)** | 🟢 Route53·K8s | 🟢 AXS 고정IP·샌드박스 | 🟢 ③-I IaC 계획서(PR #11973·living doc) + KMS 키 토폴로지 |
      | **외부(Straumann AXS)** | — | — | — | — | 🟡 PPR sandbox=확보(8/11) · ⬜ prod=NDA 후 | ④ 입력(외부 제공) |

    - **스펙 문서 등록처·baseline (SSOT)**

      | 단위 | 스펙 문서 | Repo · 경로 | baseline tag |
      | --- | --- | --- | --- |
      | **③ GW** | SRS(+OpenAPI·DBML·UnitTCL) | `vt-api-gateway` · `docs/specs/` | **`spec-v1.0.92`**(현행 · baseline v1.0 동결 후 누적) |
      | **③-C GW Console** | Sub-SRS | `vt-api-gateway-console` · [docs/specs/SRS.md](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/specs/SRS.md&version=GBmain) | ✅ baseline `spec-v1.0`(8/11) · 현행 `spec-v1.0.13` |
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
  | 15 | Webhook payload 보존·아카이브 기간(리전별) | [논의] | **법무 확정 대기** — 리전별 ① DB 잔존 기간 ② S3 보관 기간(+가동 임계값). 설계 골격=SRS §7.6.9(gw/1.1)·Appendix B #5·#36 [webhook 아카이브] |
