# ③ GW SRS — 리뷰 코멘트 추적 (③b verbatim + JWKS 승격 · PR #12440)

> **작업용 문서**. 각 스레드=코멘트 원문 전체 + 우리 판단·답변·조치. **답변 5건은 2026-08-05 전규현 명의로 게시 완료.** 반영=vt-api-gateway `spec/cleverspace-3b-verbatim-jwks` 브랜치(`a6044df` push 완료).

- **PR**: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/12440
- **주제**: ③b(GW→CleverSpace) 신원 전달 = device 토큰 verbatim + GW JWKS v1.0 승격 · §7.1.5(GW Guard 검증 계약)·`/.well-known/jwks.json` 신설 · scope 문면 정정
- **리뷰어**: Larry·Scott(필수) · Jack·Teddy·Thomas(옵션) · 우리=전규현
- **커밋**: `88b17da`(원안) + `a6044df`(리뷰 반영분·**push 완료** 2026-08-05)
- **최종 fetch**: 2026-08-05 (Update 1 포함) · 유효 thread 7건(초기 Nemesis 4 + Scott 승인 1 + **Update 1 Nemesis 2**) + 시스템 thread(리뷰어 지정·voted·push 알림)
- **상태**: **Scott 승인 완료**(voted 10·aud 위험 수용) · Nemesis 🔧1·💡2·총평1 = **push 완료(a6044df)** · **답변 5건 게시 완료**

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

## 요약 (처리 현황)
- **Scott(필수): 승인 완료.** Larry(필수): 미투표(리뷰 대기).
- **Nemesis 4건 전부 반영·push 완료**(`a6044df`): C-01 보안 수정(JWKS 신뢰 URL 고정·region 검증 후 교차검증) + C-02 rate-limit/CDN 전제 + C-03 Cache-Control 헤더 계약.
- **답변 5건 게시 완료**(2026-08-05·전규현 명의·초기 라운드).
- **Update 1(재검토·Nemesis)**: 이전 3건 해소 확인 + 잔여 💡 1건(C-06 `iss` 정밀화) **반영·push(`0a914c0`)·답변 게시 완료**.
- **Nemesis 스레드 6건(83087~83090·83141·83142) 전부 resolved(fixed).** Scott 승인 스레드(83105)만 그대로 둠.
- **미결:** ① **Larry 리뷰(대기·필수)** · ② 병합 후 태그 `spec-v1.0.11`·IP 갱신·구현세션 통지 · ③ Console Sub-SRS parent 핀 v1.0.10→v1.0.11(병합 후).
