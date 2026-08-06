# ③-P-CS CleverSpace GW 적응 OnePager — #12463(완성본) 리뷰·회신

> **작업용 문서.** Larry(CleverSpace)가 올린 **PR #12463**(OnePager 완성본 · GW #12440 반영)에 대한 우리(GW) 리뷰·회신 추적.
>
> **처리 방침**(기존과 동일): 편집 소유 = CleverSpace(Larry). 우리는 **GW 계약 확인·답변만** 하고 그쪽 문서를 편집하지 않는다. PR엔 **전체 코멘트 1건**으로 회신한다. #12239 1차 인계 리뷰는 동 폴더 `_review-log-12239.md` 참조.

- **PR**: https://dev.azure.com/ewoosoft/ezicloud/_git/ezcloud/pullrequest/12463 (Larry · `docs(onepager): CleverSpace GW 적응 OnePager — 인계 리뷰 반영`)
- **문서**: `ezcloud:/docs/onepager/gw_adaptation/CleverSpace-GW적응-OnePager.md` (base=`docs/gw-adaptation-onepager` · #12239 머지 후 main 전환)
- **관계**: #12239(우리 인계 초안 · `_review-log-12239.md` P0 3건) → thread 83069로 편집 소유 CleverSpace 이관 → **#12463 = 완성본**(우리 인계 리뷰 12건 + GW #12440 ③b 계약 반영).
- **상태**: **회신 게시 완료**(2026-08-06 · thread 83311 · 전체 코멘트 1건). GW 측 확인 = 계약 정확 반영 + P0-3 2건 답변. Approve 대기(GW 사인오프).

---

## 1. 리뷰 — GW #12440 계약 반영 정확도: ✅ 정확 (spot-check·실파일 대조)

| 우리 계약(#12440 · §7.1.5 · §7.1.1 Output) | OnePager #12463 반영 |
| --- | --- |
| iss=`https://api.<region>.gw.<도메인>`(후행 경로 없음) | ✅ 동일 문안 |
| device access token TTL 규범 상한 ≤15분 | ✅ (직접 호출 경로 revoke 노출 창 = 최대 15분 명시) |
| 서명=발급 사실까지 · verbatim은 홉 경유 미증명 · ingress 분리 전제 | ✅ 신뢰모델·요약 양쪽 |
| aud는 target-scoped 아님 · GW 수준 값 | ✅ description·예시 |
| "중복 관리 불필요" = GW 경유 트래픽 한정 | ✅ 한정어 반영 |

→ 우리 Update 2(C-08~C-14)를 정확히 옮김. **추가 정정 요청 없음.** (P0-1 ③b · P0-2 매핑 · P0-4 ingress = GW 측 닫힘. N1 리전 부정합 = Larry 철회.)

## 1b. CleverSpace 테넌트 모델 확인 (사장님 요청 · `references/CleverSpace/Confidential_EzCloud_v1.0_SRS.md` 대조)
- **테넌트 관리 = OneID.** EzServer는 테넌트 소유자가 OneID 로그인해 **로그인한 테넌트에 등록**되고 **EzServer UID**를 발급받는다(EzCloud SRS §OneID 연동 설정).
- **EzServer↔테넌트 다중성 = CleverSpace 소관 · GW 무관.** EzCloud(CS) **v1.0은 테넌트당 EzServer 1개로 제한**(다중 EzServer 역량은 OneID에 있으나 EzCloud v1.0 미지원·SRS line 61~70) — 이는 **CleverSpace v1.0의 제약**이지 GW 제약이 아니다. 다중 EzServer여도 **같은 ClinicID/테넌트를 공유**하고 GW는 그 수를 알 필요가 없다. GW가 의존하는 불변식은 "**각 `device_id`가 단일 tenant로 귀속**"(device→tenant는 1:1이든 many-to-one이든)이며 CleverSpace/OneID가 `device_id → (tenantUid, ezServerUid)`로 해석한다. **우리 §7.1.5 매핑은 EzServer 수와 무관하게 성립**(모순 없음).
- **멀티테넌트 DB**(단일 스키마·`tenant_uid` 키·S3 `{tenant_uid}/…`)·테넌트 격리는 **앱 계층**(EzCloud SRS §6).
- **member(사용자) = OneID 테넌트 사용자.** 신원은 **EzCloud App ↔ OneID 직접 로그인 경로**에서 성립하며 **③b 머신 경로(Imaging App→EzServer→GW→EzCloud API)와 분리**된다.
- **결론**: 우리 답변의 방향(각 device→단일 tenant · member는 GW 토큰에 없음)은 **정확**. 단 P0-3 ②의 "CleverSpace 세션으로 판정" 표현만 정정 — ③b 머신 경로엔 **사용자 세션이 없어** 세션에서 member를 유도할 수 없고, 필요 시 **애플리케이션 계층**(발신 앱 페이로드)에서 온다. (테넌트당 EzServer 다중성은 CS 소관·GW 무관 — "1:1" 의존 표현 제거.)

## 2. Larry 요청 P0-3 2건 — 우리 답변

### P0-3 ① gw/1.1+ endpoint 정책 = OpenAPI 소스 자동생성(수기 목록 금지)
**동의.** v1.0 GW 인가는 coarse(유효 토큰 + 등록 target 도달 허용 · `scope` 예약·미사용 · §7.5.3·§6.2)라 per-endpoint 목록이 없다. gw/1.1+에서 세분화 endpoint·scope 정책을 도입할 때 target별 허용 endpoint 집합은 **그 target의 OpenAPI에서 자동 생성**하고 수기 목록은 두지 않는다(drift 방지·target-agnostic 유지). 리소스 인가 권위가 CleverSpace라는 점은 그와 별개로 유지(§4.1.2·§6.2). → gw/1.1+ 설계 항목.

### P0-3 ② 행위자(member) 신원 문안
GW ③b 토큰의 **행위자 = device(EzServer)**이며 `device_id`로 서명 바인딩된다(§7.1.5). CleverSpace/OneID가 `device_id → (tenantUid, ezServerUid)`를 소유·해석하며 **각 device는 단일 tenant로 귀속**된다 — GW 신원 해석의 최소 단위는 **device → tenant**까지다. (테넌트당 EzServer가 1개든 여럿이든 무관 — 다중이면 같은 ClinicID/테넌트를 공유하고 GW는 그 수를 알 필요가 없다. EzCloud v1.0의 "테넌트당 1개"는 CS 제약이다.) **개별 member(사용자) 신원은 GW 토큰에 없고 GW가 발급·전달하지 않는다.** CleverSpace의 member/user 신원은 **별도 사용자 로그인 경로(EzCloud App ↔ OneID)** 에서 성립하며 **③b 머신 경로에는 사용자 세션이 없다**. 따라서 ③b 경로 행위에 member 귀속이 필요하면 그것은 **애플리케이션 계층**(발신 앱이 요청 페이로드로 전달)의 몫이지 GW ③b 전송 계약이 아니다(CleverSpace 세션에서 유도 불가).

## 3. 회신 초안 (PR #12463 전체 코멘트 · 서술문 · 이모지/님 없음)

```
검토했습니다. #12440에서 확정한 ③b 계약이 문서에 정확히 반영됐습니다 — iss 형식,
device access token TTL 상한(≤15분), 서명이 증명하는 것은 발급 사실까지라는 정정과
ingress 분리 전제, aud가 target-scoped가 아니라는 점, "중복 관리 불필요"의 GW 경유
트래픽 한정까지 저희 반영분과 일치합니다. 추가로 정정할 것은 없습니다.

P0-3 두 건에 답합니다.

첫째, gw/1.1+ endpoint 정책의 OpenAPI 소스 자동생성 원칙에 동의합니다. v1.0 GW
인가는 coarse(유효 토큰과 등록 target 도달 허용, scope는 예약·미사용)라 per-endpoint
목록이 없습니다. gw/1.1+에서 세분화 endpoint·scope 정책을 도입할 때 target별 허용
endpoint 집합은 그 target의 OpenAPI에서 자동 생성하며 수기 목록은 두지 않습니다
(drift 방지·target-agnostic 유지). 리소스 인가 권위가 CleverSpace라는 점은 그와
별개로 유지됩니다.

둘째, 행위자 신원은 GW ③b 토큰 기준으로 device(EzServer)이며 device_id로 서명
바인딩됩니다. CleverSpace/OneID가 device_id를 (tenantUid, ezServerUid)로 해석하며
각 device는 단일 tenant로 귀속되고, GW 신원 해석의 최소 단위는 device에서 tenant
까지입니다(테넌트당 EzServer 수는 CleverSpace 소관이라 GW는 무관합니다). 개별
member(사용자) 신원은 GW 토큰에 없고 GW가 발급·전달하지 않습니다. member 신원은 CleverSpace의 별도 사용자 로그인 경로(EzCloud App과 OneID)
에서 성립하며 ③b 머신 경로에는 사용자 세션이 없으므로, ③b 경로 행위에 member 귀속이
필요하다면 그것은 발신 애플리케이션이 요청 페이로드로 전달하는 애플리케이션 계층의
몫이고 GW ③b 전송 계약 밖입니다.
```
