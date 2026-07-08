# ④ Sub-SRS — Straumann(AXS) (5단계, ③ 하위)

> **이 파일의 역할 = 승격용 구조화 씨앗(seed).** ③ SRS 작업 중 이 문서로 갈 내용을 **최종 목차에 대응되게** 미리 정리해 둔다(발견 즉시 캡처·인사이트 유실 방지). 정식 Sub-SRS/문서 집필은 **의존하는 ③ SRS 절이 baseline된 뒤 승격**한다 — 몰아쓰기가 아니라 "옮겨 붙이고 살 붙이기". 승격 트리거: ① ③ 해당 절 동결 + ② 소유권 확정(GW 공통 아님) + ③ 레포/템플릿 존재. 근거: ③이 흔들리는 동안 자식 문서를 미리 쓰면 개명·재번호가 수십 절로 번져 유지면이 폭발한다.

- 상태: 미작성 (③ SRS baseline 후)
- 문서 유형: Sub-SRS
- 범위: AXS OAuth·Org-ID 매핑·리전, Webhook 이벤트·서명·재시도, **EzServer→AXS 갈래 A(우선 범위)**, unstable 환경
- 상위 여정 조망: **③ SRS §2.3 「클리닉 온보딩 end-to-end 여정」**(설치→LMP→enroll→AXS·가입 상태 A/B/C 분기 노출)이 GW 관점 뼈대를 두고, **본 ④가 AXS 내부 가입·구독 절차의 정본**이다(레이어 분리·Appendix B #44).
- 범위(구체화 대상 — ③ SRS §2.3.4 「연동 링크·org_mapping 생애주기」가 공통 레일만 정함): **AXS Organization Integration 링크 시퀀스** — `POST /v1/organization/integration/link`(`customerNumber`+integrating entity=Client ID)→`organizationId`, **동의 `PENDING`→`APPROVED` 처리·폴링**(Data Reader 동의 요건), `.../integration/check`(연결 확인)·`.../integration/unlink`(해제)·`.../integration/{customerNumber}/info`(region·countryCode). **가입 상태 A(Straumann+AXS)/B(Straumann만·AXS org 없음)/C(비-Straumann=범위 밖·가입 시 B 수렴)** 분류 + 처리(organizationId 보유=링크 생략 / 미보유=link 후 org-binding) 판정 로직. B의 **AXS org 확보 방식**(link 자동 생성 vs Straumann 별도 개통)·`customerNumber` 확보 경로·트리거 주체·organizationId→GW org_mapping 반영 시점. (org_mapping 테이블·org-bindings 로컬 API는 GW 공통 = ③ SRS 정본)
- 근거(AXS org API 정독 — `AXS_docs/openapi/organization.yml`): **`link`(`customerNumber`+`integratingEntityId`=Vatech Client ID) → `OrganizationIntegrationResponseDTO`{`organizationId`(uuid)·`consentVersion`·`status`∈PENDING/APPROVED/REJECTED/REVOKED}** — **`organizationId`는 link로 발급**받는다. **`check`는 입력으로 `organizationId`를 요구**(boolean 반환)하므로 orgId 미보유(최초)엔 쓸 수 없고 **link(customerNumber)가 orgId 획득 유일 경로**. `customerNumber`=Straumann 고객 식별자(**클리닉 사전 보유 여부는 가정 — R4 조사 대상**; AXS=호주 요구·기존 Straumann 계약 클리닉 존재 추정). `{customerNumber}/info`→region·countryCode. **연동 완료=이미 link·APPROVED(orgId 보유·check 확인) / 미연동=link 필요(customerNumber로 orgId 획득)**.
- 범위 외(현 시점): **CleverLab↔AXS 갈래 B — 미고려**(2026-06 회의). 외부 cloud 연동 일반 역량(C 프록시)은 GW에 유지되므로 향후 레지스트리 등록으로 활성화 가능. Roadmap §3.7.2(갈래 B)와 정합 필요.
- 입력(spec_refs): AXS OpenAPI 스냅샷(openapi/), AXS_docs 가이드, Straumann 분석보고서·회의록
- TBD (④ baseline 시 확정 — **시나리오가 flow·API를 정한다**):
  - **상태 A/B/C 실재·분포** — 호주 실사용 클리닉이 이미 Vatech 연동(link·APPROVED)돼 `organizationId` 보유(A)인지, 대부분 미연동(`customerNumber`만·B)인지, **둘 다 발생**하는지 → **주간회의 R4 확인**(AXS=호주 요구·기존 Straumann 계약 클리닉 존재 추정).
  - **`customerNumber` 확보 경로** — EzServer/클리닉이 자기 Straumann 고객번호를 어디서 얻는가(설치 입력·LMP·Straumann 포털).
  - **연동 트리거 주체·시점** — `link` 호출을 누가(C/S vs 클리닉 사용자) 언제(온보딩 중 vs 이후) 개시하는가.
  - **consent(`PENDING`→`APPROVED`) 처리** — org-admin 동의 대기·폴링·타임아웃·거부(`REJECTED`/`REVOKED`) 처리·재시도.
  - **연동 완료(상태 A) 시 `organizationId` 획득 경로** — `check`는 orgId 입력을 요구하므로, 기연동 클리닉의 orgId를 GW/EzServer가 어떻게 보유·조회하는가(저장 vs `link` 재호출).
  - AXS sandbox 자격증명(E2E·pilot 선결). (CleverLab 갈래 B는 현 시점 범위 외로 확정.)
- 공식 등록처: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/04-subsrs-straumann-axs/Sub-SRS.md (③ 하위)
