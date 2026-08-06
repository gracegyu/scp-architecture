# ③ GW SRS — 리뷰 코멘트 추적 (③b verbatim + JWKS 승격 · PR #12440)

> **작업용 문서**. 각 스레드=코멘트 원문 전체 + 우리 판단·답변·조치. **답변 5건은 2026-08-05 전규현 명의로 게시 완료.** 반영=vt-api-gateway `spec/cleverspace-3b-verbatim-jwks` 브랜치(`a6044df` push 완료).

- **PR**: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/12440
- **주제**: ③b(GW→CleverSpace) 신원 전달 = device 토큰 verbatim + GW JWKS v1.0 승격 · §7.1.5(GW Guard 검증 계약)·`/.well-known/jwks.json` 신설 · scope 문면 정정
- **리뷰어**: Larry·Scott(필수) · Jack·Teddy·Thomas(옵션) · 우리=전규현
- **커밋**: `88b17da`(원안) + `a6044df`(리뷰 반영분·**push 완료** 2026-08-05)
- **최종 fetch**: 2026-08-05 (Update 1 포함) · 유효 thread 7건(초기 Nemesis 4 + Scott 승인 1 + **Update 1 Nemesis 2**) + 시스템 thread(리뷰어 지정·voted·push 알림)
- **상태**: **Scott 승인 완료**(voted 10·aud 위험 수용) · 초기 Nemesis 🔧1·💡2·총평1 = **push(a6044df)·답변 게시 완료** · Update 1 Nemesis 💡1 = **push(0a914c0)·게시 완료** · **Update 2 = Larry [Block]2·[Suggestion]3 + Nemesis 권장1(C-08~C-14) 전건 수용 → 편집 push(`2a16391`)·답변 7건 게시완료·Nemesis(83156·83157) resolve · **Larry vote 10 → #12440 병합 완료(2026-08-06)·baseline 태그 `spec-v1.0.11`**

---

## 처리 절차
1. **fetch** — PR threads/comments 수집(`az devops invoke --area git --resource pullRequestThreads … pullRequestId=12440`).
2. 각 스레드를 **`## C-NN · <file:line> · [thread <id>]`** 로 기록(원문 전체 인용).
3. 우리 판단 + 답변 작성 → 사용자 확인 후 게시.
4. **조치·반영·상태** 기록. SRS/OpenAPI 반영은 `spec/cleverspace-3b-verbatim-jwks`에 커밋·push.

> 답변 스타일: 서술문(개조식 지양)·내부 라벨(C-NN)은 로그 내부용(게시 안 함)·대외 이모지 없음·`#숫자` 오링크 회피·호칭 "님" 금지.
> **처리 완료(2026-08-05):** ① 수정본 `a6044df` push 완료(보안 수정 포함·정책상 Scott 승인 재요청 여부는 PR에서 확인) → ② 답변 5건 각 스레드 게시 완료.

---

## 코멘트

### C-01 · docs/specs/SRS.md:1869 · [thread 83087] · 🔧 수정 필요 · Active
- **[민진우(Thomas)·Nemesis v0.6.0 · 83087.1]**
  > From Nemesis(v0.6.0, 🆔msfejovqa),
  > **🔧 수정 필요**
  >
  > GW Guard 검증 절차 1단계가 **아직 서명 검증이 안 된 토큰의 `region` claim**으로 JWKS fetch URL(`https://api.<region>.gw.<도메인>/.well-known/jwks.json`)을 조립한다. `region`은 서명 바인딩 대상(§7.1.1 Output)이지만, GW Guard는 서명을 검증하기 *전에* 이 값을 읽어 URL에 끼워 넣어야 하는 순서라 이 시점에는 신뢰할 수 없다. 공격자가 `region`을 조작한 위조 토큰을 보내면(예: 자신이 통제하는 호스트로 해석되는 값) GW Guard가 공격자 JWKS를 받아와 그 공개키로 위조 서명이 통과되어 신뢰 모델("GW 서명 = 정품 트래픽")이 무너진다(key-substitution·SSRF). 본 절이 CleverSpace 검증 계약의 정본이므로, `region`을 **알려진 리전 allowlist로 검증**한 뒤에만 호스트에 보간하거나, JWKS 조회 호스트를 **검증된 `iss`에 고정(pin)**하라는 요구를 명시해야 한다. 현재 서술은 이 함정을 경고하지 않아 구현이 그대로 취약해질 수 있다.

- **[전규현(우리)·답변·↳ 게시완료]**
  > 정확한 지적입니다. 서명 검증 전에 토큰의 region claim으로 JWKS URL을 조립하면, 위조된 region으로 공격자가 통제하는 호스트의 JWKS를 받아 위조 서명이 통과하는 신뢰 우회가 생깁니다. §7.1.5 검증 절차를 정정했습니다. GW Guard는 JWKS를 배포 설정에 고정된 신뢰 URL(자기 리전 GW)에서만 가져오고 토큰 claim으로 URL을 조립하지 않습니다. 리전 사일로라 ③b는 리전-로컬이므로 JWKS 출처는 그 리전 GW 하나로 고정됩니다. region claim은 서명 검증을 통과한 뒤에만 신뢰하며, 검증된 region이 설정 리전과 일치하는지 교차검증해 불일치 시 거부합니다.

