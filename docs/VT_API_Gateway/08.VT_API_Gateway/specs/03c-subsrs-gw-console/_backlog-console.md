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

## 백로그 항목

_열린 항목 없음_ — CB-1(멀티리전 운영자 authz·ZTNA 제거→Entra)·CB-2(v1.0 최소기능 선행·기술 스택 확정)는 **SRS baseline에 반영 완료**(상세는 git 이력).

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

### 5) 배포 호스트에서만 드러나는 것 ⚠

**localhost 검증만으로는 절대 드러나지 않는 결함이 하나 있다.** 정적 export는 라우트마다 별도 HTML(`out/auth/callback.html`)을 내는데, `docs/handoff/infra-requests.md` §2가 요청한 CloudFront 구성(**S3 OAC + `403`·`404` → `/index.html`**)만으로는 URI가 S3 키로 그대로 매핑돼 `/auth/callback` 키를 못 찾고 **홈 화면으로 떨어진다**. CloudFront를 흉내낸 서버로 실측 확인(2026-08-13):

```
GET /auth/callback?code=…  →  본문: "P0 스캐폴드 진행 중 — App Shell 골격" (홈)
```

즉 **Entra가 되돌려준 code가 처리되지 않아 실 dev 로그인이 조용히 실패한다.** 콜백만이 아니라 `/devices` 등 **모든 딥링크·새로고침**이 같은 증상이다. 확장자 없는 경로를 `<path>.html`로 바꾸는 **CloudFront Function(viewer-request)** 이 필요하고, `index.html` fallback은 그다음 단계다. 로컬 프리뷰 서버(`scripts/serve-preview.mjs`)는 `.html`을 붙여 보므로 이 차이가 드러나지 않는다. → **③-I 요청서 §2 항목 2에 반영 필요**(반영 여부=PL 판단).

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
