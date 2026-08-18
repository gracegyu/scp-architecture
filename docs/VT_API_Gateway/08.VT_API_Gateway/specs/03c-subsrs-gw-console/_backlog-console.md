# GW Console(③-C) Sub-SRS 백로그

> **목적.** Console SRS(`SRS.md`)에 **앞으로 반영할 변경**을 추적한다(지금 당장 손대지 않고 트리거 시 반영).
>
> **구분(중요).**
> - **이 백로그** = Console SRS에 *아직 없는, 앞으로 넣을* 변경.
> - **SRS Appendix B** = SRS에 *이미 있는* 미결·확인(TBD) 항목(C-1~).
> - **부모 백로그**(`../03-srs-gateway/_backlog-parent-srs.md`) = 부모 GW SRS/OpenAPI/DBML 변경.

## 상태 범례
- **대기** — 트리거 전 · **준비됨** — 트리거 충족·반영 대기 · **완료** — 반영

---

## 다음 할 일 — 열린 액션 색인 (2026-08-18 기준)

> **이 절의 목적.** "다음 할 일이 뭐야"에 한 곳에서 답하기 위한 **색인**이다. 상세는 각 정본(IP Task 카드·SRS Appendix B)에 있고 여기서는 **누가 막고 있는지**만 적는다 — 중복 기재하면 어긋난다.
>
> **현재 상태: 구현 세션이 무인으로 더 진행할 Task는 없다.** IP 48/52 완료, 잔여 4건은 전부 외부 선결 대기다.

### A. PL이 지금 바로 할 수 있는 것 — `[manual]` 2건 (+1 해소)

자동 테스트로 증명할 수 없어 사람이 1회 확인해야 하는 항목이다. **셋 다 코드·자동 테스트는 완료**돼 있고 확인만 남았다.

| # | 무엇 | 확인 경로 | 근거 |
|---|---|---|---|
| A-1 | **kill 다이얼로그 오조작 방지** — 문구·2차 확인·감사 노출이 실제로 사람을 멈추게 하는가 | `/devices/detail?id=dev-active-0&mock=operator` → [상태·수명주기] → "긴급 정지" | `T-FE-2-5` dod `[manual][risk:auth]` |
| A-2 | **PHI·자격 실검사** — devtools로 저장소·네트워크·콘솔에 원문이 남지 않는지 + CSP 적용 | 체크리스트 = `vt-api-gateway-console/docs/security-review-checklist.md` **§2**(항목별 체크박스 준비됨) | `T-FE-7-6` dod `[manual][risk:security]` |
| A-3 | **시각 baseline 승인** | ✅ **기계적 부분 완료** — linux 17종 커밋 · `continueOnError` 제거 → **차단 게이트** 전환(PR #12744). baseline은 구현 세션이 열어 확인했다(dev 배지 제거·리전 표시명이 실물 Directory와 일치). ⚠ **최종 미관 판단은 여전히 PL 몫**이며, 하려면 `tests/visual/__screenshots__/linux/` 17장을 보면 된다 | `T-FE-8-3` dod `[manual]` |

### B. CI 게이트 — ✅ **해소 (2026-08-18)**

PR #12744(머지 `5331365`)로 **CI가 실제 문지기가 됐다.** `T-FE-0-8` dod 충족.

| # | 무엇 | 상태 |
|---|---|---|
| B-1 | 파이프라인 등록 — `vt-api-gateway-console-ci` (definition **334**) | ✅ |
| B-2 | main 브랜치 정책 **Build validation(차단·만료 즉시)** | ✅ PL 등록 · PR #12744에서 `approved`·차단=True 평가 확인 |
| B-3 | linux 시각 baseline 17종 확정 | ✅ 커밋 완료 → 시각 회귀도 **차단 게이트** |

**등록 전까지의 상태**: `azure-pipelines.yml`이 레포에 있을 뿐 Azure DevOps에 등록되지 않았고 main 브랜치 정책도 0건이었다. **CI가 한 번도 돈 적이 없었다** — 그동안의 품질 근거는 전부 구현 세션의 로컬 실행이었다(무인 auto-complete 머지 포함).

#### ⚠ 첫 CI가 잡은 것 — 로컬 8종 게이트로는 구조적으로 못 잡는 결함 4건

| # | 결함 | 왜 로컬이 못 잡나 |
|---|---|---|
| 1 | 생성물 헤더에 **로컬 파일 경로**가 박혀 `codegen --check`가 환경 종속 | 로컬은 우회 경로(`/tmp/...`), CI는 형제 체크아웃 → **계약이 같아도 drift**. 한 환경에서만 돌면 영원히 안 보인다 |
| 2 | CI 계약 핀이 **`spec-v1.0.20`**으로 낡음(생성물은 v1.0.26) | 핀은 파이프라인에만 있고 로컬은 형제 레포 HEAD를 본다 |
| 3 | Playwright CI 설정 3종(**`forbidOnly`**·`retries`·html 리포터)이 Azure에서 통째로 죽음 | `process.env.CI`만 봤는데 **Azure는 `TF_BUILD`를 세팅한다.** `forbidOnly`가 죽어 있으면 `test.only` 하나로 **나머지 e2e가 조용히 안 돌고 CI는 초록**이 된다 |
| 4 | 시각 회귀 임계 `maxDiffPixelRatio: 0.01`(≈9,200px)이 과도하게 관대 | 리전명 변경·dev 배지 소멸·감사 2줄 증가가 전부 "같다"로 통과. `maxDiffPixels: 100`으로 교체(AA 잡음 0 실측) |

> **교훈**: CI가 없으면 **CI 전용 설정이 작동하는지도 아무도 모른다.** 3·4는 게이트가 있다고 믿는 상태에서 실제로는 아무것도 안 지키던 경우다.

### C. 외부 선결 대기 — P8 4건 (정본 = IP Task 카드)

| Task | 막는 것 | 소유 |
|---|---|---|
| `T-FE-8-1` Entra dev 전환 | **C-2** 테넌트·앱 등록 | IT |
| `T-FE-8-2` staging 실연동 | staging GW 배포 · **C-3** CORS | ③-I |
| `T-FE-8-3` baseline 승인 | 사람 판단(위 A-3) | PL |
| `T-FE-8-4` prod 배포 | **C-10** 도메인 확정 · **BLOCKER** | 회의·③-I |

> ⚠ **2026-08-18 — 새 활성 블로커**: dev 프리뷰 배포가 **CloudFront viewer-request Function 없이는 배포돼도 앱이 안 돈다**(딥링크·`/auth/callback` 전부 홈으로 떨어짐 · 실측 2회). 소유 = **③-I Jack**. 상세·근거·배포 후 확인 절차 = 아래 **§5)**. 요청서 정정은 **PR #12752**로 올려 뒀다.