- **조치:** §7.1.5 검증 1단계를 "배포 설정 신뢰 URL 고정(토큰 claim 조립 금지)"으로, 3단계에 "검증 후 region 교차검증" 추가. (제안된 allowlist/iss-pin보다 강한 방식 — 토큰에서 URL을 아예 도출하지 않음.)
- **반영:** `a6044df`(SRS.md §7.1.5) · **미푸시**
- **상태:** 답변 게시완료(push 반영)

### C-02 · docs/specs/design/openapi/…openapi.yaml:1577 · [thread 83088] · 💡 권장 · Active
- **[민진우(Thomas)·Nemesis v0.6.0 · 83088.1]**
  > From Nemesis(v0.6.0, 🆔msfejovqa),
  > **💡 권장**
  >
  > JWKS는 GW Guard가 **fail-closed로 의존**하는 무인증 공개 엔드포인트인데(도달 불가 시 거부·§7.1.5), 응답에 `429 TooManyRequests`만 선언되어 있다. `kid` 회전·미스 시 재fetch가 몰릴 때 과도한 rate-limit이 걸리면 정품 트래픽까지 fail-closed로 차단될 수 있다. 이 엔드포인트에 대해서는 넉넉한 한도(또는 CDN/캐시 전면 배치)를 전제로 한다는 점을 계약에 남기거나, 소비자 캐시로 흡수됨을 명시하면 좋다.

- **[전규현(우리)·답변·↳ 게시완료]**
  > 수용합니다. JWKS는 GW Guard가 fail-closed로 의존하는 엔드포인트라, kid 회전이나 미스로 재fetch가 몰릴 때 rate-limit으로 정품 트래픽이 차단되면 안 됩니다. 넉넉한 rate-limit과 CDN/캐시 전면 배치를 전제로 한다는 점을 OpenAPI 엔드포인트 설명과 §7.1.5에 명시했습니다. 회전은 구·신 kid 동시 게시로 재fetch 자체를 최소화합니다.

- **조치:** OpenAPI jwks 설명 + §7.1.5 JWKS 계약에 "fail-closed 의존 → 넉넉한 rate-limit + CDN/캐시 전제" 조항 추가.
- **반영:** `a6044df` · **미푸시**
- **상태:** 답변 게시완료(push 반영)

### C-03 · docs/specs/design/openapi/…openapi.yaml:1558 · [thread 83089] · 💡 권장 · Active
- **[민진우(Thomas)·Nemesis v0.6.0 · 83089.1]**
  > From Nemesis(v0.6.0, 🆔msfejovqa),
  > **💡 권장**
  >
  > §7.1.5는 소비자에게 "JWKS 캐시 TTL 수 분 + `kid` 미스 트리거 refresh"를 요구하지만, 200 응답 스키마에는 `Cache-Control`/`max-age` 등 캐시 지시 헤더 계약이 없다. 리전 로컬·회전 게시 특성상 앱/CDN이 어떤 캐시 헤더를 내려주는지를 응답 `headers`로 명시하면 소비자 캐시 동작이 계약으로 고정되어 상호운용이 명확해진다.

- **[전규현(우리)·답변·↳ 게시완료]**
  > 수용합니다. 소비자 캐시 동작을 계약으로 고정하기 위해 jwks 200 응답에 Cache-Control(max-age) 응답 헤더를 선언했고, §7.1.5의 캐시 지침(수 분 TTL + kid 미스 재fetch)과 정합시켰습니다.

- **조치:** OpenAPI jwks 200에 `Cache-Control` 응답 헤더(`public, max-age=300` 예시) 선언 + §7.1.5 계약에 캐시 헤더 조항.
- **반영:** `a6044df`(OpenAPI 200 headers) · **미푸시**
- **상태:** 답변 게시완료(push 반영)

### C-04 · (일반·총평) · [thread 83090] · Active
- **[민진우(Thomas)·Nemesis v0.6.0 · 83090.1]**
  > From Nemesis(v0.6.0, 🆔msfejovqa, ⏱4m35s, 🔢590.6k in/12.3k out),
  > ## Code Review (Other)
  >
  > 이 PR은 코드가 아니라 SRS.md·OpenAPI 스펙 문서 변경으로, ③b 홉에서 device 토큰 verbatim 전달 + GW JWKS를 v1.0으로 승격하고 §7.1.5(CleverSpace GW Guard 검증 계약)와 `/.well-known/jwks.json` OpenAPI 항목을 신설한다. 전반적으로 섹션 상호참조(§2.3.0·§7.1.1·§7.1.3.1·§4.1.2·§7.2.2 등)와 FR-AUTH-10 인라인 선언, 기존 well-known 엔드포인트(`compatibility` 태그·`security:[]`) 패턴과의 정합성은 잘 맞고, JWK 스키마(`kty/use/alg/kid/n/e`)도 RSA 서명키로 올바르다. `aud` confused-deputy 이슈는 본문에서 "v1.0 의식적 수용"으로 명시 acknowledged 되어 있어 리뷰 지침상 제외했다.
  >
  > 구조적으로 가장 중요한 지점은 검증 순서에 내재한 신뢰 부트스트랩 문제다(Line Comment 참조): 서명 검증 전 토큰 필드로 JWKS 위치를 정하는 절차가 allowlist/issuer-pinning 요구 없이 서술되어, 계약을 그대로 따르면 key-substitution/SSRF 취약점으로 이어질 수 있다. 이 절이 CleverSpace 구현의 정본 가이드이므로 해당 경고를 계약에 포함하는 것이 필요하다. 나머지는 JWKS 엔드포인트의 캐시 헤더·rate-limit 관련 계약 보강(recommendation) 수준이다.
  >
  > 3 line-specific finding(s) were posted as inline comments.

