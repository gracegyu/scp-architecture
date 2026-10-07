# VT API Gateway — 10/8 주간회의 Agenda

- **이번 주(10/8) 진행**

  - **[제품 연동 스펙] device가 연동 가능한 target을 GW에서 받는다 — 계약 신설**
    - **무엇** — 클라이언트가 target 목록과 연동 입력 폼을 하드코딩하지 않고 GW에서 받는다. **새 target이 추가돼도 클라이언트 릴리스가 없다.**
    - ✅ **스펙 확정·머지 완료** — GW `spec-v1.0.97` · Console `spec-v1.0.15`
      - [#14822](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14822) 카탈로그 신설(Thomas 승인) · [#14823](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14823) Console 표시명 편집 · [#14926](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14926) 명명 일관화(`EWC`→`CleverOne`·계약 무변경)
    - **화면·계약에서 달라진 것**
      - **표시명은 폼-universal 고정 필드로 뒀다** — `connector_type` 별 동적 필드에 섞으면 종류마다 서버가 다시 적어야 하고, **안 적은 프로파일에서는 표시명을 넣을 자리가 사라진다**
      - ⭐ **고객 노출을 폼에서 고지한다** — *"클리닉 화면에 그대로 보입니다 — 내부 메모가 아닙니다"*. 모르면 운영자가 담당자 이름·티켓 번호·`임시` 를 적고 **그게 고객 화면에 나간다**
        - ⚠ **한국어 번역을 같이 넣었다** — 운영 화면이 한국어라 영어만 고치면 **정작 읽을 사람에게 안 보인다**
      - ⚠ **표시명이 붙어도 `targetId` 를 감추지 않는다**(FR-CON-17) — 라우팅 키(`Vatech-Target` 헤더·webhook 서브도메인)라 **장애 때 로그에서 찾는 값**이다. 하나만 보이면 화면과 로그를 맞춰 볼 수 없다
      - **목은 네 행 중 둘만 표시명을 준다** — 넷 다 채우면 **폴백 경로가 목에서 한 번도 안 밟혀**, 실제 `null` 이 올 때 화면을 아무도 모른다. 공백 값 행도 하나 뒀다
      - ⛔ **값 생산 전까지 화면은 전부 `targetId` 폴백**으로 보이는 것이 정상이다 — 결함이 아니다
    - ✅ **구현 완료 — 계약 신설부터 양쪽 구현까지 이번 주에 닫혔다**(GW [#14938](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14938)·[#14965](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14965) · Console [#14933](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14933)·[#14937](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14937))
      - 운영자가 Console에서 넣은 표시명이 **클리닉 화면까지 그대로 간다**
      - ✅ **device 카탈로그 `GET /v1/clinics/me/targets` 머지 완료** — PR [#14965](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14965). **계약이 끝에서 끝까지 연결됐다**
      - ⭐ **이제 AlliedStar가 두 번째 target으로 들어올 때 클라이언트 릴리스 없이 붙는지를 실제로 검증할 수 있다** — 지금까지는 문서상 목표였다
      - **범용 불변식을 테스트로 고정했다** — org를 쓰는 프로파일인데 입력 폼이 비어 있으면 **CI가 적색**이다. 사람이 잊어도 유지된다
      - 운영자 필드 비노출은 **쿼리에서 3컬럼만 읽는 것**으로 막았다 — 거르는 코드는 빠질 수 있지만 **안 읽은 컬럼은 샐 수 없다**
      - ⚠ clinic 없는 device 엣지 케이스는 **유예**(backlog B-25·[#14966](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14966)) — v1.0은 device가 EzServer(clinic 소속)뿐이라 발생하지 않는다
    - ⭐ **구현 중에 계약 구멍 둘을 잡았다**

      | | 스펙이 안 정한 것 | 그대로 뒀으면 |
      | --- | --- | --- |
      | 1 | "미설정"이 **null만인지 공백도 포함인지** | 공백 표시명이 클리닉 화면에 **빈 칸**으로 그려져 어느 target인지 알 수 없게 된다 |
      | 2 | 길이 제한이 **trim 전인지 후인지** | 클라이언트가 막은 값을 서버가 통과시켜 **둘의 판정이 어긋난다** |

      - ⚠ **빈 문자열은 null보다 나쁘다** — 계약이 "항상 문자열"이라 약속하면 소비자가 분기하지 않으므로, **null이면 보이던 분기 지점이 사라진다**
      - **둘이 같은 형태다** — 값의 *범위*는 적었는데 **경계 판정 시점**을 안 적었다. 그리고 **둘 다 리뷰 2라운드와 승인을 통과한 문장**이었다
      - 닫는 PR [#14935](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14935)(`spec-v1.0.97`·**머지 완료**) — 쓰기에서 trim·빈 값 저장 안 함 · 투영 폴백에 공백 포함 · **문장으로만 보장하던 것을 제약으로** 부여
      - ⭐ **구현이 스펙 결함을 먼저 잡았다.** 스펙 심사가 못 거른 것을 구현이 걸렀다
    - ⭐ **AlliedStar가 GW 경유로 결정**되면서(9/28 킥오프) **두 번째 target이 실제로 들어온다** — 가변 target 설계가 문서상 목표가 아니라 당면 요건이 됐다
    - ⚠ **"target 추가 = 무변경"의 경계도 스펙에 못 박았다** — 라우팅·목록·입력 폼·org 등록·하행 배선은 GW가 흡수하지만 **그 target과 주고받는 데이터(필드 매핑·영상 이동·이벤트 처리)는 클라이언트 개발이 남는다**
      - 판별 기준 = **누가 요청을 시작하나.** 클라이언트가 시작하고 EzServer가 통과만 시키면 **EzServer 무변경**이고 그 클라이언트만 바뀐다
      - AlliedStar 1차(EzDent-i·CleverOne에서 촬영 실행)가 이 형태라 **EzServer 무변경이 성립할 가능성이 높다** · 2차(촬영 데이터를 EzServer에 저장)부터는 개발이 든다

  - **[도메인] 베이스 도메인 확정값 — 문서 정합화**
    - **확정(2026-09-17·③-I)** — ⭐ **외부에 노출되는 환경은 `ezcld.com`, 사내 전용은 `ezcld.net`** 이고 **prod은 환경 라벨을 붙이지 않는다**

      | 환경 | 위임 zone | API 호스트(예) | Console |
      | --- | --- | --- | --- |
      | **prod** | `gw.ezcld.com` | `api.<region>.gw.ezcld.com` | `console.gw.ezcld.com` |
      | **sandbox** | `gw.sandbox.ezcld.com` | `api.<region>.gw.sandbox.ezcld.com` | `console.gw.sandbox.ezcld.com` |
      | dev | `gw.dev.ezcld.net` | `api.apne2.gw.dev.ezcld.net` | `console.gw.dev.ezcld.net` |
      | test | `gw.test.ezcld.net` | `api.apne2.gw.test.ezcld.net` | `console.gw.test.ezcld.net` |

    - ⚠ **SRS에는 반영돼 있었는데 env-reference·handoff 문서가 「도메인 미정」인 채로 남아 있었다** — 그대로 두면 인프라 요청서를 받는 쪽이 아직 안 정해진 것으로 읽는다
    - ✅ 정합화 **머지 완료** — [#14831](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14831)(GW) · [#14832](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14832)(Console) · **계약·화면 무변경**(spec 태그 미증가)
    - ⭐ **풀린 것** — **test·sandbox·prod Entra 앱 등록이 지금 가능**해졌다. "호스트 확정 후"로 묶여 있었는데 도메인이 정해져 **프로비저닝 전에도 등록할 수 있다**
    - **prod 잔여는 도메인이 아니라 ③-I의 zone 위임·인증서 프로비저닝**이다

  - ✅ **[보안] 취약점 14건 → 0건 조치 완료 — 다만 ⚠ 근본 원인이 따로 있다**

    9/21~22에 GW·Console 둘 다 **0건**으로 만들었는데 2주 만에 다시 올라왔다.

    | | 9/21~22 | 현재 | 내역 |
    | --- | --- | --- | --- |
    | **GW** | 0 | **12건** | CRITICAL 1 · HIGH 3 · MEDIUM 7 · LOW 1 |
    | **Console** | 0 | **2건** | CRITICAL 1 · HIGH 1 |

    - ⭐ **핵심은 건수가 아니라 패턴이다 — 「0건 달성」은 상태가 아니라 그 시점의 사진이었다**
      - **14건 전부 전이 의존**이다. 우리가 쓴 코드가 아니다
      - 상당수가 **지난번에 이미 올려 둔 버전에 새 advisory가 붙은 것**이다 — 올려도 또 뜬다
      - ❓ **그래서 물을 것은 "지금 0으로 만들자"가 아니라 "어느 주기로 볼 것인가"다.** 지금은 사람이 생각났을 때 보는 구조다
      - GW 자체 게이트(`pnpm audit --prod`)와 **DT가 정확히 일치** — 스테일 BOM이 아니라 현재 락파일에 실재한다

    - ⭐ **CRITICAL 둘 다 배포본의 신뢰 경로에 닿지 않는다 — 이유가 서로 다르다**

      | | 무엇 | 왜 안 닿나 |
      | --- | --- | --- |
      | GW | `proxy-addr` IP 스푸핑 | ⭐ **세 겹이 이미 막고 있다** — ① SRS §7.6이 webhook 인증을 **HMAC+timestamp**로 두고 source IP를 **명시적으로 비-신뢰**(allowlist는 방어심층)로 규정 ② **`trust proxy`가 꺼져 있어** XFF를 신뢰하지 않는다(스푸핑 벡터 휴면) ③ `req.ip`의 **유일한 쓰임이 rate-limit 키**인데 그 함수가 **이미 `::ffff:` 접두를 제거**한다 — 바로 이 CVE의 벡터다 |
      | Console | `next/og` RCE | **정적 export라 서버가 없다** · 번들 8.2MB에서 고유 표지 **0건** 실측 |

      - ⭐ **GW 쪽은 설계 결정이 값을 한 사례다** — "식별은 Host/SNI, 인증은 HMAC, source IP는 방어심층"으로 갈라 둔 덕에 이 CVE가 인증을 건드리지 못한다
      - ⚠ **그래도 「조치 불요」로 끝낼 일은 아니다** — 개발 서버는 영향받고, **DT에 CRITICAL이 남으면 다음에 진짜가 왔을 때 판단이 흐려진다**(9/21 `next` 때와 같은 논리)
      - 억제로 둘 거면 **`False Positive`가 아니라 `Not Affected`** 다 — 취약점은 실재하고 우리가 그 경로를 신뢰하지 않을 뿐이다

    - 🛑 **그리고 이건 보안 지표만의 문제가 아니었다 — `main` CI가 막혀 있었다**
      - GW CI의 `pnpm audit --audit-level high` 게이트를 그 12건이 막아 **`main`과 전 PR이 적색**이었다([#14938](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14938) 포함)
      - ⭐ **즉 "언젠가 정리할 위생 작업"이 아니라 개발을 세우고 있던 것이다.** 지표로만 보면 안 보이는 비용이다

    - ✅ **양쪽 조치 완료 · DT 서버 기준 0 확인(10/7)**

      | | PR | 조치 | DT 현재 |
      | --- | --- | --- | --- |
      | **GW** | [#14952](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/14952) | surgical override 6줄 → 12건 소거 | 컴포넌트 **424 · findings 0** |
      | **Console** | [#14950](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console/pullrequest/14950) | `next` 16.3.5→**16.3.8** · `source-map-js` 1.2.1→1.2.2 | 컴포넌트 **260 · findings 0** |

      - `proxy-addr` CRITICAL은 **억제가 아니라 패치로 닫았다** — 전건 패치가 있어 억제 기록을 남길 일이 없어졌다
      - `next`는 최소 패치가 아니라 **최신 16.3.8**로 갔다 — 같은 비용에 그 사이 패치가 함께 들어온다. ⭐ **시각 회귀까지 통과**해 "breaking 없음"이 추정이 아니라 확인이다
      - `source-map-js`는 **override 없이 lockfile 갱신만** — `postcss`가 `^1.2.1`을 요구해 1.2.2가 이미 범위 안이었다

    - ⭐ **「0」을 어떻게 확인했는지가 숫자보다 중요하다** — 업로드 직후 조회는 분석이 안 끝나 0으로 보일 수 있다. 세 가지로 갈랐다
      - **지표가 새 BOM 기준으로 재계산됐다** — 재계산 시각(10:56:52)이 BOM 반입 시각(10:55:37)보다 **뒤**다
      - **조회 자체가 깨진 게 아니다** — 같은 방법으로 다른 프로젝트를 보면 311·302·519가 그대로 나온다
      - ⚠ **첫 조회는 컴포넌트를 100개에서 끊어 먹고 있었다**(260개 중). 그 상태로는 **고친 패키지가 "없음"으로 보였다** — 전수로 다시 봤다
      - ⭐ **"0을 보고했는데 실은 안 본 것"이 0이 아닌 것보다 나쁘다**

    - ⭐ **14건 전부 패치가 나와 있었다 — 「패치 없음」이 0건이었다.** 그래서 이번 결정은 "고칠 수 있나"가 아니라 "언제·누가"였다

      | | 건 | 현재 → 패치 | 조치 |
      | --- | --- | --- | --- |
      | GW | `proxy-addr` CRITICAL | 2.0.7 → **≥2.0.8** | ✅ **override 6줄**로 12건 전건 소거(#14952 머지) |
      | GW | `brace-expansion` HIGH 3건 | 5.0.9 → **≥5.0.12** | 〃 |
      | GW | `@grpc/grpc-js` HIGH·LOW | 1.14.4 → **≥1.14.5** | 〃 |
      | GW | `ip-address` MED 4건 | 10.4.0 → **≥10.7.1** | 〃 |
      | GW | `multer`·`js-yaml` MED | → **≥2.4.0** · **≥5.4.1** | 〃 |
      | Console | `next` CRITICAL | 16.3.5 → **16.3.6**(최신 16.3.8) | 직접 의존 범프 · 같은 마이너라 breaking 없음 |
      | Console | `source-map-js` HIGH | 1.2.1 → **1.2.2** | ⭐ **lockfile 갱신만** — `^1.2.1`이 이미 허용. override 불요 |

    - ⚠ **지금 올려야 하는 이유가 하나 더 있다** — ③-I가 배포에서 `trust proxy`/XFF를 켜면 **그 순간 `proxy-addr`의 정확도에 하중이 걸린다**. 켜기 전에 올려 두는 것이 맞다

    - ✅ **①은 결정·실행됐다**(PL 승인·GW 머지 완료·Console 진행) — **남은 것은 ②다**

    - 🛑 **근본 원인 — SBOM 스캔이 제품 코드를 보고 있지 않다**

      조사해 보니 **"어느 주기로 볼 것인가"가 아니라 "무엇을 보고 도는가"**가 문제였다.

      - SBOM 잡의 트리거가 `TimerTrigger`(cron)가 **아니라 `SCMTrigger`(폴링)** 다. `H 18 * * *`은 **빌드 주기가 아니라 폴링 주기**이고 **변경이 없으면 안 돈다**
      - ⚠ **그런데 폴링 대상이 Jenkinsfile이 있는 레포다.** 스캔 대상 제품 레포는 스크립트가 **자체 clone**으로 가져와 **Jenkins는 그 존재를 모른다**
      - **확인한 SBOM 잡 16개 전부** 같은 구조다
      - ⭐ **그래서 마지막 실행이 10/1이었다** — 그 레포의 마지막 커밋이 9/30이었고 그날 폴링이 그걸 변경으로 봤다. 이후 커밋 0건이라 **6일간 아무것도 안 돌았다**
      - 🛑 **지금 사내 SBOM은 담당자의 문서 커밋이 갱신하고 있다.** 제품 코드가 아무리 바뀌어도 그 레포가 가만히 있으면 DT는 멈춰 있다

      > **그래서 "주기를 짧게 잡자"는 답이 아니다.** `H 3`으로 바꿔도 그 레포에 커밋이 없으면 안 돈다.

    - **묵은 정도** — 7일 이상 갱신 없는 프로젝트 **27/53**(active 기준·주 수치) · 전체 기준 41/67
      - ⓘ `active`=DT의 활성 플래그. **inactive는 묵은 게 정상**이라 분모에 넣으면 과장이 된다

    - ❓ **결정 필요 — 트리거 구조를 고칠 것인가**
      - ⚠ **잡 16개 전부에 영향**이라 임의로 손대지 않았다
      - GW는 CI에 `audit --audit-level high` 게이트가 **이미 있어** 이번에 감지는 됐다. 다만 신호가 **"빌드 실패"로만 와서 보안 사안인 줄 모르고 보게 된다**
      - 즉 선택지는 ① SBOM 트리거를 제품 레포 기준으로 고치기 ② CI 게이트 신호를 보안 알림으로 분류하기 ③ 둘 다

  - **[인프라] Jenkins · DT · SonarQube · 백업**

    - 🔴 **SonarQube 분석 토큰이 빌드 로그에 평문으로 남아 있다 — 로그 파일 102개**
      - Linux(`sh` 가 기본 `-x` 라 전개된 줄을 찍는다) · Windows(`bat` 에 `@echo off` 가 없어 cmd 가 치환 뒤 에코한다) **양쪽 다**
      - ⭐ **코드는 변수로 감쌌는데도 샌다** — 감싼 의미가 **에코 단계에서 사라진다**. 변수로 쓰면 안전하다는 가정이 틀린 자리다
      - SonarQube 잡 전부가 **같은 토큰 하나**를 쓴다. 빌드 로그를 볼 수 있는 사람 전원에게 노출된다
      - ⚠ **`withSonarQubeEnv` 가 마스킹한다는 가정도 틀렸다** — 로그 전체에서 `****` 는 3건뿐이고 전부 SVN 자격증명이다
      - ✅ **코드 수정 완료(10/7·`5d6bde3`·5개 지점)** — Linux 는 `set +x`, Windows 는 `@echo off`
        - ⭐ **두 곳은 에코를 꺼도 안 막혔다** — Groovy 가 토큰 값을 **문자열에 직접 박고** 있었다. 그건 로그뿐 아니라 **에이전트의 임시 스크립트 파일에도** 평문을 남긴다. 변수 참조로 바꿨다
        - ⚠ **근본 수정(토큰을 명령줄에서 제거)은 못 했다** — 설치된 `sonar-scanner-cli 5.0.1` 이 `SONAR_TOKEN` 환경변수를 모른다. `-Dsonar.token` 을 빼는 대안은 **9개 잡이 동시에 걸리는데 잡을 돌려 확인할 수단이 없어** 택하지 않았다. 스캐너 업그레이드 때 다시 본다
      - 🔴 **남은 것은 토큰 폐기다 — 코드를 고쳐도 이미 찍힌 102개는 남는다.** 콘솔 작업이라 사람 몫(진행 중)

    - **백업 S3 계정 이전 완료(10/7)** — `533267126003` → `118688039229`
      - 과거분은 옮기지 않고 새 버킷에 오늘부터 쌓는다 · 전송 31개·실패 0·2.71GB · 옛 버킷과 **바이트 완전 일치** · 복구 경로(내려받기→`gzip -t`→원본 `cmp`)까지 실증
      - ⚠ **처음 받은 키는 인증은 됐는데 계정이 달라 전부 AccessDenied 였다.** `sts get-caller-identity` 만 보고 넘어갔으면 **다음 백업부터 조용히 실패**했을 것이다 — 인증 성공과 쓰기 권한은 별개다
      - ⚠ **전송 상태 파일이 어느 버킷에 보냈는지 모른다** — 그대로 뒀으면 전부 "이미 보냄" 으로 건너뛰어 **새 버킷이 빈 채로 초록불**이 떴을 것이다
      - ❓ **새 버킷의 수명주기·버전 관리 확인 필요(Jack)** — 최소 권한이라 호스트에서 읽을 수 없다. 빠져 있으면 조용히 쌓인다(옛 버킷이 그 실수로 1년간 184GB)
      - ⚠ **옛 계정 정리 시점** — 새 버킷에는 로컬에 있던 10세트만 들어갔다. 그보다 오래된 복구 지점은 **옛 계정에만** 있다. 2~3주 쌓인 뒤가 안전하다
      - PR [#14968](https://dev.azure.com/ewoosoft/sbom/_git/bm2databackup/pullrequest/14968) · [#14969](https://dev.azure.com/ewoosoft/sbom/_git/bm2databackup/pullrequest/14969) **둘 다 머지**
      - ⭐ **배포하며 결함 하나를 더 찾았다** — `restore3_services.sh` 가 `100644` 라 RUNBOOK 대로 `./` 로 부르면 Permission denied 였다. **복구 3단계가 통째로 막혀 있었다**(#14969). 9월에 `ship` 스크립트가 같은 이유로 cron 에서 조용히 죽은 적이 있는데 **같은 결함이 하나 남아 있었다**

    - **BM2 복구 — 가장 위험한 항목은 검증됐다, 전체 시연은 아직**
      - 운영에 영향 없이 격리 컨테이너로 DT 를 실제 기동해 **암호화 키 복호화까지 확정**했다. ⭐ **DB 만으로는 DT 가 복구되지 않는다**(API 키·연동 자격증명이 암호화돼 있다)는 것이 추정이 아니라 확인이 됐다
      - 남은 것은 `restore1→2→3` 전체 시연이고 **격리 VM 이 필요하다**

    - **`EzServer-SonarQube` 8연속 실패 — 담당 Thomas, 진단 전달 완료**
      - 9/16 Rust/Dart 를 Windows 에이전트로 옮긴 뒤부터다. Windows 구간 뒤 **첫 Linux `sh` 가 기동되지 않아**(`process apparently never started`) 뒤 6개 스테이지가 전부 스킵된다
      - 노드·디스크·메모리·권한·시계·연결은 실측으로 배제했다. 같은 노드에서 다른 잡은 성공한다

    - **SonarQube** — Rust 파이프라인 네이티브 전환 · ⚠ **「0파일 분석인데 게이트 통과」 가드**(31개 중 9개 — 초록이 검증됐다는 뜻으로 읽힌다) · ⓘ org-wide·Jack 소관(*vt-api-gateway 자체는 실파일 분석이라 해당 없음*)
    - **Dependency-Track** — DT 프로젝트가 없는 SBOM config 2건 삭제 [PR #14635](https://dev.azure.com/ewoosoft/sbom/_git/jenkins/pullrequest/14635) **머지 완료**(9/22)


- **남은 작업 — 전부 외부 선결** (⭐ **GW·Console 코드로 앞당길 잔여 = 0**)

  | # | 남은 작업 | 우리 쪽 상태 | 막는 것 | 소유 |
  | --- | --- | --- | --- | --- |
  | 1 | **Entra admin consent 승인** | ✅ dev 2앱 배선 완료 · admin API 부팅 확인(401) | 🔴 [IT-9442](https://vts.vatech.com/projects/IT/issues/IT-9442) 승인 1건(조직 1회) — **미승인이라 Console 실로그인 불가** | IT·③-I |
  | 2 | **test 환경 프로비저닝** | — | 🔴 요청 완료 · **마감 8/26 · 미착수** | ③-I |
  | 3 | **IoT 다운링크 E2E**(webhook→IoT 1회) | ✅ 수신·dispatcher drain·멱등 · ingress·IoT Core 완료(9/3) | 🟢 **착수 가능 · GW 몫** — 단 dispatcher exit137 진단에 **dev EKS 접근**이 필요(현 자격에 클러스터 0) | GW · ③-I(접근 개방) |
  | 4 | 자동배포 tag→TEST/PROD | main→DEV는 **실동작 확인** | #2 (환경 생기면 태그 트리거만 추가) | ③-I |
  | 5 | 부하 실측 · HA 실측 | ✅ 하네스·스크립트·파이프라인 | #2 **+ RTO/RPO 목표 미확정** | ③-I · **PL** |
  | 6 | presign E2E(환자문서 order-file) | ✅ create/download 실측 | 파일 붙은 lab order 시드 | Straumann |
  | 7 | Console 배포 보안 헤더(CSP·HSTS 등) | ✅ 8/26 실측 — **전부 부재** 확인 | CloudFront response headers policy 미배선 | ③-I |
  | 8 | Console prod 배포 | ✅ 프리뷰 배포 파이프라인 | prod 도메인 | PL · ③-I |
  | 9 | dev 재배포·재시드 | ✅ 계약 양쪽 머지 완료 | **dev에 안 떠 있어** 실화면 확인 불가 | ③-I |

  - 🔴 **최우선 블로커 둘 — 회의에서 밀 것**
    - **① Entra admin consent** — 풀리면 dev 통합검증이 통째로 풀린다
    - **② test 환경** — 풀리면 **부하·HA 2건이 동시에 해제**된다(#4·#5)
  - ❓ **PL 결정 대기 = RTO/RPO 목표**(HA 합격기준) — 환경이 생겨도 이것 없이는 #5를 끝낼 수 없다

- **논의 사항 (이번 주 · 신규 · R#)**
  - _(10/1 회의 결정사항 반영 후 확정)_

- **공유 사항** (결정 아님 · 논의사항인지 애매한 것을 임의 결정해 공유 · 매주 상시)

  - **[품질] SonarQube — 양쪽 다 전 항목 A 유지**

    | | Gate | Coverage | Security | Reliability | Maintainability |
    | --- | --- | --- | --- | --- | --- |
    | **GW** | OK | 96.5 | A · 핫스팟 **100%** | A | A |
    | **Console** | **OK** | **91.6**(신규 코드 92.1) | A · 핫스팟 100% | A | A · **78→53** |

    - ⭐ **Console 78 → 53은 고친 것이 아니라 판정이다**(아래 근거). P14 신규 코드(~500줄)는 unit+e2e가 촘촘해 **커버리지 플로어에 영향 없다**
    - ⚠ GW 수치는 **마지막 main 스캔 기준**이고 그 뒤 새 스캔 근거를 사내 도구로 가져오지 못했다 — **대시보드 재확인 권장**(바뀌었을 가능성은 낮다)
    - ⭐ **"고친 것" 과 "안 고치기로 한 것" 을 가른 것이 요점이다** — 판정도 조치이고, 근거를 남겨 **다음 사람이 같은 것을 다시 파지 않게** 한다
      - **`void` 55건** — 일부러 안 기다린다는 표시다. 떼면 *"실수로 `await` 을 놓친 것"* 과 **구분이 안 된다**. ⚠ 규칙이 틀렸다고 적지 않았다 — 그 위험은 **`no-floating-promises` 로 떠다니는 프라미스 자체를 막는 쪽**이 맞고 도입은 별도 판단으로 뒀다
      - **`role="status"` 16건** — 규칙이 제안하는 `<output>` 은 **인라인 요소**라 바꾸면 시각 baseline 이 대거 흔들린다. 접근성 결과는 같고(암묵 role 이 `status`) axe 테스트도 통과 중이다
      - **CSS 2건은 `False Positive`** — `@theme`·`@custom-variant` 는 **Tailwind v4 의 정식 문법**이다. ⚠ DT 의 `js-yaml` 을 `Not Affected` 로 둔 것과 **정반대 경우**다 — 거기선 스캐너가 옳았고 여기선 틀렸다. **섞어 적으면 기록이 사실과 달라진다**
      - **핫스팟 ReDoS 7건은 `SAFE`** — 입력 길이를 공격자가 정하지 못한다(빌드 타임 env·우리가 배포하는 리전 디렉터리·계약에서 생성한 경로 템플릿). ⭐ 결정적 근거는 **정적 export 라 서버가 없다**는 것 — 자원 고갈이 성립하지 않는다
      - ⭐ **1건은 오탐이었다** — `6.3.1.3` 을 IP 로 읽었는데 **앱 버전 문자열**이었다
    - ⚠ **위 「0파일 분석인데 게이트 통과」 와 같은 집안 문제였다** — Console 커버리지가 0 이던 것도 **잡이 테스트를 안 돌려서**였지 코드 문제가 아니었다. 스캐너는 *"측정 안 함"* 을 ***"한 줄도 커버 안 됨"*** 으로 기록한다
    - ⚠ **코드를 안 바꿨는데 수치가 움직인다** — 9/22 스캔에서 유지보수성이 78 → 124 로 늘었다(제외 범위가 걷히며 8월 이슈가 돌아옴). **등급은 개수가 아니라 가장 나쁜 항목으로 정해지므로**, 건수 추이만 보면 오독한다

  - **S1. 프로젝트 일정(Gantt) — 10/8 스냅샷**
    - **진행률(구현)** — GW ≈ 93% · Console ≈ 92%. **둘 다 코드 feature-complete**이고 잔여는 전부 위 표의 외부 선결이다
    - ⚠ **9/30 「개발환경 연동 완료」 목표를 넘겼다** — 원인은 코드가 아니라 **Entra consent·test 환경** 둘이다. 10월 출시 목표를 유지할지 **일정 재설정이 필요**하다
    - **범례** — 막대: 작성=기본·PR=강조·◆=baseline/마일스톤·**빨강=외부/미정 선결**

    ```mermaid
    gantt
        title v1.0 = Straumann(AXS) 첫 외부연동 · 10월 출시 목표 (10/8 현재)
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

  | # | 항목 | 타입 | 상태 |
  | --- | --- | --- | --- |
  | 4 | Webhook 클라우드 분배(CleverLab 갈래B) | [논의] | v1.0 제외 — Open 후 결정 |
  | 6 | AXS **prod** 자격(Straumann 정식계약) | [정보] | PPR sandbox=확보(8/11) · prod=NDA 후 |
  | 7 | 경로 B EOS 시점 | [논의] | EOS 시점만 PM·CS/CO OnePager 미정 |
  | 8 | v1.0 목표 RPS·동시 세션 | [논의] | 목표치 확정 필요 · test 환경 후 실측 [부하] |
  | 9 | RTO/RPO·유지보수 윈도우 | [논의] | ❓ **PL 결정 대기** — HA 합격기준. 환경이 생겨도 이것 없이는 HA 실측을 끝낼 수 없다 [HA] |
  | 10 | 감사·consent 보존 기간 | [정보] | 법무 확인 대기 |
  | 11 | 호환성 매트릭스 확정본 | [정보] | CleverSpace/CleverOne OnePager 의존 — 담당팀 baseline 후 |
  | 15 | Webhook payload 보존·아카이브 기간(리전별) | [논의] | **법무 확정 대기** — 리전별 ① DB 잔존 기간 ② S3 보관 기간(+가동 임계값) |
