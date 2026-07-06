# ① One Pager — API 호환성 (1단계)

- 상태: 미작성 (착수 가능)
- 문서 유형: Engineering One Pager
- 입력(spec_refs): API 호환성 방안 비교 보고서, CleverSpace v1.3 CSV/xlsx/MMI, EzServer PMS SRS, **제품간 버전 호환 매트릭스 2종**(참조-카탈로그 §3: [C1] CleverOne–EzServer–DTKS Version · DTKS↔ES제품 연동 버전)
- TBD: 운영 호환성 매트릭스 확정값, CleverOne SRS(Nick)
- 공식 등록처: VKS(Confluence) 페이지 (2안 확정)

> **씨앗(작성 시 반영) — GW 호환 게이트(③ §7.7)와 동기화할 핵심 2건.**
> 1. **불일치 반응 = semver 자리별 3단계 정책.** 출하된 CleverOne↔EzServer 게이팅 선례: **major(1번째 자리) 미달 = 차단**(강제 종료) / **minor(2번째 자리) 미달 = 경고 + 실행**(일부 기능 제한·degrade) / **patch(3번째 자리) = 무시**. ① 매트릭스는 값뿐 아니라 **이 반응 정책·경고 헤더명·(API 버전↔제품 버전) 매핑**까지 확정해야 GW가 게이팅 구현 가능(③ §7.7.3·Appendix B #8).
> 2. **매트릭스 형식 선례.** "or higher"(하한+상향호환)·다중 지원 버전·출시일 행·외부 의존 note(예 NVIDIA 드라이버 ≥·3rd-party) — ① 확정본과 ③ `compat_matrix`(파일 SSOT→well-known JSON·§7.7.5) 스키마를 이 형식에 맞춘다.
> ※ 주의: 위 선례는 **제품/바이너리 버전 호환**이라 GW의 **API-계약 버전** 게이트로 옮길 때 의미론·형식만 차용(데이터 직접 재사용 불가).
