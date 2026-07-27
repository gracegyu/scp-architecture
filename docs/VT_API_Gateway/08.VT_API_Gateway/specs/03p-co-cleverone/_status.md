# ③-P-CO — CleverOne GW 적응 (1·2·3·4단계 통합)

> **이 파일의 역할 = 승격용 구조화 씨앗(seed).** ③ SRS 작업 중 이 문서로 갈 내용을 **최종 목차에 대응되게** 미리 정리해 둔다(발견 즉시 캡처·인사이트 유실 방지). 정식 Sub-SRS/문서 집필은 **의존하는 ③ SRS 절이 baseline된 뒤 승격**한다 — 몰아쓰기가 아니라 "옮겨 붙이고 살 붙이기". 승격 트리거: ① ③ 해당 절 동결 + ② 소유권 확정(GW 공통 아님) + ③ 레포/템플릿 존재. 근거: ③이 흔들리는 동안 자식 문서를 미리 쓰면 개명·재번호가 수십 절로 번져 유지면이 폭발한다.

- 상태: **초안 작성중(2026-07-27·Raymond)** — **OnePager는 지금 작성**하되 **연동 *구현*만 post-v1.0**(v1.0 AXS 연동 = Straumann IO Scanner만·SRS §1.2·§2.7). 초안 정본 = 이 폴더의 `CleverOne-GW적응-OnePager.md`. 초안 완료 후 CleverOne 팀 인계.
  - **7/23 결정 반영**: 문서 범위를 **1·2·3·4단계 통합**으로 확정. **①호환성·②Presigned One Pager는 별도 미작성 — 이 CleverOne OnePager에 흡수**. presigned는 CleverOne이 **이용측**(CleverSpace 발급 API를 GW 경유로 호출·직접 연동 금지).
- 문서 유형: Engineering One Pager
- 범위: **① Vatech-\* 헤더·well-known·fallback(1단계)** · **② presigned 업로드 이용(2단계)** · **③ Direct→GW 경유(3단계)** · **④ Region 선택 UI(대안)·ClinicID(4단계)**
- 입력(spec_refs): ③ GW SRS — 헤더 §7.7.1·§2.3.0 · 호환성 §7.7 · 라우팅 §2.3.0·§4.5.1(A+C·ADR-11) · presigned 이용 §2.3.5·§7.4 · 리전 §7.3. Roadmap §4·§5.1, 실행 할당표, CleverOne SRS(references/CleverOne, Nick)
- 작성 모델(**7/23 변경**): **Nick → Raymond**로 이관 — **Raymond가 초안 작성**(GW SRS 계약 추출) → CleverOne 팀 인계. GW(Raymond)는 표준 계약(§7.7.1 헤더·§2.3.0 라우팅) + 초안까지.
- 리뷰어(제품 적응): 탁수용/Nick (Agenda R6)
- TBD: CleverOne SRS(Nick) 헤더·인증 상세 확보 · Region 선택 UI(대안) 범위
- 공식 등록처: TBD (CleverOne 제품 repo / VKS — 인계 시 결정)