> `T-FE-8-4`는 도메인이 확정돼도 **무인 대상이 아니다** — IP §7 Operating Mode가 "prod 배포 자동 실행 금지"로 명시적으로 제외한다.
>
> `T-FE-8-2`는 dod가 허용한 **MSW 대체 커버가 이미 적용**돼 있다(`tests/e2e/staging/README.md` — 여정별로 *목이 증명하지 못하는 것*까지 적어 뒀다).
>
> **2026-08-18 — Region Directory dev 실물이 떴다**(③-I publish): `https://regions.gw.dev.ezcld.net/regions.json`. 스키마 §7.3.6 정합 확인됨(`apne2`·`KR`·`active`·`api.apne2.gw.dev.ezcld.net`·`{target}.webhook.apne2.gw.dev.ezcld.net`). `T-FE-8-2`에서 로컬 스텁 대신 이 URL로 리전 컨텍스트를 검증한다.
>
> ⚠ **로컬 개발은 그대로 `GW_ADMIN_BASE`를 쓴다** — 단일리전 로컬에서 Directory host로 덮으면 즉시 죽는다.
> ⚠ **`adminHost`는 Directory 스키마에 여전히 없다**(실물에서도 확인). 지금은 DNS 관례/env로 가고 별개 스펙 건으로 추적 중이다.

### D. 결정이 나면 생기는 후속 구현 — 4건 (전부 비차단)

지금은 잠정값으로 동작 중이라 **화면은 정상**이다. 결정이 나면 **상수·훅만** 손보면 된다.

