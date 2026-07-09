# ③-P-LMP — LMP 제3자 서명 attestation (enroll B안 · 조건부 · gw/1.1+)

> **이 파일의 역할 = 승격용 구조화 씨앗(seed).** ③ SRS 작업 중 이 문서로 갈 내용을 **최종 목차에 대응되게** 미리 정리해 둔다(발견 즉시 캡처·인사이트 유실 방지). 정식 문서 집필은 **의존하는 ③ SRS 절이 baseline된 뒤 승격**한다. 승격 트리거: ① ③ 해당 절 동결 + ② 소유권 확정(GW 공통 아님) + ③ 레포/템플릿 존재.

- 상태: **초안**(OnePager.md 작성) · **조건부** — enroll 승인 flow **R9에서 B 채택 시만** 승격·개발
- 문서 유형: Engineering One Pager (기계적 적응이면 티켓)
- 범위: enroll **자동승인**용 **제3자(LMP) 서명 라이선스 attestation** — LMP가 서명 발급, EzServer가 릴레이, GW가 **LMP JWKS(런타임 fetch+캐시)** 로 검증 (§2.3.1 B안·§7.1.1·§7.1.4·Appendix B #42)
- 입력(spec_refs): ③ GW SRS(§2.3.1 B·§7.1.1·§7.1.4 JWKS·§7.2.5), Roadmap §4 LMP 행, Agenda R9, `ezserver-license-manager` `api/licenseapi.yaml`
- **소유(개발)**: **LMP/ELM 팀(ES 라이선스)** — 크로스팀(GW팀 아님). GW 소유자가 1차 초안 → 팀 인계
- **전제**: v1.0 baseline = **A안(C/S 수동 승인)** — 항상 존재(LMP 경로 밖 device fallback). B는 gw/1.1+ 조건부·A와 **공존**(택일 아님)
- TBD: R9 결정(A먼저/B먼저/동시) · **LMP가 GW-검증 가능 서명 attestation 발급 가능한지 확인** · claim set · 서명 키 회전
- 공식 등록처: LMP/ELM repo(`ewoosoft/ezserver`) 또는 GW `docs/` (인계 시 결정)

> 상세 초안 = [OnePager.md](OnePager.md). GW가 검증에 쓰는 키 = **LMP 공개키(JWKS)** 뿐(Cryptlex 키는 LMP/ELM 내부).
>
> **참고(별도·미래 — 7/9 R11).** 클라이언트 **SW 인벤토리의 정식(중앙) 수집·관리**(설치·update 연계)도 **신규 LMP** 소관으로 결정됐다 — 현재 GW는 **간이(interim)** 구현만 둔다(GW SRS §7.8.5). 본 seed(enroll attestation)와는 **별개 항목**(신규 LMP의 또 다른 기능)이라 여기 상술하지 않고 포인터만 둔다.