- **[전규현(우리)·답변·↳ 게시완료]**
  > 리뷰 감사합니다. 지적하신 세 가지를 반영했습니다. 서명 검증 전 region 신뢰 문제는 JWKS 신뢰 URL을 배포 설정으로 고정하고 region은 검증 후 교차검증하도록 정정했고, JWKS의 fail-closed 의존은 넉넉한 rate-limit과 CDN 전제, Cache-Control 헤더 계약으로 보완했습니다.

- **조치:** 총평 확인. 라인 지적 3건(C-01·02·03) 반영으로 갈음.
- **반영:** `a6044df` · **미푸시**
- **상태:** 답변 게시완료(push 반영)

### C-05 · (일반·승인) · [thread 83105] · Active
- **[김성훈(Scott) · 83105.1]** (thread 83104: voted 10)
  > JWKS 에 대한 승인을 하며 aud 위험은 현재로선 안고 갑니다.
  > 다음 단계 에서 충분히 커버 할 수 있는 영역으로 보이며, 이에 대한 언급이 되어있어 승인 합니다.

- **[전규현(우리)·답변·↳ 게시완료]**
  > 승인 감사합니다. aud 위험은 말씀대로 현 단계에서 수용하고, 내부 target이 둘 이상으로 늘 때 aud를 target으로 못박는 upstream 어서션으로 승격하는 방향을 §7.1.5에 남겨두었습니다.

- **조치:** 승인 확인(필수 리뷰어 Scott 완료). 별도 스펙 변경 없음.
- **반영:** 문구만(§7.1.5 향후 승격 경로는 원안에 이미 존재).
- **상태:** 답변 게시완료(push 반영)

---

## Update 1 (2026-08-05 · 수정본 `a6044df` push 후 Nemesis 재검토 · v0.6.0 msflr4qli)

### C-06 · docs/specs/SRS.md:1870 (§7.1.5) · [thread 83141] · 💡 권장 · 게시완료·resolved(fixed)
- **[민진우(Thomas)·Nemesis v0.6.0 · 83141.1]**
  > From Nemesis(v0.6.0, 🆔msflr4qli),
  > **💡 권장**
  >
  > 검증 절차 2단계가 `iss`(발급 GW) 확인을 신뢰 기준으로 삼지만, **무엇과 대조해 `iss`를 검증하는지(기대값)**가 명시돼 있지 않다. 게다가 아래 "신원 계약 — 서명 바인딩(신뢰 가능)" 목록은 `device_id`·`region`·`aud`·TTL만 열거하고 `iss`를 빠뜨려(§7.1.1 Output 라인 1790도 동일), 검증이 의존하는 claim이 정작 서명 바인딩 계약 목록에서 누락된 상태다. 실제 신뢰는 1단계의 JWKS URL 고정(리전 GW 공개키로 서명 검증)이 앵커하므로 보안 구멍은 아니지만, GW Guard 구현 가이드로서는 (a) `iss`의 기대값 = 배포 설정에 고정된 리전 GW issuer 식별자와 일치 검증, (b) `iss`를 서명 바인딩 목록에 포함,을 계약에 명시하면 리전 교차검증(3단계)과 정합되고 구현 재량으로 남는 애매함이 사라진다.

- **[전규현(우리)·답변·↳ 게시완료]**
  > 정확한 지적입니다. 신뢰 앵커는 JWKS URL 고정이지만 가이드 명확성을 위해 반영했습니다. 검증 2단계에서 iss가 배포 설정에 고정된 그 리전 GW issuer 식별자와 일치하는지 확인하도록 명시하고, iss를 서명 바인딩 claim 목록(§7.1.5·§7.1.1 Output)에 포함했습니다. 3단계 region 교차검증과 정합됩니다.

- **조치:** §7.1.5 검증 2단계에 **iss 기대값(배포 설정 리전 GW issuer와 일치) 검증** 명시 + **서명 바인딩 목록에 `iss` 추가**(§7.1.5 · §7.1.1 Output·narrative 정합).
- **반영:** `0a914c0` push 완료
- **상태:** 답변 게시완료 · thread resolved(fixed)

### C-07 · (일반·총평 Update 1) · [thread 83142] · 게시완료·resolved(fixed)
- **[민진우(Thomas)·Nemesis v0.6.0 · 83142.1]**
  > From Nemesis(v0.6.0, 🆔msflr4qli, ⏱2m02s, 🔢283.2k in/7.8k out),
  > ## Code Review (Other) — Update 1
  >
  > 이번 증분은 이전 리뷰의 세 지적을 모두 해소한다. (1) **must_fix — 서명 검증 전 `region` claim으로 JWKS URL 조립**: 신설 §7.1.5 검증 절차 1단계가 "신뢰 URL 고정(토큰 claim으로 조립 금지)"을 명문화하고, JWKS 출처를 GW Guard 배포 설정에 고정된 리전-로컬 GW 하나로 못박아 위조 `region`을 통한 key-substitution/SSRF를 원천 차단한다. `region`은 서명 검증 통과 후 3단계에서 교차검증 용도로만 쓰도록 순서를 바로잡았고(§7.1.1 라인 1790에서 `region`이 실제 서명 바인딩 claim임을 확인), 방어심층 성격이라 정합적이다. (2) **recommendation — JWKS fail-closed 대비 rate-limit**: "넉넉한 rate-limit + CDN/캐시 전면 배치" 전제와 회전 시 구·신 `kid` 동시 게시(재fetch 최소화)를 §7.1.5·OpenAPI description에 계약으로 남겼다. (3) **recommendation — 캐시 헤더 계약**: OpenAPI 200 응답에 `Cache-Control: max-age`(권장 수 분) `headers` 선언이 추가되어 소비자·CDN 캐시 동작이 계약으로 고정됐다.
  >
  > 구조적으로 §7.1.5는 신뢰 모델·검증 절차·JWKS 엔드포인트 계약·구현 책임 분담표·오류 처리·시퀀스 다이어그램을 갖춰 GW/CleverSpace 경계(공개 JWKS 하나)를 명확히 규정하며, 보안 8항목 표의 2컬럼(디바이스·프록시 면 / 운영자·관리 면) 분리와 `scope` 예약(미사용) 정정도 기존 §7.1.1·§7.2.2·§7.5.3 서술과 정합한다. `aud` confused-deputy는 이전과 동일하게 "v1.0 의식적 수용"으로 acknowledged 되어 있어 제외했다. 남은 지적은 위 line comment 한 건(`iss` 기대값·바인딩 목록 정밀화)뿐이며 recommendation 수준이다.
  >
  > 1 line-specific finding(s) were posted as inline comments.

