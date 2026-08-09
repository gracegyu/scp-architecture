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

### CB-1. [gw/1.2] 멀티리전 운영자 authz — Console 반영 (주간회의 8/6 R1) — ✅ **완료(v0.14·2026-08-10)**
- **ZTNA 제거 → 접근 통제 = 애플리케이션 계층 Entra.** ✅ 반영: §1.4·§2.1 외부표·§2.1.1/2.1.2 다이어그램·§2.3 S1·§2.6·§3.1.2·§3.3.2·§4.5·§6.2·Appendix C-3에서 ZTNA/Zero Trust 스윕 → **Entra 인증(OIDC + operatorAuth)**. 호스팅 = **S3 + CloudFront** 유지. **Admin API=Entra-gated 공개**(부모 #12487·내부전용/mesh DENY 폐기)·전역 Console origin CORS 명시.
- **운영자 멀티리전 authz UX.** ✅ 반영: 부모 최종 결정이 **역할 전 리전 균일 sync·regionScope 제거**라, grant별 리전 스코프 선택 UI는 두지 않음(§7.2 note). 리전 스위처(FR-CON-03)는 운영 base 선택뿐(기존과 정합). 전역 admin 서사 유지.
- **부모 의존.** 부모 B-7 = **#12487 병합·`spec-v1.0.12`**(regionScope 제거·§4.5.1 Admin Entra-gated 공개). Console 핀 v1.0.12로 갱신. **복제 계층 구현은 gw/1.2**(v1.0 단일 리전 무영향).
- **출처.** 2026-08-06 주간회의 R1.

### CB-2. Console v1/v2 분리 · v1.0 최소기능 선행 · 기술 스택 확정 (R5 · 7/30 확정 → 8/6 재확인) — ✅ **완료(v0.14·2026-08-10)**
> 기술 스택 = **Next.js + Refine(headless) + shadcn/ui(Radix+Tailwind) + TanStack Query** 확정 반영(§2.2·§3.4.2·§6.5·Appendix A B·C-4 해소). v1/v2 분리·internal API 미보유는 기반영 확인.
- **v1/v2 분리 · v1.0 최소기능 선행.** v1.0 = 온보딩·디바이스 승인 Flow 동작 최소 스펙 선행, v2.0 후속(7/30 R5·8/6 재확인). 이미 §1.3 단계 규약·§2.7·`기능-v1-v2-분리.md`에 반영 → **추가 작업 없음(확인)**.
- **기술 스택 확정 (2026-08-06).** **Next.js + Refine + shadcn/ui(Radix UI primitives + Tailwind) + TanStack Query.** UI 킷 = **shadcn/ui 확정**(§3.4.2의 "Ant Design 또는 shadcn/ui" → shadcn/ui). Console SRS §2.2·§3.4.2·Appendix C-4·핵심 결정 B의 "권장·LLD 확정" → **"확정"** 으로 승격. *LLD 참고: shadcn/ui는 Refine의 1급 UI 통합(Ant/MUI/Chakra/Mantine)이 아니라 Radix+Tailwind 컴포넌트를 직접 두는 방식이므로, **Refine은 headless(data/auth/routing provider)로 쓰고 UI는 shadcn으로 구성**한다.*
- **internal API = Console 소관 아님.** Console은 **자체 백엔드/internal API를 두지 않고** GW Admin API를 직접 소비(SPA·GW=SoT). Admin API 내부 접근 통제는 GW/③-I 소관. 이미 §1.2 Scope 반영 → 추가 작업 없음(확인).
- **트리거.** Console SRS 다듬기(스택 캐비엇 제거) — 저위험·baseline 전 반영 가능.
- **출처.** 2026-08-06 R5(7/30 R5 계승).
