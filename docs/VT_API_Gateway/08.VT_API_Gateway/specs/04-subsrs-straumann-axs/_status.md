# ④ Sub-SRS — Straumann(AXS) (5단계, ③ 하위)

> **이 파일의 역할 = 승격용 구조화 씨앗(seed).** ③ SRS 작업 중 이 문서로 갈 내용을 **최종 목차에 대응되게** 미리 정리해 둔다(발견 즉시 캡처·인사이트 유실 방지). 정식 Sub-SRS/문서 집필은 **의존하는 ③ SRS 절이 baseline된 뒤 승격**한다 — 몰아쓰기가 아니라 "옮겨 붙이고 살 붙이기". 승격 트리거: ① ③ 해당 절 동결 + ② 소유권 확정(GW 공통 아님) + ③ 레포/템플릿 존재. 근거: ③이 흔들리는 동안 자식 문서를 미리 쓰면 개명·재번호가 수십 절로 번져 유지면이 폭발한다.

- 상태: 미작성 (③ SRS baseline 후)
- 문서 유형: Sub-SRS
- 범위: AXS OAuth·Org-ID 매핑·리전, Webhook 이벤트·서명·재시도, **EzServer→AXS 갈래 A(우선 범위)**, unstable 환경
- 범위(구체화 대상 — ③ SRS §2.3.4 「연동 링크·org_mapping 생애주기」가 공통 레일만 정함): **AXS Organization Integration 링크 시퀀스** — `POST /v1/organization/integration/link`(`customerNumber`+integrating entity=Client ID)→`organizationId`, **동의 `PENDING`→`APPROVED` 처리·폴링**(Data Reader 동의 요건), `.../integration/check`(연결 확인)·`.../integration/unlink`(해제)·`.../integration/{customerNumber}/info`(region·countryCode). **경우 A(이미 연결·organizationId 보유)=링크 생략 / 경우 B(미연결)=링크 후 org-binding** 판정 로직. `customerNumber` 확보 경로·트리거 주체·organizationId→GW org_mapping 반영 시점. (org_mapping 테이블·org-bindings 로컬 API는 GW 공통 = ③ SRS 정본)
- 범위 외(현 시점): **CleverLab↔AXS 갈래 B — 미고려**(2026-06 회의). 외부 cloud 연동 일반 역량(C 프록시)은 GW에 유지되므로 향후 레지스트리 등록으로 활성화 가능. Roadmap §3.7.2(갈래 B)와 정합 필요.
- 입력(spec_refs): AXS OpenAPI 스냅샷(openapi/), AXS_docs 가이드, Straumann 분석보고서·회의록
- TBD: AXS sandbox 자격증명 (CleverLab 갈래 B는 현 시점 범위 외로 확정)
- 공식 등록처: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/04-subsrs-straumann-axs/Sub-SRS.md (③ 하위)
