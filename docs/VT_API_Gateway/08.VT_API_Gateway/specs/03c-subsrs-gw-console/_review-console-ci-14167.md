# Console dev Entra 배포 경로 — 리뷰 로그

> **PR**: `vt-api-gateway-console` #14167 (`ci(console): dev 실 Entra 로그인 배포 경로를 추가한다 (devAuthMode)`)
> **작성자**: 임건혁(Jack) · **리뷰어**: Console 세션 · **작성일**: 2026-09-09
>
> 이번 건은 **우리가 리뷰어**다(지난 #12602 는 반대). 코멘트 원문·근거·게시 위치를 남긴다.
> 게시는 Raymond 가 직접 한다.

---

## 배경

Entra 회신(IT-9442) 이후 dev 에서 실 로그인을 검증하려면 **목 없는 배포본**이 필요했다.
그런데 `main` 머지 시 도는 배포는 `preview-build.mjs` 가 만들고, 그 스크립트가
`NEXT_PUBLIC_AUTH_MODE=mock`·`NEXT_PUBLIC_MOCK_PREVIEW=true` 를 **강제**한다.
즉 **Entra 값을 아무리 잘 넣어도 배포본은 계속 목**이었다. 이 PR 이 그 구멍을 메운다.

---

## F1 — `CONSOLE_STATIC_EXPORT` 누락 · **차단** · 라인 코멘트

**위치**: `azure-pipelines.yml:561` — `- script: pnpm build`

**무엇이 문제인가.** 정적 export 는 `CONSOLE_STATIC_EXPORT === "true"` 일 때만 켜진다
(`next.config.ts:23`). 프리뷰 경로는 `preview-build.mjs:62` 가 그 값을 넣어 주지만,
`pnpm build` 단독으로는 들어가지 않는다. 그래서 **`out/` 이 만들어지지 않는다.**

**실측(로컬 재현).**

```
NEXT_PUBLIC_AUTH_MODE=entra pnpm build   →  exit 0 (빌드는 성공)
out/                                      →  없음 (.next 만 생성)
aws s3 sync <없는 경로> …                 →  The user-provided path does not exist
```

**영향.** `deploy-preview.sh:37` 이 `aws s3 sync "$OUT_DIR" …` 이고 `OUT_DIR="out"` 이라
**배포 스텝에서 반드시 실패**한다. `PublishPipelineArtifact` 도 같은 경로를 본다.

⚠ **빌드가 초록으로 끝나고 배포에서 죽으므로, 그 시점에는 원인이 AWS·자격증명 문제처럼
보인다.** 진단이 엉뚱한 곳으로 간다.

**조치(한 줄).**

```yaml
- script: pnpm build
  env:
    CONSOLE_STATIC_EXPORT: "true"      # ← 추가
    NEXT_PUBLIC_GIT_COMMIT: "$(Build.SourceVersion)"
    NEXT_PUBLIC_BUILD_TIME: "$(Build.QueueTime)"
```

---

## 확인하고 넘어간 것 (지적 아님)

| 항목 | 판단 |
| --- | --- |
| `AUTH_MODE` 를 안 주는 것 | ✅ 맞다 — `resolveAuthMode()` 가 프로덕션 빌드에서 `MOCK_PREVIEW` 없이는 mock 을 안 돌려주므로 **안 주는 것 자체가 실 로그인 빌드**다 |
| `verify:bundle` 을 실 빌드에도 건 것 | ✅ 반대 방향의 같은 검사 — 목·로그인 우회가 섞이면 잡힌다 |
| `.env*` 사전 삭제 | ✅ self-hosted 는 워크스페이스를 재사용해 **지난 실행 값으로 조용히 빌드**되는 사고가 실제로 난다 |
| `failOnEmpty` + SSM 착지 게이트 | ✅ 값이 비면 빌드를 세운다 — 빈 설정으로 배포되면 원인이 배포 후에야 드러난다 |
| 같은 버킷 상호배제 | ✅ 두 배포가 경쟁해 *"나중에 끝난 쪽이 남는"* 상황을 없앴다 |
| 기본값 `mock` 유지 | ✅ PR 트리거는 파라미터를 못 넘기므로 자동 실행은 전부 기존과 동일 |

---

## 선결 조건 — 이 PR 밖 (전체 코멘트)

PR 주석이 적어 둔 두 가지가 **아직 미충족**이라, 머지해도 지금은 로그인이 끝까지 못 간다.

1. **admin consent 미완료** — 2026-09-09 로컬에서 실측. 사용자마다 승인 요청 화면이 뜬다.
   IT팀(이희선)에 요청 전송함. **조직 단위 1회**면 되고, 이후 사용자는 동의 화면을 안 본다.
2. **`https://console.gw.dev.ezcld.net/auth/callback` redirect URI** — 회신에 없어 미확인.
   consent 요청 시 **함께 등록 확인**하면 한 번에 끝난다.

> 참고: 로컬 실측으로 **테넌트·issuer·JWKS 일치**, **SPA client ID·`localhost:3100` redirect
> 등록**, **scope `access_as_operator` 노출**은 확인됐다(동의 화면까지 도달). 남은 것이 consent 다.

---

## 연관 PR

| PR | 내용 |
| --- | --- |
| #14162 | Jack — Entra 회신값 문서 반영. 검토 완료·문제 없음 |
| #14168 | Console — `verify:entra` 가 v2 토큰(`aud`=GUID)을 오류로 잡던 것 수정 |
| #14169 | Console — MSAL `interaction_in_progress` 로 로그인이 영영 막히던 버그 수정 |

⚠ `aud` 형식(GUID vs `api://`)은 **실토큰으로만 확정된다.** consent 후 로그인해 판정한다
(`scripts/inspect-entra-token.mjs`).

---

## 게시할 코멘트

> 아래 두 블록은 **그대로 복사해 붙이는 원문**이다. 인용 부호를 붙이지 않는다 — 붙이면
> 복사할 때 `> ` 가 따라와 PR 에서 통째로 인용문이 된다.

### ① 라인 코멘트 — `azure-pipelines.yml` 561 행 (`- script: pnpm build`)

~~~markdown
⚠ **여기서 `out/` 이 안 만들어져 아래 배포 스텝이 반드시 실패합니다.**

정적 export 는 `CONSOLE_STATIC_EXPORT === "true"` 일 때만 켜집니다(`next.config.ts:23`). 프리뷰 경로는 `preview-build.mjs` 가 그 값을 넣어 주는데, `pnpm build` 단독으로는 안 들어갑니다.

로컬에서 그대로 재현했습니다:

```
NEXT_PUBLIC_AUTH_MODE=entra pnpm build   →  exit 0 (빌드는 성공)
out/                                      →  없음 (.next 만 생성)
```

`deploy-preview.sh` 는 `aws s3 sync out ...` 이고, 경로가 없으면 `The user-provided path does not exist` 로 죽습니다. `PublishPipelineArtifact` 도 같은 경로를 봅니다.

⚠ **빌드가 초록으로 끝나고 배포에서 죽으니**, 그 시점엔 원인이 AWS 문제처럼 보입니다.

한 줄이면 됩니다:

```yaml
env:
  CONSOLE_STATIC_EXPORT: "true"      # ← 추가
  NEXT_PUBLIC_GIT_COMMIT: "$(Build.SourceVersion)"
  NEXT_PUBLIC_BUILD_TIME: "$(Build.QueueTime)"
```
~~~

### ② 전체 코멘트

~~~markdown
설계 방향에 동의합니다 — 제가 짚었던 **"dev 에 목 빌드만 올라가는 구멍"** 을 정확히 메웠고, 특히 세 가지가 좋습니다.

- **`verify:bundle` 을 실 빌드에도 건 것** — 반대 방향의 같은 검사라 로그인 우회가 섞이면 잡힙니다
- **`.env*` 사전 삭제** — self-hosted 는 워크스페이스를 재사용해서, 지난 실행 값으로 **조용히 빌드되는** 사고가 실제로 납니다
- **같은 버킷 상호배제** — 두 배포가 경쟁해 "나중에 끝난 쪽이 남는" 상황을 없앤 것

`AUTH_MODE` 를 안 주는 것이 곧 실 로그인 빌드라는 판단도 맞습니다 — `resolveAuthMode()` 가 프로덕션 빌드에서 `MOCK_PREVIEW` 없이는 mock 을 안 돌려줍니다.

**막는 건 라인 코멘트 하나뿐입니다**(`CONSOLE_STATIC_EXPORT` 누락). 그것만 고치면 승인입니다.

⚠ **다만 지금 돌려도 로그인은 끝까지 못 갑니다** — 주석에 적으신 선결 조건 둘이 아직 미충족입니다.

- **admin consent 미완료** — 오늘 로컬에서 확인했습니다. 사용자마다 승인 요청 화면이 뜹니다. IT팀(이희선님)에 요청 전송했습니다.
- **`https://console.gw.dev.ezcld.net/auth/callback` redirect URI** — 회신에 없어 미확인입니다. consent 요청하실 때 **함께 등록 확인**을 부탁드리면 한 번에 끝납니다.

그 둘이 끝나면 이 파이프라인으로 **dev 에서 실 로그인 검증(T-FE-8-1)** 이 가능해집니다.
~~~

---

## 처리 상태 — **종결**(2026-09-10)

| 항목 | 상태 |
| --- | --- |
| F1 `CONSOLE_STATIC_EXPORT` | ✅ **반영·머지됨**(main `8112e0d`) — Jack 이 근거 주석까지 붙여 수정 |
| 선결 조건 ① admin consent | ✅ **완료**(IT팀 승인·2026-09-10) |
| 선결 조건 ② `console.gw.dev.ezcld.net/auth/callback` redirect URI | ⏳ **미확인** — 실 배포본으로 로그인해 봐야 판정된다 |

### 머지본 실검증

```
CONSOLE_STATIC_EXPORT=true pnpm build   →  exit 0
out/                                     →  ✅ 60 항목 생성
pnpm verify:bundle                       →  ✅ 개발 전용 표지 0건
```

**F1 이 실제로 해소됐고, 실 빌드에 목·로그인 우회가 섞이지 않는 것까지 확인**했다.

### 남은 것 — 이 PR 밖

- **redirect URI(dev 호스트)** — `devAuthMode=entra` 로 첫 배포·로그인을 해 봐야 안다.
  미등록이면 `AADSTS50011` 로 드러난다.
- ⚠ **로컬 로그인은 별도 회귀로 막혀 있었다**(#14195) — MSAL 리다이렉트 응답을 초기화가
  소비해 **로그인이 무한 반복**됐다. 그 수정이 머지돼야 로컬·배포 양쪽에서 로그인이
  끝까지 간다.