| 항목 | 지금 | 결정 후 할 일 |
|---|---|---|
| **C-5** break-glass 열람 역할 | **잠정 admin만**(PHI라 넓히는 쪽 오류는 되돌릴 수 없어 최소로) | `permissions.ts`의 `webhook-events.payload.view` 부여 역할 + 매트릭스 테스트 행 갱신 |
| **C-11** 서버 낙관적 잠금 | 클라이언트측 stale-write **감지**(`useStaleWriteGuard`) | 서버가 `expectedVersion`+409를 강제하면 **훅을 걷어낸다**(방지가 아니라 감지였다) |
| **C-12** 정렬 계약 | GW 기본 정렬에 의존(정렬 파라미터 없음) | 파라미터가 생기면 목록 화면에 배선 |
| **C-17** operator/developer 매트릭스 | draft 매트릭스로 UI 게이팅(서버 강제는 GW) | 확정되면 §7.2 매트릭스 상수 + `permissions.test.ts` 기대표 갱신 |

### E. 스펙 세션 작업 대기 — 1건 (Console 구현 영향 없음)

| 항목 | 내용 |
|---|---|
| **FR-CON-12 문구 정정** | `*멱등:* 이미 revoked면 재-kill은 무효(상태 표시)` — **FR-CON-10과 같은 형태의 모호함**이다("무효"의 주어가 UI인지 서버인지 없음). GW 확인 결과 종단 상태 kill도 **409**다(`kill()`이 `PATCH→revoked`와 **같은 경로**·`assertTransition` 통과). FR-CON-10(#12728)과 같은 방식으로 정정 예정. **Console 구현 영향 없음** — 목은 이미 409이고 UI는 종단 상태에 kill 버튼을 두지 않는다. |

---

## 백로그 항목

> **현재 열린 항목 없음** — CB-1~CB-4 전부 반영·해소(아래 완료 이력). 새 변경이 생기면 여기에 CB-5~ 로 추가한다.

---

## 완료·반영 이력

- **CB-1**(멀티리전 운영자 authz·ZTNA 제거→Entra) · **CB-2**(v1.0 최소기능 선행·기술 스택 확정) — ✅ **SRS baseline 반영 완료**(상세=git 이력).
- **CB-3**(감사 로그 대상 리소스 축 부재) — ✅ **해소(2026-08-18)**: 부모가 `AuditLog`에 **`resourceType`/`resourceId`** additive(부모 B-14·`spec-v1.0.25`·`3b6a834`). ⚠ 명명=`resourceType`(targetType 아님 — GW 프록시 대상 target·ADR-11과 이름충돌 회피·값에 `target`도 옴). Console 반영=**`T-FE-6-6`**(codegen 재생성·감사 화면 두 필터·device/clinic/target 상세 `ResourceHistory` 신설). `T-FE-2-5` kill 잠정 처리는 유지(방금-실행-사실 vs 서버 감사 이력=출처 다름). 발견=`T-FE-2-5`(2026-08-13).
- **CB-4**(감사 응답에 `reason` 부재) — ✅ **해소(2026-08-18)**: 부모가 `AuditLog`에 **`reason`(read-only·nullable)** additive(부모 B-15·`spec-v1.0.26`·`7734c22`·#12735). DB 컬럼·write 기존, read 스키마만 빠졌던 **정합 갭**. GW 구현=`T-DATA-1-9` 흡수(같은 매퍼·별 PR 없음). Console 반영=**`T-FE-6-6`**(codegen·`ResourceHistory`·감사 화면에 사유 표시·**truncate 안 함**·`null`이면 빈 자리 안 만듦). 발견=`T-FE-6-6`(2026-08-18).

---

## Entra 실환경 검증 대기 (트리거: IT/③-I 앱 등록 회신)

> **왜 여기 있나.** `T-FE-1-1`(SCR-AUTH-01·PR #12658·머지 `0ea8af0`·2026-08-13)로 Entra OIDC(Auth Code+PKCE)를 **코드는 실배선**했지만, **실제 Entra 테넌트로 로그인해 본 적은 없다**. 지금 통과한 검증은 목 우회 경로와 MSAL 호출 규약(모듈 경계 mock)까지다. 아래는 앱 등록이 끝나는 순간 그대로 소진할 체크리스트다.
> **정본:** 절차·값=`Entra-설정-가이드.md` · 인증 요구=SRS §3.2·§7.1 · env=§3.4. **IP Task:** `T-FE-8-1`(`[risk:auth]` 실 Entra 검증) → `T-FE-8-2`(staging 핵심 여정). 이 목록은 그 Task의 DoD 재료다.

### 1) 선행 조건 (이게 와야 시작)

| # | 필요한 것 | 소관 |
| --- | --- | --- |
| 1 | **Console SPA 앱** 등록(공개 클라이언트·PKCE·client secret 없음) + **GW Admin API 앱**(Expose an API·Application ID URI·delegated scope) — 2-앱 구조 | IT |
| 2 | redirect URI **`http://localhost:3100/auth/callback`** 등록(SPA는 포트 **정확 일치**) · **로그아웃 URI `http://localhost:3100/login`** 도 함께 | IT |
| 3 | 회신 값 4종 → `NEXT_PUBLIC_ENTRA_ISSUER`·`CLIENT_ID`·`AUDIENCE`·`REDIRECT_URI` | IT |
| 4 | 앱 역할/그룹 클레임 발급 구성(`admin`·`cs`·`operator`·`developer` → GW `operator_role` 매핑) | IT + GW |
| 5 | 로컬에서 붙을 **dev GW Admin API**(또는 로컬 GW `:3001`) + **CORS allowed origin** | GW BE (GW IP P11) |

### 2) 환경 전환

- `.env.local`에 `NEXT_PUBLIC_AUTH_MODE=entra` + `ENTRA_*` 4키(템플릿=repo `.env.example`).
- ⚠ **`AUTH_MODE=entra`면 MSW 목이 함께 꺼진다**(`src/mocks/enabled.ts`) → **실 GW가 떠 있어야** 화면이 뜬다. 인증만 실물로 바꾸고 목 데이터를 보는 조합은 여전히 없다(그럴 이유가 없다).
- 반대 조합(**인증은 목 + 데이터는 실 GW**)은 2026-08-13에 생겼다 — `NEXT_PUBLIC_GW_LIVE=true`. Entra 앱 등록 전에 로컬 GW 실데이터를 보기 위한 경로이며 §3-2 참조.
- ⚠ `NEXT_PUBLIC_*`는 **빌드 타임 주입**이라 값을 바꾸면 dev 서버를 재시작해야 한다.

### 3) 실제로 확인할 것 (코드로는 증명 불가·실물로만 드러남)

| # | 확인 | 틀렸을 때 증상 |
| --- | --- | --- |
| 1 | **issuer→authority 변환** — `ISSUER`에 `…/{tenant}/v2.0`을 넣어도 discovery 성공 | `/v2.0/v2.0/.well-known/…`을 찾아 로그인이 통째로 실패 |
| 2 | **토큰의 `aud`·`scp`** — jwt.ms로 디코드해 `aud`=GW Admin API 앱, `scp` 비어있지 않음, `iss`·`tid` 일치 | GW가 `/v1/admin/*` **전 요청을 401**로 막는다 |
| 3 | `{audience}/.default` scope가 **실제로 발급되는지**(scope 이름 TBD를 우회하려고 쓴 방식) | 동의 화면 오류 또는 `scp` 누락 |
| 4 | **`GET /v1/admin/me` 200** — GW가 그 토큰을 받아들이는지 | 401이면 #2 셋 중 하나가 어긋난 것 |
| 5 | 미인증으로 `/devices` 직접 진입 → `/login?to=/devices` → 로그인 후 **`/devices`로 복귀** | 매번 홈으로 떨어짐 |
| 6 | **무음 갱신** — 토큰 만료(Entra 세션 정책 종속) 후에도 화면이 계속 동작 | 갑자기 401 → 강제 로그아웃(FR-CON-33 위반) |
| 7 | **로그아웃** — `logoutRedirect` 후 다시 진입 시 계정 선택 없이 자동 재로그인되지 **않음** | 공용 PC에서 이전 사용자로 재진입 |
| 8 | 실패 경로 — 잘못된 clientId/redirect로 **사유가 화면에 표시**되고 조용히 실패하지 않음 | 흰 화면 또는 무한 왕복 |
| 9 | 역할 클레임 → GW `operator_role` 매핑이 실제로 성립(`/me`의 roles) | 권한 매트릭스(`T-FE-1-5`)가 전부 헛돎 |

### 3-1) P1에서 미룬 `[manual][risk:auth]` 2건 (실 GW 없이는 증명 불가)

구현 중 "지금은 증명할 수 없다"고 판단해 미룬 것들이다. **MSW가 403/409를 준다는 건 "우리 목이 그렇게 준다"만 보여줄 뿐** 서버가 실제로 막는지와는 무관하다. 둘 다 실 dev GW가 필요하다.

| # | 확인 | 유래 | 방법 |
| --- | --- | --- | --- |
| 1 | **무권한 역할로 API를 직접 호출하면 서버가 403을 내는가** — UI 게이팅은 클라 우회 가능이라 최종 인가는 서버여야 한다(SRS §7.2 결정 K) | `T-FE-1-5` dod | cs 토큰으로 `GET /v1/admin/operators`를 curl → 403 기대. Console UI를 거치지 않는 것이 요점 |
| 2 | **시스템 마지막 admin 회수를 서버가 409로 거부하는가** — Console UI 가드와 서버 판정이 **일치**하는지 | `T-FE-1-9` risk | admin이 1명뿐인 상태를 만들고 `PATCH …/roles/{grantId}` `status=revoked` → 409 기대. UI 버튼 비활성과 같은 시점에 막히는지 대조 |

⚠ 2번은 **lock-out 되면 Console 자체 복구 수단이 없다**(서버 seed 재배포 필요). 반드시 **버릴 수 있는 로컬/dev DB**에서만 시도한다.

### 3-2) Entra 전환 시 걷어낼 임시 경로

Entra 앱 등록 전 로컬에서 실 GW 데이터를 보려고 만든 우회로다. 전환 후 **코드는 그대로 두고 env만 끄면 된다**(오프라인 개발에 계속 쓸모가 있다).

| 대상 | 지금 | Entra 후 |
| --- | --- | --- |
| Console `.env.local` | `NEXT_PUBLIC_AUTH_MODE=mock` · `NEXT_PUBLIC_GW_LIVE=true` · `NEXT_PUBLIC_DEV_OPERATOR_TOKEN=…` | `NEXT_PUBLIC_AUTH_MODE=entra` + `ENTRA_*` 4키 (앞의 세 줄 삭제) |
| GW `.env` | `GW_OPERATOR_OIDC_*` → `http://127.0.0.1:3099` | 실 Entra issuer·JWKS·audience |
| 로컬 발급자 | `pnpm dev:oidc` 상시 기동 필요 | 불필요 |

**코드 변경 0건**이다 — `AUTH_MODE=entra`면 MSW가 꺼지고 MSAL 경로로 붙는다(T-FE-1-1에서 실 경로를 먼저 만들어 뒀다). `GW_LIVE`는 `NODE_ENV !== production`에서만 살아 있어 실 배포에는 영향이 없고, `verify:bundle`이 매 PR 그 사실을 검사한다.

### 4) 미리 적어 두는 함정 (디버깅 시간 절약용)

- **MSAL v5의 `navigateToLoginRequestUrl`은 config가 아니라 `handleRedirectPromise()` 인자이고 기본값이 `true`** — 코드에는 `false`로 고정해 뒀다(회귀 테스트 있음). 이 값이 살아나면 콜백 화면이 렌더되기 전에 브라우저가 옮겨져 **복귀 경로 결정과 실패 사유 표시가 동시에 죽는다**.
- **`postLogoutRedirectUri`(`{origin}/login`)도 Entra에 로그아웃 URI로 등록**돼야 한다. 미등록이면 로그아웃 직후 Entra 오류 페이지에 착지한다.
- **`.default`는 다른 scope와 섞어 요청할 수 없다.**
- **SPA redirect는 포트 wildcard 불가** — 3100 고정(§ IP 준비 메모).
- 토큰 캐시는 **MSAL이 sessionStorage에** 들고 있다(SRS §6.3). 앱이 따로 복사해 두지 않으므로, 디버깅 시 `gw-console.access-token` 같은 자체 키를 찾지 말 것(존재하지 않는다).

### 5) 배포 호스트에서만 드러나는 것 ⚠ — **활성 블로커 (2026-08-18)**

정적 export는 라우트마다 개별 HTML을 낸다(`out/devices.html` · `out/auth/callback.html` — `out/devices/index.html`이 **아니다**). CloudFront가 URI를 S3 키로 그대로 매핑하니 `/devices`는 없는 키이고, `403`·`404` → `/index.html` fallback만 있으면 **홈이 200으로 내려온다.**

**실측 2회** — 2026-08-13(최초 발견) · 2026-08-18(현 산출물로 재현, `cmp` 바이트 비교):

| 요청 | rewrite Function 없음 | 있음 |
| --- | --- | --- |
| `GET /devices` | 본문 = **`out/index.html`**(홈) | `out/devices.html` ✅ |
| `GET /auth/callback?code=…` | 본문 = **`out/index.html`**(홈) | `out/auth/callback.html` ✅ |

**`/auth/callback`이 홈으로 떨어지면 Entra가 되돌려준 `code`를 아무도 처리하지 않아 실 로그인이 조용히 실패한다.** 딥링크·새로고침 전부 같은 증상이다.

필요한 것: **확장자 없는 경로 → `.html` viewer-request CloudFront Function**(URI에 `.` 없으면 `.html` 붙이기, 루트는 `/index.html`). `403`/`404` fallback은 **그 다음** 단계다.

| # | 무엇 | 소유 | 상태 |
| --- | --- | --- | --- |
| 5-1 | 요청서 §2 항목 2에 Function을 **필수**로 명시 | Console | ✅ **PR #12752**(PL 리뷰 대기) |
| 5-2 | es-infra CloudFront `E165UOG7NKHXXZ`에 Function 추가 | **③-I Jack** | ⛔ **활성 블로커** — PL이 Teams 전달 |
| 5-3 | Jack CD PR #12743(파이프라인) | ③-I | 문제없음 · 그대로 진행 |
| 5-4 | 배포 후 딥링크 **자동** 스모크 체크를 CD 스테이지에 추가 | Console | ⏳ **#12743 머지 후** (같은 `azure-pipelines.yml`이라 지금 하면 충돌) |

**배포 후 확인**(수동·1줄):

```bash
diff <(curl -s https://console.gw.dev.ezcld.net/devices) \
     <(curl -s https://console.gw.dev.ezcld.net/)
# **달라야 한다.** 같으면 홈으로 떨어진 것 = Function 없음
```

> ⚠ **로컬 프리뷰 서버(`scripts/serve-preview.mjs`)로는 이 결함이 안 드러난다** — 그쪽은 `.html`을 붙여 보기 때문이다. "로컬에서 잘 되던데요"는 근거가 못 된다.

#### ⚠ 이 항목이 살아남은 방식 — 추적 자체의 실패

2026-08-13에 **실측까지 마치고** "→ ③-I 요청서 §2 항목 2에 반영 필요(**반영 여부=PL 판단**)"로 적어 두었는데, **그 뒤 아무도 집지 않아 요청서에 반영되지 않은 채 ③-I로 나갔다.** 그래서 es-infra는 요청서대로 만들었고, 결함은 Jack의 CD PR이 올라온 **5일 뒤**에야 다시 발견됐다.

**교훈: "PL 판단"으로 남긴 항목은 소유자와 기한이 없으면 사라진다.** 판단이 필요한 항목도 **누가·언제까지 판단할지**를 같이 적는다. 위 표처럼 소유·상태를 붙여 둔다.

---

## IP 준비 메모 (구현 세션 인계 — Console SRS baseline 후 Console IP로 반영)

> **성격 구분.** 백로그 항목(위) = *Console SRS에 넣을 변경*. 이 섹션 = *SRS 변경이 아니라, 추후 **Console IP** 작성 시 챙길 구현 인계 메모*(잊지 않으려 미리 캡처). **트리거 = Console SRS baseline → 스펙 세션이 Console IP 작성**(현재 Console IP 없음·부모 GW IP와 별개).
>
> **원칙.** IP는 SRS에서 도출한다 — 스택(§3.4.2)·**테스트 자동화 전략(§3.5)**·env 키(§3.4)·FR-CON 인수기준(§7)을 Task로 분해하면 대부분 자동 반영된다. 아래는 **SRS에 자연스럽게 안 담기는 구현 세부**만 누적한다(SRS에 이미 있는 건 여기 중복 기재 금지·포인터만).

- **테스트 자동화(§3.5 전략의 구현 세부).**
  - MSW 목은 **부모 OpenAPI에서 핸들러 생성**(계약 고신뢰 목·타입 재생성과 연동).
  - **완전 E2E는 dev/staging GW + Entra dev 테넌트(③-I) 필요**(§3.5) — 없을 땐 로컬은 MSW로 component/e2e 대체. IP Task DoD에 "환경 없으면 MSW 경로로 커버" 명시.
  - **시각**: Playwright 스크린샷 회귀 + axe-core는 자동, **baseline 승인만 사람**(§3.5 ④). Storybook+Vitest addon·Chromatic은 LLD 평가(도입 시 IP Task 추가).
  - v1.0 단일 리전이라 **리전 스위처 e2e는 자명**(멀티리전 스위칭·토큰 audience 테스트는 gw/1.2).
- **계약 소비.** Console은 부모 OpenAPI를 **코드젠(orval/openapi-typescript)** 으로 소비 — 부모 계약 변경 시 **타입 재생성**을 IP Task 절차에 포함(§4.4 핀 갱신과 연동).
- **범위 경계(오구현 방지).** enroll CSR→cert·operator_role 복제 등은 **부모/③-I 소관**이지 Console 구현 아님 — Console은 Admin API 소비만(혼동 방지 메모).
- **Console 구현 = 별도 세션(현 GW 백엔드 세션과 분리·2026-08-10 결정).** 이유: repo(`vt-api-gateway-console`)·스택(Next.js+Refine+shadcn vs NestJS+Prisma)·IP·도메인 에이전트(**frontend-expert** vs backend-expert)가 모두 다름 → 컨텍스트 오염 방지·도메인 격리·병렬성. **조율은 세션 공유가 아니라 계약(부모 OpenAPI @baseline 태그·§4.4)으로** 하고, GW Admin API 변경 필요 시 스펙 세션 경유(부모 OpenAPI PR→양 세션이 새 baseline 픽업). ⚠ Console 세션은 **frontend-expert 기본 템플릿 스택으로 흘러가지 말고 Console SRS §3.4.2 확정 스택(Refine headless+shadcn+Tailwind+TanStack)을 따르도록** IP에 명시. 시작 시점 = Console SRS baseline → Console IP → 세션 오픈.
- **조기 UI 리뷰 · Entra 준비 전 개발 (mock-first).**
  - **Entra 없이 착수 가능(blocker 아님)** — 로컬은 `AUTH_MODE=mock`(SRS §3.4)로 인증 우회 + **MSW**로 API 목 → **전 화면·역할별(admin/cs/operator/developer)·3상태(로딩/오류/빈)를 로컬에서 확인**. Console UI 코드는 실제 그대로(인증·API만 가짜).
  - **설치 0 조기 리뷰** — mock 빌드 또는 **Storybook을 정적 URL로 배포**(Console=정적 SPA라 S3/CloudFront·PR 프리뷰로 쉬움) → **링크만 열어 화면 리뷰**. **IP에 "리뷰용 mock/Storybook 정적 배포" Task 포함**(사장님 조기 피드백용).
  - **Entra 등록(병렬 진행) — 절차명 = "앱 등록(App registration)"**(SPA·PKCE·client secret 없음). **지금 가능**: 앱 생성 + **dev(`console.gw.dev.ezcld.net/auth/callback`)·localhost(`http://localhost:3100/auth/callback`·포트 고정·SPA는 포트 정확 일치) redirect 등록**. **prod redirect(`console.gw.<도메인>`)는 도메인 확정 후**(C-10) 추가(redirect는 나중에 추가 가능). **IT에 테넌트·claim/역할(→`operator_role`) 확정을 일찍 요청**(C-2 · claim 형식이 GW authz 매핑에 영향).
  - **실 연동 전환 순서** — local(mock) → 실 dev 테넌트(localhost redirect) → **staging/e2e = 실 dev/test 테넌트**(실 OIDC·claim→역할 검증·§3.5) → prod. **mock은 prod 금지.**
  - **dev 포트 = 3100** — Console dev 서버 포트를 **3100으로 고정**(Next.js 기본 3000이 **GW core(3000)와 충돌**하므로 변경 — admin=3001·receiver=3002·dispatcher=3003과도 안 겹침). Entra SPA redirect는 포트 정확 일치라 이 값(3100)으로 등록. Console→Admin 호출 base=`http://localhost:3001`(local GW admin).
  - 정본: 절차 상세=`Entra-설정-가이드.md`(§2-A 로컬 개발 인증) · 인증 요구=SRS §3.2·§7.1 · env=§3.4.
- *(이하 발견 시 계속 누적 — Console IP 작성 시 이 섹션을 체크리스트로 소진)*