- **[전규현(우리)·답변·↳ 게시완료]**
  > 리뷰 감사합니다. 지적하신 iss 기대값·서명 바인딩 목록 명확화도 반영했습니다.

- **조치:** 총평 확인 — 이전 3건(C-01·02·03) 해소 확인. 잔여 1건은 C-06 반영으로 갈음.
- **반영:** `0a914c0`(C-06과 함께)
- **상태:** 답변 게시완료 · thread resolved(fixed)

---

## Update 2 (2026-08-05 · Nemesis 재검토 Update 2 + Larry 리뷰 · **Larry voted -5 작성자 대기**)

> **fetch 2026-08-06.** 신규 액티브 6건 — Nemesis Update 2 권장 1(C-08·총평 C-09) + **Larry [Block] 2·[Suggestion] 3**(C-10~C-14). 공통 진단: verbatim의 대가(‘GW 홉 경유’ 증명 상실 + 직접 호출 경로 revocation/rate-limit 미적용)를 문면이 지불 안 한 것처럼 서술 → **전건 수용(정밀 정정·계약 보강·verbatim 반전 아님, Larry도 verbatim 동의).**
>
> **처리 결과(2026-08-06):** 확정 4건(TTL `expires_in` ≤15분 · iss `https://api.<region>.gw.<도메인>` · aud=`GW`(비-target) · revocation=(c) TTL 상한) 반영 → §7.1.5·§7.1.1 Output·OpenAPI **편집 push(`2a16391`)** · **답변 7건 게시완료(comment id 2)** · **Nemesis 83156·83157 resolved(fixed)** · **Larry 83230~83234 active(재리뷰·재투표 대기)**.

### C-08 · docs/specs/SRS.md:1886 (§7.1.5 aud 주의 문단) · [thread 83156] · 💡 권장 · 초안(게시 전)
- **[민진우(Thomas)·Nemesis 🆔msfmxzzql · 83156]**
  > From Nemesis(v0.6.0, 🆔msfmxzzql),
  > **💡 권장**
  > `aud` 주의 문단이 GW Guard의 신뢰 기준을 "**GW 서명 + `iss` + `exp` + device 활성**"으로 나열하는데, 이 중 앞의 세 가지(서명·`iss`·`exp`)는 GW Guard가 §7.1.5 검증 절차 2단계에서 **실제로 대조·검증하는** 항목인 반면, "**device 활성**"은 GW Guard가 토큰만 보고는 확인할 수 없는 상태다(lifecycle/revocation은 §7.1.1·§7.2.4로 GW 소유이며, 시퀀스 다이어그램 라인 1920 "GW→GW: 토큰 서명·lifecycle 검증(등록·active)"처럼 **매 프록시 홉에서 GW edge가 재검증**해 보장한다). 즉 "device 활성"은 GW Guard가 *평가하는 기준*이 아니라 *GW가 상류에 보장해 주는 전제*(라인 1864 신뢰 모델)로, 성격이 다른 두 부류를 한 목록에 섞으면 구현자가 GW Guard에서 device 활성/폐기 상태를 별도 확인해야 한다고 오해할 수 있다. 라인 1909가 "토큰 폐기·rate-limit은 GW 담당 → 중복 관리 불필요"라고 이미 못박은 것과도 정합되도록, "device 활성"은 GW 서명·`iss`·`exp` 검증에 GW edge의 per-hop lifecycle 보장이 더해져 **간접 보장**됨을 명시하면 검증 항목과 전제가 분리돼 애매함이 사라진다.
- **[우리·판단]** 타당. GW Guard 검증 항목(서명·iss·exp)과 GW 보장 전제(device 활성=간접보장·GW 경유 한정) 분리. C-13·C-14와 정합.
- **[우리·답변 초안]**
  > 수용합니다. GW Guard가 실제 검증하는 항목(GW 서명·iss·exp)과 GW가 상류에서 보장하는 전제(device 활성)를 분리해 서술합니다. device 활성은 GW edge의 매 홉 lifecycle 재검증으로 간접 보장되며 이는 GW 경유 트래픽에 한정된다는 점(직접 경로엔 미치지 않아 TTL 상한으로 노출 창 제한)을 함께 명시해 검증 항목과 전제가 섞이지 않게 합니다.
