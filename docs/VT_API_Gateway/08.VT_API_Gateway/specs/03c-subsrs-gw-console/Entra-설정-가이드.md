# Entra 설정 가이드 — GW 운영자 인증 (운영 런북)

> **성격:** 운영 런북(**living doc**) — SRS 아님. Console SRS(§3.2·§7.1)·GW SRS(부모 §7.1.4·§7.9.2)가 규정한 *인증 요구*를 실제 MS Entra에 **설정하는 절차**를 담는다.
> **소유:** IT(Entra 관리자) + ③-I. **공용:** GW Console(UI)뿐 아니라 GW(토큰 검증)가 함께 쓰는 사내 운영자 인증이므로 **GW 공용**이다.
> **상태:** 스켈레톤(2026-08-04). 구체값(클레임·앱 역할·리다이렉트 URI·테넌트)은 IT/③-I가 확정하며 미확정은 `TBD(결정자·시점)`로 표기(Console SRS Appendix B C-2).

---

## 0. 왜 이 문서 (SRS와의 경계)
- **SRS(요구·계약):** OIDC 플로우(Auth Code+PKCE), 앱이 소비하는 config 키(issuer·clientId·audience·redirect), 필요 클레임/앱 역할→`operator_role_type` 매핑.
- **본 가이드(절차·How):** 위 요구를 만족시키기 위해 Entra에서 *무엇을 어떻게 등록*하는지. controlled document(SRS)에 넣지 않는다.

## 1. 등록 대상 요약 (IT가 만들어야 할 것)
| # | 항목 | 값(예시/규약) | 상태 |
| --- | --- | --- | --- |
| 1 | **테넌트** | 사내 Entra 테넌트 | TBD(IT) |
| 2 | **앱 등록(App registration)** | GW Console SPA (공개 클라이언트·PKCE·client secret 없음) | TBD(IT) |
| 3 | **리다이렉트 URI** | **환경별 전역 단일 콘솔**(리전 라벨 없음) — prod `https://console.gw.<도메인>/auth/callback` · dev `https://console.gw.dev.ezcld.net/auth/callback` · **local** `http://localhost:3100/auth/callback`(Console dev 포트 = **3100**·GW core(3000)와 충돌 회피 — SPA redirect는 **포트 정확 일치**라 wildcard 불가·**dev 앱 등록에 추가**·별도 앱 아님·mock 경로는 redirect 불요) · **격리 존**(중국 등)은 그 존 전용 호스트별 추가 · 각 로그아웃 URI | **dev·localhost=지금 등록 가능**(dev 도메인 ezcld.net 확정) · **prod=`<도메인>` 확정 후**(C-10) |
| 4 | **토큰 audience/issuer** | GW가 검증할 audience·issuer(부모 §7.1.4) | TBD(IT+GW) |
| 5 | **앱 역할 또는 그룹** | `admin`·`cs`·`operator`·`developer` 클레임 발급 → GW가 `operator_role`로 매핑 | TBD(IT+GW) |
| 6 | **환경별 분리** | dev/staging/prod 앱 등록(또는 테넌트) 분리 | TBD(IT/③-I) |

## 2. 절차 (초안 — IT가 확정·보강)
> 포털/CLI 단계는 IT가 표준 절차로 채운다. 아래는 앱 요구에서 도출한 **체크리스트**다.
1. 앱 등록 생성(SPA·PKCE). client secret 미발급(공개 클라이언트).
2. 리다이렉트 URI 등록(리전별 콘솔 호스트·로그아웃 URI).
3. ID 토큰 클레임에 **역할/그룹**을 실어 발급하도록 구성(앱 역할 or 그룹 클레임).
4. GW 토큰 검증 config(issuer·audience·JWKS)와 정합 확인(부모 §7.1.4).
5. 오프보딩 = Entra 계정 비활성(→ Console은 `suspended` 표시·§7.2).
6. 환경별(dev/staging/prod) 반복.

## 2-A. 로컬 개발 인증 (구현 착수·local 테스트)
**Entra 프로비저닝을 기다리지 않고** 로컬에서 개발·테스트할 수 있다 — Entra 설정은 구현 착수의 blocker가 아니다(단 claim/역할 형식은 GW authz 매핑에 영향이라 IT 확정을 **병렬로 일찍** 진행).
1. **(권장·1차) OIDC mock** — `AUTH_MODE=mock`(Console SRS §3.4)로 Entra를 우회하고 **역할·claim을 주입**해 로그인·부트스트랩 분기(active/no_access/suspended)·RBAC 게이팅을 개발한다. Entra 없이 단위·컴포넌트·로컬 e2e 대부분을 커버(인력·속도 최적). **prod 금지**(dev/local 전용).
2. **(2차) 실 dev 테넌트 + localhost** — 실 `claim→operator_role` 매핑 경로처럼 mock으로 못 잡는 것을 검증할 땐, **dev 앱 등록에 `http://localhost:3100/auth/callback` 리다이렉트 URI를 추가**하고 로컬에서 **dev Entra 테넌트로 실제 로그인**한다. ⚠ **SPA redirect는 포트를 정확히 일치**시켜야 등록되므로(native loopback과 달리 포트 wildcard 불가) **Console dev 포트를 3100으로 고정**한다(Next.js 기본 3000이 **GW core(3000)와 충돌**하므로 변경 — admin=3001·receiver=3002·dispatcher=3003과도 안 겹침). 다른 포트를 쓰면 그 포트도 각각 등록해야 하니 **3100으로 표준화**(별도 앱 등록은 불요). *mock 경로(1)는 OIDC를 우회하므로 이 redirect가 필요 없다.*
3. **환경 진행 순서** — local(mock → 필요 시 dev 테넌트+localhost) → **staging/e2e = 실 dev/test 테넌트**(§3.5·실 OIDC·claim→역할 검증) → prod. local은 **dev 앱 등록에 localhost redirect를 얹는 것**이지 별도 환경 등록이 아니다(위 표 #6의 dev/staging/prod 분리와 구분).

## 3. 앱↔Entra 계약 (변경 시 SRS 영향)
- 역할 클레임 이름·형식이 바뀌면 **GW authz 매핑·Console 역할 게이팅**(부모 §7.9.2·Console §7.2)에 영향 → 변경 관리.
- 리다이렉트 URI는 도메인(§R4 `<도메인>`) 확정에 종속.

## 4. 미결 (IT/③-I 확정)
- C-2(Console SRS Appendix B): 테넌트·앱 등록·claim/역할 구체값.
- 역할=Entra 앱 역할 vs 그룹 클레임 중 택(운영 편의·GW 매핑 방식과 함께 확정).
