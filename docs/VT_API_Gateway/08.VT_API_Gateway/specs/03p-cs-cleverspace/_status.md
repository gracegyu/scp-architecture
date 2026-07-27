# ③-P-CS — CleverSpace GW 적응 (1·2·3·4단계 통합)

> **이 파일의 역할 = 승격용 구조화 씨앗(seed).** ③ SRS 작업 중 이 문서로 갈 내용을 **최종 목차에 대응되게** 미리 정리해 둔다(발견 즉시 캡처·인사이트 유실 방지). 정식 Sub-SRS/문서 집필은 **의존하는 ③ SRS 절이 baseline된 뒤 승격**한다 — 몰아쓰기가 아니라 "옮겨 붙이고 살 붙이기". 승격 트리거: ① ③ 해당 절 동결 + ② 소유권 확정(GW 공통 아님) + ③ 레포/템플릿 존재. 근거: ③이 흔들리는 동안 자식 문서를 미리 쓰면 개명·재번호가 수십 절로 번져 유지면이 폭발한다.

- 상태: **초안 작성중(2026-07-27 착수·Raymond)** — 초안 완료 후 **CleverSpace 팀에 인계**. 초안 정본 = 이 폴더의 `CleverSpace-GW적응-OnePager.md`. **의존 ③ 절은 baseline v1.0 동결(7/20·`spec-v1.0`) 완료**라 승격 트리거 ① 충족.
  - **7/23 결정 반영**: 문서 범위를 **1·2·3·4단계 통합**으로 확정. **①호환성·②Presigned One Pager는 별도 미작성 — 이 CleverSpace OnePager에 흡수**(딱 2개 제품 문서: CleverSpace·CleverOne). presigned는 CleverSpace가 발급 API 신규 개발(양쪽 다 GW 경유라 발급측=CleverSpace·이용측=CleverOne 모두 변경).
- 문서 유형: Engineering One Pager
- 범위: **① 서버 버전 체크·well-known·오류코드(1단계)** · **② presigned 발급 API 신규(2단계)** · **③ Direct→GW 경유 수신 정합(3단계)** · **④ 멀티 Region 구축(4단계·gw/1.2)**
- 입력(spec_refs): ③ GW SRS — 라우팅 §2.3.0·§4.1.2·§4.5.1(ADR-11) · presigned §2.3.5·§4.1.4·§7.4 · 호환성 §7.7(§7.7.1~5) · 프록시 오류·타임아웃 §7.5.4·§7.7.4 · 리전 §7.3(§7.3.1·§7.3.3·§7.3.5) · upstream 레지스트리 §4.1.2·§7.5.1. Roadmap §4, 실행 할당표, CleverSpace v1.3 기능요구정의서(references/CleverSpace)
- **비범위(명시)**: **CleverSpace는 Webhook 수신 대상이 아니다**(내부(B) 프록시·presigned 백엔드일 뿐 — §7.6.5·§2.3.6 확정). Webhook 클라우드 수신 = CleverLab만(갈래B·보류).
- 작성 모델(**7/23 변경**): **Raymond가 초안 작성**(GW SRS 계약 추출) → **CleverSpace 팀 인계·완성**. GW(Raymond)는 표준 계약 제공(§2.3.5 presigned 중계·§7.7 호환성·§4.1.2 라우팅·§7.3 리전) + 초안까지. **연동 *구현* 순서는 AXS(Straumann IO Scanner) 선행·CleverSpace 후행**(§7.5.2)이나 **OnePager는 지금 작성**.
- 리뷰어(제품 적응): 고형용/Larry (Agenda R6)
- TBD: presigned 발급 상세(세션·resumable·ETag·완료 콜백) = CleverSpace 소유 · 멀티 Region 구축 범위·AWS 미지원국 MinIO 전제 · GW→CleverSpace 리전 전달 방식(§7.3.3 확정 대상)
- 공식 등록처: TBD (CleverSpace 제품 repo / VKS — 인계 시 결정)
