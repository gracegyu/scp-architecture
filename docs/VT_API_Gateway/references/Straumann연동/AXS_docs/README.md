# Straumann AXS Developer Portal — 문서 스냅샷

Straumann AXS 개발자 포털 가이드의 **내부 참고용 스냅샷**이다.

- 출처: [AXS Developer Portal](https://developer.axs.straumann.com/docs/getting-started)
- 취득일: 2026-06-16 (외부 문서는 통보 없이 변경될 수 있어, 설계 기준 시점 보존용으로 저장)
- 취급: Straumann 자료 — **Confidential**. 최신 내용은 항상 원본 포털을 함께 확인한다.

## 읽는 순서 (포털 구성과 동일)

순서가 곧 이해 흐름이다 — 시작 → 시나리오 → 인증 → 이벤트(Webhook) → 운영 리전.

| 순서 | 문서 | 내용 |
|------|------|------|
| 1 | [Getting Started](getting-started.md) | 사전 조건·클라이언트 등록·첫 API 호출(`Organization-ID` 헤더) |
| 2 | [Integration Scenarios Guide](Integration_guide.md) | 연동 시나리오 가이드 |
| 3 | [Authentication](authentication.md) | 토큰 발급·사용(인증 흐름) |
| 4 | [Webhooks](webhooks.md) | 외부 이벤트 수신 개요 |
| 4-1 | [Patient Events](webhooks/patientevents.md) | 환자 이벤트 |
| 4-2 | [File Events](webhooks/fileevents.md) | 파일 이벤트 |
| 4-3 | [Lab order Events](webhooks/laborderevents.md) | 기공 오더 이벤트 |
| 5 | [Regions of operation](regions_of_operation.md) | 운영 리전 |

## OpenAPI (API Reference)

포털 API Explorer의 **OpenAPI 3.0 전체 스펙** 스냅샷 — [openapi/](openapi/README.md) (5 API · `index.json` + YAML, 취득 2026-06-16).

> 우리 설계 연계: Webhook(4)은 GW Webhook Receiver(개발 Roadmap §2.7·ARD ADR-09), 인증(3)은 AXS OAuth 중계(5단계 갈래 A), `Organization-ID`는 ClinicID↔Org-ID 매핑과 직접 연결된다.