- **[편집안]** §7.1.5 aud 주의 문단: 검증 항목/전제 분리 + GW 경유 한정 명시.
- **상태:** 게시완료(comment 2) · thread **resolved(fixed)**

### C-09 · (일반·총평 Update 2) · [thread 83157] · 초안(게시 전)
- **[민진우(Thomas)·Nemesis 🆔msfmxzzql · 83157]**
  > From Nemesis(v0.6.0, 🆔msfmxzzql, ⏱2m00s, 🔢295.2k in/7.4k out),
  > ## Code Review (Other) — Update 2
  > 이번 증분은 이전 리뷰의 유일한 잔여 지적(§7.1.5 line comment — `iss` 기대값 미명시 + 서명 바인딩 목록에서 `iss` 누락)을 완전히 해소했다. (a) 검증 2단계(라인 1870)가 "`iss`가 배포 설정에 고정된 그 리전 GW issuer 식별자와 일치"로 기대값을 명문화하고 1단계 JWKS URL 고정·3단계 `region` 교차검증과의 정합까지 서술했으며, (b) 신원 계약의 "서명 바인딩(신뢰 가능)" 목록(라인 1881)에 `iss`를 추가하고, 상류의 §7.1.1 Output(라인 1799)·§2.3.2(라인 714) 토큰 claim 목록에도 `iss`를 함께 반영해 계약 전반이 일관된다.
  > 구조적으로 나머지 신규 서술은 정합적이다. 구간별 헤더 표(라인 594)·③b 예시 HTTP(라인 643·645)·§7.1.5 본문·시퀀스 다이어그램·구현 책임 분담표가 모두 "GW는 ③b에서 자기 서명 device 토큰을 verbatim 전달, JWKS 공개 / CleverSpace GW Guard가 JWKS로 검증"이라는 한 계약으로 수렴한다. JWKS 호스트(`api.<region>.gw.<도메인>`)는 §7.1.1(라인 1804)·§7.1.5(라인 1869)에서 동일하게 고정됐고, 키 출처(Secrets Manager PEM·KMS CMK 아님·앱 동적 파생·프로비저닝=③-I) 서술도 §7.1.3.1과 어긋나지 않는다. 보안 8항목 표의 2컬럼(디바이스·프록시 면 / 운영자·관리 면) 분리와 `v1.1→gw/1.1` 버전 표기 정정, `scope` 예약(미사용) 정정도 §7.1.1·§7.2.2·§7.5.3과 정합한다. `aud` confused-deputy는 이전과 동일하게 "v1.0 의식적 수용"으로 acknowledged 되어 제외했다. 남은 지적은 위 line comment 한 건(신뢰 기준 목록에서 GW Guard가 *검증하는 항목*과 *GW가 보장하는 전제*의 분리)뿐이며 recommendation 수준이다.
  > 1 line-specific finding(s) were posted as inline comments.
- **[우리·판단]** 총평. 액션은 C-08. 반영 후 resolve.
- **[우리·답변 초안]**
  > 리뷰 감사합니다. 지적하신 검증 항목과 GW 보장 전제의 분리(위 line comment)를 반영했습니다.
- **상태:** 게시완료(comment 2) · thread **resolved(fixed)**

