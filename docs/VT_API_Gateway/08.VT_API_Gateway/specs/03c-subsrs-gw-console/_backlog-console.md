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

### CB-1. [gw/1.2] 멀티리전 운영자 authz — Console 반영 (주간회의 8/6 R1)
- **운영자 멀티리전 authz UX.** 승인 시 **리전 스코프 선택**(all / 특정 리전 · admin·dev 기본 all-regions) · **리전 전환**(전역 Console) · **전역 admin 서사**. → §2.1.2·§2.3.6·§4.2·§7.2 반영.
- **ZTNA 제거 → 접근 통제 = 직원 IdP(Entra).** R1에서 Zero Trust 폐기·Entra only 확정. Console SRS의 ZTNA 참조를 정리한다: **§1.4(용어)·§1.7.1·§2.1(외부 시스템·다이어그램)·§2.1.1/2.1.2 다이어그램·§2.3 다이어그램·§2.6(접근 경계)·§3.1.2·§3.3.2**. 호스팅 = **S3 + CloudFront** 유지.
- **부모 의존.** 계약(`operator_role` 전역 복제·`regionScope`·§4.5.1 ZT→CloudFront·내부 Admin API 도달 경로)은 **부모 백로그 B-7**. 부모 확정 후 Console 반영.
- **트리거.** gw/1.2 · 부모 B-7 확정 후. **v1.0 단일 리전 구현 무영향**(방향만 R1로 확정).
- **출처.** 2026-08-06 주간회의 R1(아카이브 「8/6 결정사항」 R1).

### CB-2. Console v1/v2 분리 · v1.0 최소기능 선행 · 기술 스택 확정 (R5 · 7/30 확정 → 8/6 재확인)
- **v1/v2 분리 · v1.0 최소기능 선행.** v1.0 = 온보딩·디바이스 승인 Flow 동작 최소 스펙 선행, v2.0 후속(7/30 R5·8/6 재확인). 이미 §1.3 단계 규약·§2.7·`기능-v1-v2-분리.md`에 반영 → **추가 작업 없음(확인)**.
- **기술 스택 확정 (2026-08-06).** **Next.js + Refine + shadcn/ui(Radix UI primitives + Tailwind) + TanStack Query.** UI 킷 = **shadcn/ui 확정**(§3.4.2의 "Ant Design 또는 shadcn/ui" → shadcn/ui). Console SRS §2.2·§3.4.2·Appendix C-4·핵심 결정 B의 "권장·LLD 확정" → **"확정"** 으로 승격. *LLD 참고: shadcn/ui는 Refine의 1급 UI 통합(Ant/MUI/Chakra/Mantine)이 아니라 Radix+Tailwind 컴포넌트를 직접 두는 방식이므로, **Refine은 headless(data/auth/routing provider)로 쓰고 UI는 shadcn으로 구성**한다.*
- **internal API = Console 소관 아님.** Console은 **자체 백엔드/internal API를 두지 않고** GW Admin API를 직접 소비(SPA·GW=SoT). Admin API 내부 접근 통제는 GW/③-I 소관. 이미 §1.2 Scope 반영 → 추가 작업 없음(확인).
- **트리거.** Console SRS 다듬기(스택 캐비엇 제거) — 저위험·baseline 전 반영 가능.
- **출처.** 2026-08-06 R5(7/30 R5 계승).
