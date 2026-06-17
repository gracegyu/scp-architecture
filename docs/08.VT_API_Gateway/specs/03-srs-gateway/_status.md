# ③ SRS — VatechAPIGateway (3+4단계, 메인 SSOT)

- 상태: 작성 중 (`SRS.md`) — §1.1·§1.2 확정 + §7 전 절 상세화 + §5·§6 정밀화 + **자체 검증 1차(§7 순서 7.1~7.9 복구·중복 스텁 제거, §4.5.1 DNS 엔드포인트 제안 추가)**. 남은 결정(TBD): v1.0 fleet 규모(→§5.1·5.2 수치)·DNS 호스트 확정(§4.5.1)·Swagger/ERD 링크·경로 B EOS 시점·MQTT 운영 주체·CCB 명단·감사 보존 기간 (**1순위 착수** — ④·③-C의 부모)
- 문서 유형: SRS
- 범위: GW PEP·라우팅·ClinicID/Region·Webhook Receiver 프레임·Presigned 공통·멀티 Region/GeoDNS·Vatech-* 규칙·Path B EOS·관리 API
- 입력(spec_refs): PRD(v2), ARD, 요구사항 명세, Roadmap 결정
- 공식 등록처: vt-api-gateway (Azure, es-platforms) `docs/specs/`