### C-10 · docs/specs/SRS.md:1865 (§7.1.5 신뢰 모델) · [thread 83230] · **[Block]** · 초안(게시 전)
- **[고형용(Larry) · 83230]**
  > **[Block] 신뢰 모델 — verbatim 이 포기한 속성을 문면이 여전히 주장합니다.**
  > verbatim 선택에는 동의합니다. "target 을 추가해도 상류 인증 로직을 target별로 늘리지 않는다" 는 근거는 저희가 어서션을 권장할 때 든 근거보다 상위입니다 — 저희는 CleverSpace 하나를 보고 권장했고 GW 는 N개 target 플랫폼을 봤습니다. 되돌릴 뜻이 없습니다.
  > 정정을 요청하는 것은 문면 하나입니다.
  > > "GW Guard 는 그 서명을 GW JWKS 로 검증하기만 하면 **'정품 GW 트래픽'임을 암호학적으로 확인**한다."
  > **서명 검증이 증명하는 것은 "GW 가 이 device 에게 이 토큰을 발급했다" 까지입니다.** "이 요청이 GW hop 을 지나왔다" 는 증명하지 못합니다. verbatim 토큰은 채널에 바인딩되지 않은 bearer 이고, DPoP(sender-constrained)는 §7.1.1 에서 gw/1.1 비목표입니다. 그리고 이건 **verbatim 을 고른 순간 원리적으로 사라진 속성**입니다 — 어서션이었다면 GW 개인키로만 만들 수 있는 객체가 hop 증거가 됐습니다. 즉 선택은 옳지만, 지불한 대가를 문면이 지불하지 않은 것처럼 적었습니다.
  > 그리고 CleverSpace 는 "GW 만 도달 가능" 이라는 네트워크 전제를 만족시킬 수 없습니다. 브라우저 SPA·게스트 공유 링크(경로 B)를 계속 열어둬야 하고(#12239 L89 스레드에서 EOS 제외로 합의), 그 ingress 는 같은 호스트입니다. 유효한 device 토큰 보유자는 GW 를 우회해 직접 호출할 수 있고 GW Guard 는 그것을 구분하지 못합니다.
  > **요청 3건 — 모두 문장 단위입니다.**
  > 1. 이 불릿의 결론을 "…GW 가 **이 device 에게 발급한 토큰임을** 암호학적으로 확인한다" 로 정정.
  > 2. 신뢰 모델에 전제 1줄 추가 — *"이 신뢰 모델은 GW Guard 가 붙은 라우트에 **GW 이외의 ingress 가 없을 때** 성립한다. 그 전제는 target 이 ingress 분리로 보장한다."*
  > 3. 절 끝 "요약(계약 한 줄)" 의 *"'GW 통과 요청'임을 확인하고"* 도 같은 취지로 정정.
  > *(CleverSpace 측 대응: GW Guard 라우트를 별도 host/ingress 로 정적 분리합니다. 요청 헤더 유무로 Guard 를 고르면 공격자가 Guard 를 고르게 되므로 데코레이터·호스트로만 선택합니다.)*
- **[우리·판단]** 정확. verbatim은 "발급 사실"만 증명, "홉 경유"는 증명 불가. 3건 모두 수용(문장 단위 정정).
- **[우리·답변 초안]**
  > 지적이 정확합니다. verbatim을 택한 이상 서명이 증명하는 것은 "GW가 이 device에게 이 토큰을 발급했다"까지이고, "GW 홉을 경유했다"는 채널 바인딩이 없어 증명되지 않는다는 데 동의합니다. 세 가지 모두 반영합니다. (1) 결론을 "GW가 이 device에게 발급한 토큰임을 암호학적으로 확인한다"로 정정, (2) 신뢰 모델에 전제 한 줄 추가 — 이 모델은 GW Guard 라우트에 GW 이외의 ingress가 없을 때 성립하며 그 전제는 target이 host/ingress 분리로 보장한다, (3) 요약의 "GW 통과 요청" 표현도 같은 취지로 정정. 브라우저 SPA·게스트 공유 경로가 같은 호스트로 열려 있다는 점과 Guard 라우트를 host/ingress로 정적 분리하는 대응도 이 전제와 정합합니다.
- **[편집안]** §7.1.5: (a) 결론 문면 정정 (b) 전제 1줄 추가(GW 이외 ingress 없음·target이 분리 보장) (c) 요약 한 줄 정정.
- **상태:** 게시완료(comment 2) · active(Larry 재리뷰 대기)

### C-11 · docs/specs/design/openapi/…openapi.yaml:1749 (TokenResponse.claims) · [thread 83231] · **[Block]** · 초안(게시 전)
- **[고형용(Larry) · 83231]**
  > **[Block] `aud` 예시가 §7.1.5 와 정반대이고 `iss` 가 빠졌습니다 — 그대로 두면 GW Guard 구현이 어긋납니다.**
  > **① `aud` 예시가 target 서브도메인입니다.** 반면 §7.1.5 는 *"v1.0 device 토큰의 `aud` 는 CleverSpace 로 못박혀 있지 않다(발급 시점에 대상 target 미정)"* 로 적었습니다.
  > `TokenRequest` 스키마를 확인하니 `grant_type`·`client_id`·`client_assertion_type`·`client_assertion`·`scope` 뿐이고 target/resource/audience 파라미터가 없으며 `scope` 는 v1.0 미사용·예약입니다. **GW 는 발급 시점에 대상 target 을 알 방법이 구조적으로 없으므로 §7.1.5 가 맞고 예시가 틀렸습니다.**
  > 실패 모드가 둘인데 두 번째가 더 나쁩니다.
  > - (i) 정본 예시를 따라 `aud === 'cleverspace.<region>.gw.<도메인>'` 검증을 넣으면 **100% 401**. 시끄럽게 실패하니 금방 발견됩니다.
  > - (ii) **"`aud` 가 target 에 묶여 있으니 confused-deputy 는 이미 닫혔다"** 로 오독. §7.1.5 가 **명시적으로 수용한 위험**을 닫힌 것으로 착각하고 넘어갑니다. 조용히 실패합니다.
  > **② `iss` 가 description 에 없습니다.** Update 1 이 §7.1.1 Output·§2.3.2·§7.1.5 서명 바인딩 목록에 `iss` 를 추가했는데 이 description 은 그대로 "device_id·region·aud·TTL" 입니다. §4.1 이 OpenAPI 를 스키마 정본으로 지정하므로 지금은 **정본이 본문보다 뒤처진 상태**입니다.
  > **요청**: description 에 `iss` 추가 + *"`aud` 는 target-scoped 가 아니다"* 한 줄 + 예시를 실제 발급값으로 교체(`iss` 포함). 두 줄 수정입니다.
  > 머지 전 처리를 부탁드립니다 — 가장 싸고, 정본이 구현을 틀리게 만드는 유일한 항목입니다.
- **[우리·판단]** 정확·최우선(정본이 구현을 오도). TokenRequest에 target 파라미터 없음 → 발급 시 target 모름 → §7.1.5가 맞고 예시가 틀림. 수용.
- **[우리·답변 초안]**
  > 정확한 지적이라 머지 전에 반영합니다. TokenRequest에 target/resource/audience 파라미터가 없고 scope도 v1.0 미사용이라 GW는 발급 시점에 대상 target을 알 수 없으므로 §7.1.5가 맞고 OpenAPI 예시가 틀렸습니다. aud 예시를 target 서브도메인에서 실제 발급값으로 교체하고 "aud는 target-scoped가 아니다(confused-deputy는 v1.0 의식적 수용)"를 description에 명시하며, iss를 description과 예시에 추가해 OpenAPI 정본을 §7.1.1·§7.1.5 본문과 일치시킵니다.
- **[편집안]** OpenAPI TokenResponse.claims: aud 예시 교체(비-target `GW`) + "aud target-scoped 아님" 1줄 + iss description·예시 추가.
- **상태:** 게시완료(comment 2) · active(Larry 재리뷰 대기)

### C-12 · docs/specs/SRS.md:1870 (§7.1.5 검증 2단계) · [thread 83232] · [Suggestion] · 초안(게시 전)
- **[고형용(Larry) · 83232]**
  > **[Suggestion] `iss` 기대값의 형식이 정의되지 않았습니다.**
  > Update 1 로 `iss` 검증이 규범이 됐는데, **`iss` 값의 형식이 SRS·OpenAPI 어디에도 없습니다.** SRS 전문에서 `issuer` 는 §7.1.4(Entra) 맥락 1건뿐이고, OpenAPI `TokenResponse.claims` 예시에도 `iss` 가 없습니다.
  > GW Guard 는 이 값을 배포 설정에 고정해 대조해야 하므로, 형식이 없으면 저희가 추측하게 됩니다. 후보가 최소 넷입니다 — `https://api.<region>.gw.<도메인>` / `api.<region>.gw.<도메인>` / `https://api.<region>.gw.<도메인>/v1` / 리전 라벨 또는 불투명 문자열. 틀리면 전건 401 이고, 이 절이 실패를 401 로 규정했으므로 원인 진단도 어렵습니다.
  > **제안**: §7.1.1 Output 또는 이 절에 `iss` 값의 **형식 1줄**. `TokenResponse.claims` 예시에 실제 `iss` 값을 함께 넣어주시는 것으로도 충분합니다.
  > 값·형식·기재 위치의 판단은 GW 에 맡깁니다. 정해진 형식만 알려주시면 저희가 설정으로 고정합니다.
- **[우리·판단]** 타당. iss 형식 확정 필요. 제안: `https://api.<region>.gw.<도메인>`(리전 GW 베이스 URL·https·후행 경로 없음). 수용.
- **[우리·답변 초안]**
  > 반영합니다. iss 형식을 §7.1.1 Output에 명시합니다 — iss = https://api.<region>.gw.<도메인> (그 리전 GW 베이스 URL·https·후행 경로 없음). TokenResponse.claims 예시에도 이 값을 넣어 설정으로 고정하실 수 있게 합니다.
- **[편집안]** §7.1.1 Output + OpenAPI 예시: iss 형식 `https://api.<region>.gw.<도메인>`.
- **상태:** 게시완료(comment 2) · active(Larry 재리뷰 대기) · 확정: iss=`https://api.<region>.gw.<도메인>`

### C-13 · docs/specs/SRS.md:1909 (§7.1.5 "중복 관리 불필요") · [thread 83233] · [Suggestion] · 초안(게시 전)
- **[고형용(Larry) · 83233]**
  > **[Suggestion] "중복 관리 불필요" 는 GW 경유 트래픽에 한정해서만 성립합니다.**
  > > "토큰 폐기(`jti`)·rate-limit 은 GW 가 담당(§7.1.1)하므로 **중복 관리 불필요**."
  > 직접 호출 경로에는 **revocation(§7.2.4 즉시 차단)도, kill-switch(§7.8.2)도, rate-limit 도 미치지 않습니다.** 무상태 검증만 하는 GW Guard 는 revoke 된 device 의 토큰을 TTL 만료까지 그대로 받습니다.
  > 그리고 CleverSpace 가 이를 대체할 수단이 없습니다. #12239 스레드(③b 신원 전달)에서 *"EzServer 유효성 권위·해지 전파는 CleverSpace/OneID 쪽에서 정리"* 로 정리됐는데, 해지에는 두 방향이 있습니다.
  > - **OneID 발 해지**(EzServer 가 OneID 에서 해지) — CleverSpace/OneID 가 처리합니다. 이 부분은 말씀대로입니다.
  > - **GW 발 해지**(device revocation·kill-switch) — **GW 만 알고 있고 target 에 조회 수단이 없습니다.**
  > 회귀는 아닙니다 — 오늘 EzServer 경로도 무상태입니다. 새로운 것은 **발급 권한이 GW 로 옮겨가는데 집행은 GW 경유 경로에만 남는다**, 즉 권한과 집행점이 분리되는 구조입니다.
  > **제안**:
  > 1. 이 문장에 **"단 GW 경유 트래픽에 한정"** 한정어 추가.
  > 2. 아래 중 최소 하나 — (a) device 상태 조회 API(내부 B target 용) (b) revocation webhook (c) `expires_in` 상한 규범화(별 스레드). **(c) 가 가장 쌉니다** — target 이 못 하는 것을 "계약으로 상한이 있는 것" 으로 바꿔 줍니다.
  > 어느 쪽이 GW 로드맵에 맞는지는 GW 판단에 맡깁니다. (a)·(b) 가 부담이면 (c) 만으로도 저희는 위험을 정량화할 수 있습니다.
- **[우리·판단]** 정확. 권한(GW 발급)과 집행(GW 경유만)의 분리 구조 인정. v1.0=(c) TTL 상한 채택(C-14와 짝), (a)·(b)는 gw/1.1+. 수용.
- **[우리·답변 초안]**
  > 동의합니다. 발급 권한은 GW로 옮겨갔는데 집행(revocation·kill-switch·rate-limit)은 GW 경유 경로에만 미친다는 구조가 맞습니다. 해당 문장에 "GW 경유 트래픽에 한정" 한정어를 추가하고, 직접 호출 경로의 노출 창은 device access token TTL 상한으로 제한합니다(가장 싼 (c)안·아래 TTL 스레드와 함께). device 상태 조회 API와 revocation webhook은 gw/1.1+ 후속으로 남깁니다.
- **[편집안]** §7.1.5: "GW 경유 한정" 한정어 + 직접 경로 노출 창=TTL 상한 제한 + (a)·(b) gw/1.1+ 후속.
- **상태:** 게시완료(comment 2) · active(Larry 재리뷰 대기) · 확정: (c) TTL 상한(≤15분)·(a)(b) gw/1.1+

### C-14 · docs/specs/SRS.md:1790 (§7.1.1 Output) · [thread 83234] · [Suggestion] · 초안(게시 전)
- **[고형용(Larry) · 83234]**
  > **[Suggestion] device access token TTL 의 규범값·상한이 없습니다.**
  > Output 은 `expires_in`(초)만 규정하고 **숫자를 정하지 않습니다.** OpenAPI `TokenResponse` 예시에 `900` 이 있지만 예시일 뿐입니다.
  > §7.1.5 의 무상태 검증 모델 때문에 이 값이 필요합니다 — **직접 호출 경로에서 revoke 된 device 가 계속 통과하는 창의 길이가 곧 이 TTL** 입니다. 규범값이 없으면 (i) GW Guard 측이 "허용 가능한 노출 창" 을 판단할 근거가 없고 (ii) GW 가 운영 중 값을 바꾸면 **target 의 위험도가 조용히 변합니다.**
  > **제안**: 이 Output 항에 device access token TTL 의 **규범값 또는 상한**(예: ≤15분) 명시.
  > 구체 값은 GW 운영 판단에 맡깁니다. 상한이 계약에 있기만 하면 저희는 그것을 전제로 설계할 수 있습니다.
- **[우리·판단]** 정확(C-13과 짝). 직접 경로 revocation 창 = TTL. 규범 상한 명시. 제안: ≤15분(값은 상한 내 GW 판단). 수용.
- **[우리·답변 초안]**
  > 반영합니다. §7.1.1 Output에 device access token TTL의 규범 상한을 명시합니다(≤15분 제안 — 직접 호출 경로의 revocation 지연 창이 곧 이 TTL이므로 상한을 계약으로 둡니다). 구체 값은 상한 내에서 GW 운영 판단으로 정하되, 상한 자체는 계약에 남겨 target이 위험을 정량화할 수 있게 합니다.
- **[편집안]** §7.1.1 Output: device access token TTL 규범 상한(≤15분) 명시 + OpenAPI 정합.
- **상태:** 게시완료(comment 2) · active(Larry 재리뷰 대기) · 확정: `expires_in` ≤15분

---

## 요약 (처리 현황)
- **Scott(필수): 승인 완료.** **Larry(필수): voted -5(작성자 대기)** — Update 2로 [Block] 2·[Suggestion] 3 제기(C-10~C-14). verbatim 결정엔 동의하며 문면·계약 정밀화 요청 → **전건 반영·답변 게시완료(push `2a16391`) → Larry vote 10 → #12440 병합 완료(2026-08-06)**.
- **Nemesis 4건 전부 반영·push 완료**(`a6044df`): C-01 보안 수정(JWKS 신뢰 URL 고정·region 검증 후 교차검증) + C-02 rate-limit/CDN 전제 + C-03 Cache-Control 헤더 계약.
- **답변 5건 게시 완료**(2026-08-05·전규현 명의·초기 라운드).
- **Update 1(재검토·Nemesis)**: 이전 3건 해소 확인 + 잔여 💡 1건(C-06 `iss` 정밀화) **반영·push(`0a914c0`)·답변 게시 완료**.
- **Nemesis 스레드 6건(83087~83090·83141·83142) 전부 resolved(fixed).** Scott 승인 스레드(83105)만 그대로 둠.
- **Update 2(2026-08-06):** Larry [Block]2·[Suggestion]3 + Nemesis 권장1(C-08~C-14) 전건 수용 — **편집 push(`2a16391`)·답변 7건 게시·Nemesis(83156·83157) resolve 완료**.
- **처리 완료:**
  - ① **확정 4건 완료** — TTL `expires_in` ≤15분 · iss `https://api.<region>.gw.<도메인>` · aud=`GW`(비-target) · revocation=(c) TTL 상한((a)(b) gw/1.1+).
  - ② **§7.1.5·§7.1.1 Output·OpenAPI 편집 push(`2a16391`)·답변 7건 게시·Nemesis 스레드 resolve 완료** · Larry 스레드(83230~83234) active(재리뷰 대기).
- **병합 완료(2026-08-06):** #12440 Larry vote 10 승인 → 병합 · #12453(리전/Console)도 병합 · **baseline 태그 `spec-v1.0.11` 부여**(`a57dcf2`) · Console Sub-SRS parent 핀 v1.0.10→v1.0.11 스윕 완료.
- **잔여:**
  - IP 갱신·구현세션 통지(§7.1.5 ③b 계약·TTL ≤15분·iss 형식 `https://api.<region>.gw.<도메인>`).
  - CleverSpace 측 OnePager(#12463·Larry·ezcloud) 회신 — P0-3 2건(OpenAPI 소스 자동생성 원칙·행위자 신원 문안) 처리 계획. 우리 #12440 반영은 정확히 옮겨짐(spot-check 확인).
