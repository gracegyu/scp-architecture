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
| 3 | **리다이렉트 URI** | **환경별 전역 단일 콘솔**(리전 라벨 없음) — prod `https://console.gw.<도메인>/auth/callback` · dev `https://console.gw.dev.ezcld.net/auth/callback` · **격리 존**(중국 등)은 그 존 전용 호스트별 추가 · 각 로그아웃 URI | TBD(도메인 확정 후) |
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

## 3. 앱↔Entra 계약 (변경 시 SRS 영향)
- 역할 클레임 이름·형식이 바뀌면 **GW authz 매핑·Console 역할 게이팅**(부모 §7.9.2·Console §7.2)에 영향 → 변경 관리.
- 리다이렉트 URI는 도메인(§R4 `<도메인>`) 확정에 종속.

## 4. 미결 (IT/③-I 확정)
- C-2(Console SRS Appendix B): 테넌트·앱 등록·claim/역할 구체값.
- 역할=Entra 앱 역할 vs 그룹 클레임 중 택(운영 편의·GW 매핑 방식과 함께 확정).
