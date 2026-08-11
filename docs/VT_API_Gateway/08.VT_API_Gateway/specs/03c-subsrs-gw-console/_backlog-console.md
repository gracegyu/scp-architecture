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
